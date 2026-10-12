# AGENTS.md

Guidance for AI coding agents working in this repository.

- This is the public website. Keep it short and accurate about the
  project's maturity; claims about features must match
  [the design](https://github.com/sparewall/sparewall/blob/main/docs/design.md).
- Plain HTML and CSS: no build step, no JavaScript, no third-party fonts,
  scripts or trackers. Use relative links so the site works on both
  sparewall.github.io and a custom domain (`404.html` is the exception: it
  is served at any path, so it uses root-relative links).
- The layout must work at phone width and in both light and dark schemes.
- The Pages workflow must pin third-party actions to a full commit SHA and
  request the minimum `permissions`.
