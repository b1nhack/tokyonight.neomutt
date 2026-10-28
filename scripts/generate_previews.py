#!/usr/bin/env python3
"""Generate SVG previews of every tokyonight variant for NeoMutt.

Colors are parsed from the *truecolor* theme files, so the previews always
show the exact palette. The mock screen shows a sidebar, the message index
(with whole-line flag colors), a status bar (with counter highlighting) and
the pager (headers, quoted text, address/URL markup).

Usage:  python3 scripts/generate_previews.py
Output: assets/preview-<variant>.svg
"""

from __future__ import annotations

import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
VARIANTS = ("night", "storm", "moon", "day")

FONT = "ui-monospace, 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Consolas, monospace"
FONT_SIZE = 13
CHAR_W = 7.8
LINE_H = 20
PAD_X = 16
PAD_Y = 14
TITLE_H = 36
SIDEBAR_W = 26  # chars
DOT_R = 5.5
COLS = 78

# window chrome colors, from each variant's own palette
CHROME = {
    "night": {"bg": "#1a1b26", "bg_dark": "#16161e", "fg_dark": "#a9b1d6", "red": "#f7768e", "yellow": "#e0af68", "green": "#9ece6a"},
    "storm": {"bg": "#24283b", "bg_dark": "#1f2335", "fg_dark": "#a9b1d6", "red": "#f7768e", "yellow": "#e0af68", "green": "#9ece6a"},
    "moon": {"bg": "#222436", "bg_dark": "#1e2030", "fg_dark": "#828bb8", "red": "#ff757f", "yellow": "#ffc777", "green": "#c3e88d"},
    "day": {"bg": "#e1e2e7", "bg_dark": "#d0d5e3", "fg_dark": "#6172b0", "red": "#f52a65", "yellow": "#8c6c3e", "green": "#587539"},
}

