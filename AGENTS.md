# AGENTS.md

Guidance for AI coding agents working in this repository.

- This is the public website. Keep it short and accurate about the
  project's maturity; claims about features must match
  [the design](https://github.com/sparewall/sparewall/blob/main/docs/design.md).
- Plain HTML and CSS: no JavaScript, no third-party fonts, scripts or
  trackers. `build-releases.py` fills in the release history of the home page and
  `releases/` from the GitHub release notes; `docs/` is built by
  `build-docs.sh` (MkDocs, with this site's own theme in `docs-theme/` and
  `assets/docs.css`) from the latest published sparewall release, and
  the same rules apply to it. Use relative links so the site works on both
  sparewall.github.io and a custom domain (`404.html` is the exception: it
  is served at any path, so it uses root-relative links).
- Release history comes from the release notes on GitHub; don't write
  it by hand here. A `notes/TAG.md` override must match those notes and,
  like them, must not mention any real deployment (its hosts, network or
  state). README.md lists what to update with each release.
- The layout must work at phone width and in both light and dark schemes.
- The Pages workflow must pin third-party actions to a full commit SHA and
  request the minimum `permissions`.
