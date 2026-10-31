#!/usr/bin/env python3
"""Fill in the site's release history from the GitHub release notes.

    build-releases.py RELEASES.json SITE

RELEASES.json is the list of sparewall releases from the GitHub API
(`gh api --paginate repos/sparewall/sparewall/releases | jq -s add`).
SITE is the assembled site, whose index.html and releases/index.html
have the placeholders this replaces:

- index.html: <!-- latest-badge --> and <!-- release-list -->
- releases/index.html: <!-- releases-toc --> and <!-- releases -->

A release's entry is its notes up to the boilerplate every release
repeats (the changes list, installing, verifying). notes/TAG.md, if it
exists, is used instead of the notes on GitHub, for a release whose
notes don't read well on their own.
"""
import datetime
import html
import json
import pathlib
import re
import sys

import markdown

REPO = "https://github.com/sparewall/sparewall"
# The first of these headings ends the part of the notes shown here.
BOILERPLATE = ("what's changed", "new contributors", "installing and upgrading",
               "verifying the downloads")
HOME_RELEASES = 3


def version(r):
    return r["tag_name"].removeprefix("v")


def when(r):
    d = datetime.datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))
    return f"{d:%B} {d.day}, {d.year}"


def notes(r, notes_dir):
    """The notes of r, without the boilerplate, as (lede, rest)."""
    override = notes_dir / f"{r['tag_name']}.md"
    text = override.read_text() if override.exists() else (r.get("body") or "")
    text = text.replace("\r\n", "\n")
    kept = []
    for line in text.split("\n"):
        m = re.match(r"#+\s+(.*)", line)
        if (m and m.group(1).strip().lower() in BOILERPLATE) or line.startswith("**Full Changelog**"):
            break
        kept.append(line)
    text = "\n".join(kept).strip()
    first, _, rest = text.partition("\n\n")
    if re.match(r"\s*([#|>`]|[-*+] |\d+\. )", first):
        return "", text
    return first.replace("\n", " "), rest


def to_html(text, shift=1):
    """GitHub-flavoured release notes as HTML, headings one level down."""
    # Python-Markdown nests lists at four spaces, GitHub at two.
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            indent = len(line) - len(line.lstrip(" "))
            line = " " * indent + line
            line = re.sub(r"^(#+)", lambda m: "#" * min(6, len(m.group(1)) + shift), line)
        out.append(line)
    text = "\n".join(out)
    # #123 is an issue or pull request, as on GitHub.
    text = re.sub(r"(?<![\w/&#`\[])#(\d+)\b", rf"[#\1]({REPO}/issues/\1)", text)
    return markdown.markdown(text, extensions=["fenced_code", "tables", "sane_lists"])


def inline(text):
    """One paragraph as inline HTML."""
    return re.sub(r"^<p>|</p>$", "", to_html(text).strip())


def summary(lede):
    """The first sentence of a lede, without "Sparewall X.Y.Z"."""
    s = re.split(r"(?<=\.)\s+(?=[A-Z])", lede, maxsplit=1)[0]
    s = re.sub(r"^Sparewall \S+ (\w)", lambda m: m.group(1).upper(), s)
    return inline(s)


def main():
    releases_json, site = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    notes_dir = pathlib.Path(__file__).resolve().parent / "notes"
    rels = [r for r in json.loads(releases_json.read_text())
            if not r["draft"] and r.get("published_at")]
    rels.sort(key=lambda r: r["published_at"], reverse=True)
    finals = [r for r in rels if not r["prerelease"]]
    latest = finals[0]
    # A prerelease newer than the latest release has its docs in docs/next/;
    # every other prerelease is listed briefly at the end.
    nxt = next((r for r in rels if r["prerelease"]
                and r["published_at"] > latest["published_at"]), None)
    shown = ([nxt] if nxt else []) + finals
    earlier = [r for r in rels if r["prerelease"] and r is not nxt]

    articles, toc = [], []
    for r in shown:
        v, tag = version(r), html.escape(r["tag_name"])
        lede, rest = notes(r, notes_dir)
        badge, docs = "", ""
        if r is latest:
            badge = ' <span class="badge latest">Latest release</span>'
            docs = ' &middot; <a href="../docs/">Documentation</a>'
        elif r is nxt:
            badge = ' <span class="badge">Prerelease</span>'
            docs = ' &middot; <a href="../docs/next/">Documentation</a>'
        toc.append(f'<a href="#{tag}">{html.escape(v)}</a>')
        articles.append(f"""<article class="release" id="{tag}">
      <header>
        <h2>{html.escape(v)}{badge}</h2>
        <p class="when">{when(r)} &middot; <a href="{REPO}/releases/tag/{tag}">Notes and downloads</a>{docs}</p>
      </header>
      {f'<p class="lede">{inline(lede)}</p>' if lede else ''}
      {to_html(rest, shift=1)}
    </article>""")
    if earlier:
        toc.append('<a href="#prereleases">Earlier prereleases</a>')
        items = []
        for r in earlier:
            v, tag = version(r), html.escape(r["tag_name"])
            d = datetime.datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))
            m = re.match(r"(.*)-rc\d+$", v)
            what = (f"a release candidate for {html.escape(m.group(1))}." if m
                    else summary(notes(r, notes_dir)[0]))
            what = what[:1].lower() + what[1:] if not what[1:2].isupper() else what
            items.append(f'<li><a href="{REPO}/releases/tag/{tag}"><strong>{html.escape(v)}</strong></a>'
                         f" ({d:%B} {d.day}, {d.year}): {what}</li>")
        articles.append("""<article class="release" id="prereleases">
      <header>
        <h2>Earlier prereleases</h2>
      </header>
      <ul>
        """ + "\n        ".join(items) + """
      </ul>
    </article>""")

    page = site / "releases" / "index.html"
    text = page.read_text()
    text = text.replace("<!-- releases-toc -->", "\n      ".join(toc))
    text = text.replace("<!-- releases -->", "\n\n    ".join(articles))
    page.write_text(text)

    home = site / "index.html"
    text = home.read_text()
    v, tag = html.escape(version(latest)), html.escape(latest["tag_name"])
    text = text.replace("<!-- latest-badge -->",
                        f'<a class="badge" href="releases/#{tag}">{v} is out &middot; what&rsquo;s new</a>')
    items = []
    for r in finals[:HOME_RELEASES]:
        tag = html.escape(r["tag_name"])
        items.append(f'<li><a href="releases/#{tag}"><strong>{html.escape(version(r))}</strong></a>'
                     f'<span class="when">{when(r)}{" &middot; latest" if r is latest else ""}</span>'
                     f"<span>{summary(notes(r, notes_dir)[0])}</span></li>")
    text = text.replace("<!-- release-list -->", "\n          ".join(items))
    home.write_text(text)


if __name__ == "__main__":
    main()