# ---------------------------------------------------------------------------
# parse themes/truecolor/tokyonight-<style>.neomuttrc
# ---------------------------------------------------------------------------
def parse_theme(style: str) -> dict[str, tuple[str | None, str | None, tuple[str, ...]]]:
    """Return {object: (fg, bg, attrs)}.

    Plain objects are keyed by name (first definition wins). Pattern-based
    objects (index, header, body, status, attach_headers) are keyed by
    object+pattern, e.g. 'index~N' or 'statusNew:[0-9]+'.
    """
    path = ROOT / "themes" / "truecolor" / f"tokyonight-{style}.neomuttrc"
    out: dict[str, tuple[str | None, str | None, tuple[str, ...]]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(" # ", 1)[0].strip()
        if not line.startswith("color "):
            continue
        tokens = line[len("color "):].split()
        obj = tokens.pop(0)
        attrs = tuple(t for t in tokens if t in ("bold", "underline", "italic", "none", "reverse", "standout"))
        tokens = [t for t in tokens if t not in attrs]
        # neomutt syntax is strictly: color OBJ [attrs] FG BG [pattern]
        fg, bg = tokens[0], tokens[1]
        pattern_tokens = tokens[2:]
        if pattern_tokens:  # a pattern remains → key by object + pattern
            out.setdefault(obj + pattern_tokens[0].strip("'\""), (fg, bg, attrs))
        else:
            out.setdefault(obj, (fg, bg, attrs))
    return out


def st(theme, key: str):
    """Style lookup: exact match, else unique prefix match, else 'normal'."""
    if key in theme:
        return theme[key]
    matches = [v for k, v in theme.items() if k.startswith(key)]
    if len(matches) == 1:
        return matches[0]
    return theme.get("normal", (None, None, ()))


# ---------------------------------------------------------------------------
# the mock screen
#   ("split", sidebar_segments, pane_segments)   sidebar + index
#   ("full",  segments)                          status bar / pager
# ---------------------------------------------------------------------------
def build_rows():
    def sb(text, style, width=SIDEBAR_W):
        return (text.ljust(width)[:width], style)

    rows = []
    rows.append(("split", [sb("  Mailboxes", "sidebar_ordinary")], []))
    rows.append(("split", [sb("  INBOX", "sidebar_spool_file", 15), ("New: 2", "sidebar_new")],
                 [("  1 N  Oct 28  folke       tokyonight v4 is out", "index~N")]))
    rows.append(("split", [sb("  > tokyonight [open]", "sidebar_highlight")],
                 [("  2 N  Oct 28  GitHub      [neomutt] PR #313 merged", "index~N")]))
    rows.append(("split", [sb("  > sent", "sidebar_ordinary")],
                 [("> 3    Oct 27  b1n        Re: theme for neomutt?", "indicator")]))
    rows.append(("split", [sb("  > drafts  !", "sidebar_flagged")],
                 [("  4 !  Oct 26  boss       deploy the theme tonight", "index~F")]))
    rows.append(("split", [sb("  > archive", "sidebar_ordinary")],
                 [("  5 A  Oct 25  mutt-users sidebar colors question", "normal")]))
    rows.append(("split", [sb("  > lists", "sidebar_unread")],
                 [("  6 T  Oct 24  me         palette notes", "index~T")]))

    rows.append(("full", [
        ("tokyonight.neomutt  ", "status"),
        ("Inbox: 6 messages   ", "status"),
        ("New: 2   ", "statusNew:"),
        ("Flag: 1", "statusFlag:"),
    ], []))

    pager = [
        [("From:     Folke Lemaitre <folke@example.com>", "header")],
        [("Subject:  *Tokyo Night* for neomutt", "header")],
        [("Date:     Mon, 27 Oct 2026 23:11:00 +0900", "header")],
        [("", "normal")],
        [("Hi — thanks for shipping ", "normal"), ("truecolor", "search"), (" support!", "normal")],
        [("> Thanks for making this theme!", "quoted")],
        [("> > Have you tried the moon style?", "quoted1")],
        [("Grab it at ", "normal"), ("https://github.com/folke/tokyonight.nvim", "body(https?")],
        [("Ping ", "normal"), ("folke@example.com", "body([\\-"), (" if anything breaks.", "normal")],
        [("-- ", "signature")],
        [("Folke Lemaitre", "signature")],
    ]
    for seg in pager:
        rows.append(("full", seg, []))
    return rows


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render(variant: str) -> str:
    theme = parse_theme(variant)
    chrome = CHROME[variant]
    normal_fg = theme.get("normal", ("#ffffff",))[0] or "#ffffff"
    rows = build_rows()
    height = PAD_Y * 2 + TITLE_H + LINE_H * len(rows)
    width = COLS * CHAR_W + 2 * PAD_X

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" font-family="{esc(FONT)}" font-size="{FONT_SIZE}">'
    )
    # window: title bar on bg_dark, body on the variant's bg
    parts.append(f'<rect width="{width:.0f}" height="{height:.0f}" rx="10" fill="{chrome["bg_dark"]}"/>')
    parts.append(
        f'<path d="M 0 {TITLE_H} H {width:.0f} V {height - 10:.0f} '
        f'Q {width:.0f} {height:.0f} {width - 10:.0f} {height:.0f} H 10 '
        f'Q 0 {height:.0f} 0 {height - 10:.0f} Z" fill="{chrome["bg"]}"/>'
    )
    dot_y = TITLE_H / 2 + 2
    for i, color in enumerate((chrome["red"], chrome["yellow"], chrome["green"])):
        parts.append(f'<circle cx="{PAD_X + i * (DOT_R * 3):.1f}" cy="{dot_y:.1f}" r="{DOT_R}" fill="{color}"/>')
    title = f"neomutt — tokyonight-{variant}"
    parts.append(
        f'<text x="{width / 2:.1f}" y="{dot_y + FONT_SIZE * 0.36:.1f}" text-anchor="middle" '
        f'fill="{chrome["fg_dark"]}">{esc(title)}</text>'
    )

    def draw_segments(segments, x, base_y) -> float:
        for text, key in segments:
            fg, bg, attrs = st(theme, key)
            fg = fg if fg not in (None, "default") else normal_fg
            if bg and bg != "default":
                parts.append(
                    f'<rect x="{x:.1f}" y="{base_y - FONT_SIZE * 0.88:.1f}" '
                    f'width="{len(text) * CHAR_W:.1f}" height="{FONT_SIZE * 1.25:.1f}" fill="{bg}"/>'
                )
            weight = ' font-weight="bold"' if "bold" in attrs else ""
            deco = ' text-decoration="underline"' if "underline" in attrs else ""
            italic = ' font-style="italic"' if "italic" in attrs else ""
            extra = f"{weight}{deco}{italic}"
            # One <text> per glyph at an explicit x: rendering is independent
            # of the viewer's font metrics, so columns line up everywhere.
            for ch in text:
                if ch != " ":
                    parts.append(
                        f'<text x="{x:.1f}" y="{base_y:.1f}" fill="{fg}"{extra} '
                        f'xml:space="preserve">{esc(ch)}</text>'
                    )
                x += CHAR_W
        return x
        return x

    base_top = TITLE_H + PAD_Y + FONT_SIZE
    for i, (kind, *payload) in enumerate(rows):
        base_y = base_top + i * LINE_H
        if kind == "split":
            sb_segs, pane_segs = payload
            draw_segments(sb_segs, PAD_X, base_y)
            draw_segments(pane_segs, PAD_X + SIDEBAR_W * CHAR_W + CHAR_W, base_y)
        else:
            draw_segments(payload[0], PAD_X, base_y)
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for variant in VARIANTS:
        svg = render(variant)
        out = ASSETS / f"preview-{variant}.svg"
        out.write_text(svg, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
