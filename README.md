# sparewall.github.io

The Sparewall website, served by GitHub Pages at
<https://sparewall.github.io/>.

The home page and `releases/` are plain static HTML and CSS with no
third-party requests. Their release history (the home page's badge and
release list, and every entry on `releases/`) is filled in at build time
from the release notes on GitHub, by `build-releases.py`, in place of
the `<!-- ... -->` placeholders. An entry is a release's notes up to
`## What's Changed`; `notes/TAG.md` replaces the notes of a release
whose notes on GitHub don't read well on their own. To preview the
site with its release history:

```shell
mkdir _site && cp -r index.html 404.html releases assets _site/
gh api --paginate repos/sparewall/sparewall/releases | jq -s add > releases.json
.venv/bin/python build-releases.py releases.json _site
python3 -m http.server -d _site 8000
```

`/docs/` is the documentation of the latest published sparewall release
(not main, a draft or a prerelease), built with MkDocs and this site's own
theme, without JavaScript. When a prerelease is newer than that release,
its documentation is built beside it, under `/docs/next/`, with a banner
that says so. To build it locally from a sparewall checkout of a release tag:

```shell
python3 -m venv .venv
.venv/bin/pip install --require-hashes -r requirements-docs.txt
PATH=$PWD/.venv/bin:$PATH ./build-docs.sh ../sparewall v0.2.0 _site/docs
# A prerelease, after the release (MkDocs empties docs/ first):
PATH=$PWD/.venv/bin:$PATH ./build-docs.sh --preview ../sparewall-next v0.3.0-rc1 _site/docs/next
```

`requirements-docs.txt` is generated from `requirements-docs.in` with
`uv pip compile --generate-hashes --python-version 3.12`.

Pull requests build the site without deploying it. Pushing to `main` deploys through `.github/workflows/pages.yml`, which
assembles the home page and the docs into `_site/` and publishes them. It
also runs every six hours, so a newly published release reaches the site
(its notes and its docs) without a push here; run it by hand to publish
one at once.

## With each release

Nothing, usually: the next scheduled build lists the release, links the
docs and badge to it, and moves a replaced prerelease to the list of
earlier ones. Edit the release's notes on GitHub, not this repository,
to change what the site says about it. By hand, when they change:

- The roadmap and the features the home page describes, such as a
  "New in" badge.
- New UI screenshots go in `assets/screenshots/` as WebP, a light and a
  dark one each, 1600 pixels wide, taken from the demo
  (`tests/vm/demo.sh` in sparewall). Check them for anything that
  should not be public.

## License

The site content is licensed under the GNU General Public License v3.0
only, like the rest of Sparewall; see [`LICENSE`](LICENSE).
