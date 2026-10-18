#!/bin/bash
# Build the documentation of a Sparewall release into OUT with MkDocs:
# the release's docs/, this site's theme and overview page, and links
# outside docs/ (examples, cosign.pub) pointed at GitHub at the tag.
#
#   ./build-docs.sh SPAREWALL-CHECKOUT TAG OUT
set -euo pipefail
src=${1:?usage: build-docs.sh SPAREWALL-CHECKOUT TAG OUT}
tag=${2:?usage: build-docs.sh SPAREWALL-CHECKOUT TAG OUT}
out=${3:?usage: build-docs.sh SPAREWALL-CHECKOUT TAG OUT}
here=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cp -r "$src/docs" "$work/docs"
cp "$here/docs-index.md" "$work/docs/index.md"
# A link out of docs/ goes to the file on GitHub, at the release.
sed -i -E "s#\]\(\.\./([^)]+)\)#](https://github.com/sparewall/sparewall/blob/$tag/\1)#g" "$work"/docs/*.md
# GitHub needs a pipe in a table's code span escaped; Python-Markdown
# keeps code spans literal (and does not split cells inside them).
python3 - "$work"/docs/*.md <<'PY'
import re, sys
for f in sys.argv[1:]:
    lines = open(f).read().split("\n")
    for i, l in enumerate(lines):
        if l.lstrip().startswith("|"):
            lines[i] = re.sub(r"`[^`]*`", lambda m: m.group(0).replace("\\|", "|"), l)
    open(f, "w").write("\n".join(lines))
PY

DOCS_DIR=$work/docs SPAREWALL_TAG=$tag SPAREWALL_VERSION=${tag#v} \
DOCS_SITE_NAME="Sparewall ${tag#v} documentation" \
    mkdocs build -q -f "$here/mkdocs.yml" -d "$out"
