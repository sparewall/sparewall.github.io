#!/bin/bash
# Build the documentation of a Sparewall release into OUT with MkDocs:
# the release's docs/, this site's theme and overview page, and links
# outside docs/ (examples, cosign.pub) pointed at GitHub at the tag.
#
#   ./build-docs.sh [--preview] SPAREWALL-CHECKOUT TAG OUT
#
# --preview marks the build as a prerelease's documentation, published
# beside the release's under docs/next/.
set -euo pipefail
preview=
if [ "${1:-}" = --preview ]; then
    preview=1
    shift
fi
usage="usage: build-docs.sh [--preview] SPAREWALL-CHECKOUT TAG OUT"
src=${1:?$usage}
tag=${2:?$usage}
out=${3:?$usage}
here=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cp -r "$src/docs" "$work/docs"

# The overview page lists the HTTP API from the release that has it on.
index=$(cat "$here/docs-index.md")
if [ -d "$work/docs/api" ]; then
    index=${index//'<!-- api -->'/'- [HTTP API](api/README.md): the calls, errors and statuses of the
  HTTP API the web UI uses, and the OpenAPI document that describes it.'}
else
    index=${index//$'<!-- api -->\n'/}
fi
if [ -n "$preview" ]; then
    index=${index//'This is the documentation of the latest Sparewall release.'/'This is the documentation of Sparewall '"${tag#v}"', a prerelease. The
documentation of the latest release is [one level up](../).'}
fi
printf '%s\n' "$index" > "$work/docs/index.md"

# The site's config, with its theme found from here and the HTTP API in
# the nav only when the release has it.
sed -e "s#^  custom_dir: .*#  custom_dir: $here/docs-theme#" \
    "$here/mkdocs.yml" > "$work/mkdocs.yml"
if [ ! -d "$work/docs/api" ]; then
    sed -i '/api\/README\.md/d' "$work/mkdocs.yml"
fi

python3 - "$tag" "$work/docs" <<'PY'
import pathlib, re, sys
tag, docs = sys.argv[1], pathlib.Path(sys.argv[2])
for f in docs.rglob("*.md"):
    text = f.read_text()
    # A link out of docs/ goes to the file on GitHub, at the release.
    up = "../" * (len(f.relative_to(docs).parts))
    text = re.sub(r"\]\(" + re.escape(up) + r"([^)]+)\)",
                  lambda m: f"](https://github.com/sparewall/sparewall/blob/{tag}/{m.group(1)})",
                  text)
    # GitHub needs a pipe in a table's code span escaped; Python-Markdown
    # keeps code spans literal (and does not split cells inside them).
    lines = text.split("\n")
    for i, l in enumerate(lines):
        if l.lstrip().startswith("|"):
            lines[i] = re.sub(r"`[^`]*`", lambda m: m.group(0).replace("\\|", "|"), l)
    f.write_text("\n".join(lines))
PY

# The theme reaches the site's assets and home page through ROOT.
DOCS_DIR=$work/docs SPAREWALL_TAG=$tag SPAREWALL_VERSION=${tag#v} \
DOCS_ROOT=${preview:+../}../ DOCS_PREVIEW=${preview:-} \
DOCS_SITE_NAME="Sparewall ${tag#v} documentation" \
    mkdocs build -q -f "$work/mkdocs.yml" -d "$(realpath -m "$out")"
