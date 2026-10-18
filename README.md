# sparewall.github.io

The Sparewall website, served by GitHub Pages at
<https://sparewall.github.io/>.

The home page is plain static HTML and CSS with no build step and no
third-party requests. Open `index.html` in a browser to preview it, or serve
the directory:

```shell
python3 -m http.server -d . 8000
```

`/docs/` is the documentation of the latest published sparewall release
(not main, a draft or a prerelease), built with MkDocs and this site's own
theme, without JavaScript. To build it locally from a sparewall checkout of a release tag:

```shell
python3 -m venv .venv
.venv/bin/pip install --require-hashes -r requirements-docs.txt
PATH=$PWD/.venv/bin:$PATH ./build-docs.sh ../sparewall v0.1.0 _site/docs
```

`requirements-docs.txt` is generated from `requirements-docs.in` with
`uv pip compile --generate-hashes --python-version 3.12`.

Pushing to `main` deploys through `.github/workflows/pages.yml`, which
assembles the home page and the docs into `_site/` and publishes them. It
also runs every six hours, so a newly published release reaches the docs
without a push here; run it by hand to publish one at once.

## License

The site content is licensed under the GNU General Public License v3.0
only, like the rest of Sparewall; see [`LICENSE`](LICENSE).
