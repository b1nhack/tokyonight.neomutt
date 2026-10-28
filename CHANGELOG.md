# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-10-28

### Added

- Tokyo Night themes for NeoMutt, one file per tokyonight.nvim style:
  `night`, `storm`, `moon`, `day`.
- Two color depth variants per style:
  - `themes/*.neomuttrc` — 256-color, works in any terminal.
  - `themes/truecolor/*.neomuttrc` — exact `#RRGGBB` palette; requires
    `set color_directcolor = yes` and a TERM whose terminfo advertises
    16M colors (e.g. `xterm-direct`).
- Full coverage of all 55 of NeoMutt's colorable objects (verified against the
  object registry in `color/commands.c` and a real binary): general UI, sidebar,
  compose, quoted levels 0–9, index flag patterns and per-column colors, body
  markup regexes and status-bar counter highlighting. This includes `italic`
  and the `stripe_even`/`stripe_odd` help-page stripes, which the manual's
  color tables do not list yet.
- `install.sh` — copies themes to `~/.config/neomutt/` and prints the
  `source` line.
- `scripts/generate_themes.py` — single source of truth that renders both
  variants from the tokyonight.nvim palettes.
- `scripts/generate_previews.py` — renders the SVG previews from the theme
  files themselves.
