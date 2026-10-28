#!/usr/bin/env python3
"""Generate the tokyonight.neomutt theme files.

Emits, for each tokyonight.nvim style (night, storm, moon, day):
  themes/tokyonight-<style>.neomuttrc            256-color, works everywhere
  themes/truecolor/tokyonight-<style>.neomuttrc  exact #RRGGBB, needs truecolor

Usage:  python3 scripts/generate_themes.py
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"

# ---------------------------------------------------------------------------
# Palettes — colors taken from folke/tokyonight.nvim (the generated extras,
# e.g. extras/helix, reveal the fully-resolved values including derived ones
# such as bg_highlight and bg_search).
# ---------------------------------------------------------------------------
PALETTES: dict[str, dict[str, str]] = {
    "night": {
        "fg": "#c0caf5", "fg_dark": "#a9b1d6", "bg_dark": "#16161e",
        "bg_highlight": "#292e42", "bg_search": "#3d59a1",
        "comment": "#565f89", "dark3": "#545c7e", "dark5": "#737aa2",
        "red": "#f7768e", "green": "#9ece6a", "green1": "#73daca",
        "magenta": "#bb9af7", "cyan": "#7dcfff", "blue": "#7aa2f7",
        "blue5": "#89ddff", "orange": "#ff9e64", "teal": "#1abc9c",
        "yellow": "#e0af68",
    },
    "storm": {
        "fg": "#c0caf5", "fg_dark": "#a9b1d6", "bg_dark": "#1f2335",
        "bg_highlight": "#292e42", "bg_search": "#3d59a1",
        "comment": "#565f89", "dark3": "#545c7e", "dark5": "#737aa2",
        "red": "#f7768e", "green": "#9ece6a", "green1": "#73daca",
        "magenta": "#bb9af7", "cyan": "#7dcfff", "blue": "#7aa2f7",
        "blue5": "#89ddff", "orange": "#ff9e64", "teal": "#1abc9c",
        "yellow": "#e0af68",
    },
    "moon": {
        "fg": "#c8d3f5", "fg_dark": "#828bb8", "bg_dark": "#1e2030",
        "bg_highlight": "#2f334d", "bg_search": "#3e68d7",
        "comment": "#636da6", "dark3": "#545c7e", "dark5": "#737aa2",
        "red": "#ff757f", "green": "#c3e88d", "green1": "#4fd6be",
        "magenta": "#c099ff", "cyan": "#86e1fc", "blue": "#82aaff",
        "blue5": "#89ddff", "orange": "#ff966c", "teal": "#4fd6be",
        "yellow": "#ffc777",
    },
    "day": {
        "fg": "#3760bf", "fg_dark": "#6172b0", "bg_dark": "#d0d5e3",
        "bg_highlight": "#c4c8da", "bg_search": "#7890dd",
        "comment": "#848cb5", "dark3": "#8990b3", "dark5": "#68709a",
        "red": "#f52a65", "green": "#587539", "green1": "#387068",
        "magenta": "#9854f1", "cyan": "#007197", "blue": "#2e7de9",
        "blue5": "#006a83", "orange": "#b15c00", "teal": "#118c74",
        "yellow": "#8c6c3e",
    },
}

# ---------------------------------------------------------------------------
# Theme body: (object line, comment).
#   {token}       → color from the palette (or its nearest 256-color entry)
#   ATTRS:a b     → video attributes placed before the colors
#   default       → the transparent color
# ---------------------------------------------------------------------------
BODY: list[tuple[str, str]] = [
    # --- general ---
    ("normal        {fg} default",                'text is "text"'),
    ("error         {red} default",               "error messages"),
    ("warning       {yellow} default",            "warning messages"),
    ("message       {green} default",             "informational messages"),
    ("options       ATTRS:bold {magenta} default", "key letters in multi-choice questions"),
    ("prompt        ATTRS:bold {blue} default",   "a question"),
    ("progress      {blue} {bg_highlight}",       "visual progress bar"),
    ("status        {fg_dark} default",           "status bar"),
    ("indicator     {fg} {bg_highlight}",         "current item in a menu"),
    ("tree          {fg_dark} default",           "thread tree arrows"),
    ("tilde         {comment} default",           '"~" padding in the pager'),
    ("markers       {orange} default",            '"+" wrapped-line markers'),
    ("hdrdefault    {fg_dark} default",           "default header text in the pager"),
    ('header        {blue} default "^From:"',     "header labels are titles"),
    ('header        {blue} default "^(To|Cc):"',  ""),
    ('header        {blue} default "^Subject:"',  ""),
    ('header        {blue} default "^Date:"',     ""),
    ("attachment    {magenta} default",           "attachment headers"),
    ('attach_headers {dark5} default ".*"',       "attachment header block"),
    ("search        default {bg_search}",         "search matches in the pager"),
    ("signature     {comment} default",           "signature lines"),
    ("bold          ATTRS:bold {fg} default",     "bold text in message bodies"),
    ("underline     ATTRS:underline {fg} default", "underlined text in message bodies"),
    ("italic        ATTRS:italic {fg} default",   "italic text in message bodies"),
    ("stripe_even   default default",             "help-page stripes: even lines stay transparent"),
    ("stripe_odd    default {bg_dark}",           "help-page stripes: odd lines get a subtle tint"),
    # --- sidebar ---
    ("sidebar_background {fg_dark} {bg_dark}",    "the sidebar panel"),
    ("sidebar_divider    {bg_highlight} default", "sidebar/index divider"),
    ("sidebar_highlight  {fg} {bg_highlight}",    "sidebar cursor"),
    ("sidebar_indicator  {blue} default",         "mailbox open in the index"),
    ("sidebar_new        {green} default",        "mailboxes with new mail"),
    ("sidebar_unread     {yellow} default",       "mailboxes with unread mail"),
    ("sidebar_flagged    {red} default",          "mailboxes with flagged mail"),
    ("sidebar_ordinary   {dark5} default",        "mailboxes with nothing special"),
    ("sidebar_spool_file {teal} default",         "the incoming-mail mailbox"),
    # --- compose ---
    ("compose_header            ATTRS:bold {blue} default", "header labels, e.g. From:"),
    ("compose_security_none     {dark5} default",  "mail will not be encrypted or signed"),
    ("compose_security_sign     {cyan} default",   "mail will be signed"),
    ("compose_security_encrypt  {blue} default",   "mail will be encrypted"),
    ("compose_security_both     {green1} default", "mail will be encrypted and signed"),
    # --- quoted text ---
    ("quoted  {fg_dark} default", "quoted text, level 0 (quoted0; \"quoted\" kept for older NeoMutt)"),
    ("quoted1 {cyan} default",    "quoted text, level 1"),
    ("quoted2 {blue5} default",   "quoted text, level 2"),
    ("quoted3 {comment} default", "quoted text, level 3"),
    ("quoted4 {dark5} default",   "quoted text, level 4"),
    ("quoted5 {dark3} default",   "quoted text, level 5"),
    ("quoted6 {dark3} default",   "quoted text, level 6"),
    ("quoted7 {dark3} default",   "quoted text, level 7"),
    ("quoted8 {dark3} default",   "quoted text, level 8"),
    ("quoted9 {dark3} default",   "quoted text, level 9"),
    # --- index: whole-line flag colors ---
    ("index {green} default ~N",   "new messages"),
    ("index {red} default ~F",     "flagged messages"),
    ("index {magenta} default ~T", "tagged messages"),
    ("index {red} default ~D",     "messages to delete"),
    # --- index: per-column colors ---
    ("index_number   {dark3} default \".*\"",   "message number column"),
    ("index_size     {dark3} default \".*\"",   "message size column"),
    ("index_date     {comment} default \".*\"", "date column"),
    ("index_flags    {orange} default \".*\"",  "flags column"),
    ("index_collapsed {yellow} default \".*\"", "collapsed-thread count"),
    ("index_label    {magenta} default \".*\"", "label column"),
    ("index_tags     {green1} default \".*\"",  "transformed tags column"),
    ("index_tag      {green1} default \".*\"",  "tags column"),
    ("index_author   {blue} default \"!(~N|~F|~T|~D)\"", "author column (except on flag-colored lines)"),
    ("index_subject  {fg} default \"!(~N|~F|~T|~D)\"",   "subject column (except on flag-colored lines)"),
    # --- message body: addresses, URLs, markup ---
    ("body {teal} default ([\\-\\.+_a-zA-Z0-9]+@[\\-\\.a-zA-Z0-9]+)", "email addresses"),
    ("body {teal} default (https?|ftp)://[\\-\\.,/%~_:?&=\\#a-zA-Z0-9]+", "URLs"),
    ("body ATTRS:bold {blue5} default (^|[[:space:]])\\*[^[:space:]]+\\*([[:space:]]|$)", "*bold* markup"),
    ("body ATTRS:underline {blue5} default (^|[[:space:]])_[^[:space:]]+_([[:space:]]|$)", "_underlined_ markup"),
    ("body ATTRS:italic {blue5} default (^|[[:space:]])/[^[:space:]]+/([[:space:]]|$)", "/italic/ markup"),
    # --- status bar counters ---
    ("status {green} default 'New:[0-9]+'",   "new-mail counter"),
    ("status {red} default 'Del:[0-9]+'",     "deleted counter"),
    ("status {red} default 'Flag:[0-9]+'",    "flagged counter"),
    ("status {yellow} default 'Post:[0-9]+'", "postponed counter"),
]

# section headers inserted before the given first object of a section
SECTIONS = [
    ("normal", "general"),
    ("sidebar_background", "sidebar"),
    ("compose_header", "compose"),
    ("quoted", "quoted text"),
    ("index", "index: whole-line flag colors"),
    ("index_number", "index: per-column colors\n(author/subject use a complement pattern so they are only tinted on\nlines that have no whole-line flag color)"),
    ("body", "message body: addresses, URLs, markup"),
    ("status", "status bar counters"),
]
# `index` also matches index_number etc., and `status` has a plain form early
# in the general section — use unique sentinels for those.
SECTION_SENTINELS = {"index": "~N", "body": "@", "status": "New:"}

HEADER_TRUECOLOR = """\
# vim: filetype=neomuttrc

