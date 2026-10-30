# sparewall.github.io

The Sparewall website, served by GitHub Pages at
<https://sparewall.github.io/>.

The home page and `releases/` are plain static HTML and CSS with no build step and no
third-party requests. Open `index.html` in a browser to preview it, or serve
the directory:

```shell
python3 -m http.server -d . 8000
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
also runs every six hours, so a newly published release reaches the docs
without a push here; run it by hand to publish one at once.

## With each release

The home page and `releases/index.html` describe releases by hand. When
one is published:

- Add it to `releases/index.html`, from its GitHub notes, and update the
  home page's badge, release list and roadmap.
- When a final release replaces a prerelease, links to `docs/next/` stop
  working: point them at `docs/`.
- New UI screenshots go in `assets/screenshots/` as WebP, a light and a
  dark one each, 1600 pixels wide, taken from the demo
  (`tests/vm/demo.sh` in sparewall). Check them for anything that
  should not be public.

## License

The site content is licensed under the GNU General Public License v3.0
only, like the rest of Sparewall; see [`LICENSE`](LICENSE).
