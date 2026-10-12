# sparewall.github.io

The Sparewall website, served by GitHub Pages at
<https://sparewall.github.io/>.

The site is plain static HTML and CSS with no build step and no third-party
requests. Open `index.html` in a browser to preview it, or serve the
directory:

```shell
python3 -m http.server -d . 8000
```

Pushing to `main` deploys through `.github/workflows/pages.yml`, which
copies the site into `_site/` and publishes it.

## Plans

Once [sparewall/sparewall](https://github.com/sparewall/sparewall) has
tagged releases, the workflow will check out the latest release, build its
`docs/` with MkDocs, and publish them under `/docs/`.

## License

The site content is licensed under the GNU General Public License v3.0
only, like the rest of Sparewall; see [`LICENSE`](LICENSE).