# Tokyo Night ({title}) theme for NeoMutt
# Palette: https://github.com/folke/tokyonight.nvim (style: {style})
# Generated by scripts/generate_themes.py — do not edit by hand.
#
# This variant uses exact 24-bit colors. It needs BOTH of:
#   1. set color_directcolor = yes            (done below)
#   2. a TERM whose terminfo advertises 16M colors (e.g. xterm-direct)
# Otherwise every line below errors with "color not supported by term".
# See the README for details.

set color_directcolor = yes
"""

HEADER_256 = """\
# vim: filetype=neomuttrc

# Tokyo Night ({title}) theme for NeoMutt
# Palette: https://github.com/folke/tokyonight.nvim (style: {style})
# Generated by scripts/generate_themes.py — do not edit by hand.
#
# This variant uses the 256-color palette, so it works on any terminal.
# For the exact Tokyo Night colors use the truecolor variant instead
# (themes/truecolor/, see the README).
"""


# ---------------------------------------------------------------------------
# xterm-256 palette (entries 16..255) for the nearest-color approximation.
# Entries 0..15 are excluded on purpose: they are theme-dependent.
# ---------------------------------------------------------------------------
def _xterm256_rgb() -> list[tuple[int, int, int]]:
    rgb: list[tuple[int, int, int]] = [(-1, -1, -1)] * 16
    steps = (0, 95, 135, 175, 215, 255)
    for r in steps:
        for g in steps:
            for b in steps:
                rgb.append((r, g, b))
    for i in range(24):
        v = 8 if i == 0 else 8 + 10 * i
        rgb.append((v, v, v))
    return rgb


_XTERM = _xterm256_rgb()


def nearest_256(hex_color: str) -> int:
    """Index of the closest xterm-256 color (weighted RGB distance)."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    best, best_dist = 16, 1 << 30
    for idx, (cr, cg, cb) in enumerate(_XTERM):
        if cr < 0:
            continue
        dist = 2 * (r - cr) ** 2 + 4 * (g - cg) ** 2 + 3 * (b - cb) ** 2
        if dist < best_dist:
            best, best_dist = idx, dist
    return best


def render(style: str, truecolor: bool) -> str:
    palette = PALETTES[style]

    def fmt_color(token: str) -> str:
        if token == "default":
            return "default"
        hex_color = palette[token.strip("{}")]
        return hex_color if truecolor else f"color{nearest_256(hex_color)}"

    lines: list[str] = []
    header = HEADER_TRUECOLOR if truecolor else HEADER_256
    lines.append(header.format(title=style, style=style))

    for template, comment in BODY:
        for trigger, heading in SECTIONS:
            if template.split()[0] == trigger and SECTION_SENTINELS.get(trigger, trigger) in template:
                lines.append("")
                lines.append("# " + "-" * 74)
                lines.extend(f"# {l}" for l in heading.splitlines())
                break

        attrs: list[str] = []
        plain = template.replace("ATTRS:", "")
        tokens = plain.split()
        obj = tokens[0]
        rest = tokens[1:]
        while rest and rest[0] in ("bold", "underline", "italic", "none", "reverse", "standout"):
            attrs.append(rest.pop(0))
        fg_tok, bg_tok = rest[0], rest[1]
        pattern = " ".join(rest[2:])

        parts = ["color", obj, *attrs, fmt_color(fg_tok), fmt_color(bg_tok)]
        if pattern:
            parts.append(pattern)
        line = " ".join(parts)
        if comment:
            pad = max(1, 56 - len(line))
            line = f"{line}{' ' * pad}# {comment}"
        lines.append(line)

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    (THEMES / "truecolor").mkdir(parents=True, exist_ok=True)
    for style in PALETTES:
        for truecolor in (False, True):
            sub = THEMES / ("truecolor" if truecolor else "")
            out = sub / f"tokyonight-{style}.neomuttrc"
            out.write_text(render(style, truecolor), encoding="utf-8")
            print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
