#!/usr/bin/env zsh
# tokyonight.neomutt — install a Tokyo Night theme for NeoMutt.
#
# Usage:
#   ./install.sh [--truecolor] [night|storm|moon|day]
#
# Copies the theme files into ~/.config/neomutt/ and prints the `source`
# line to add to your neomuttrc.

emulate -LR zsh
setopt err_exit no_unset pipefail

local script_dir=${0:A:h}
local -a variants=(night storm moon day)

local usage="usage: ./install.sh [--truecolor] [night|storm|moon|day]"

local truecolor=false
if [[ $1 == --truecolor ]]; then
  truecolor=true
  shift
fi

local variant=${1:-night}
if [[ ${variants[(Ie)$variant]} -eq 0 ]]; then
  print -u2 "tokyonight.neomutt: unknown variant '$variant'"
  print -u2 $usage
  exit 1
fi

local src="$script_dir/themes/tokyonight-$variant.neomuttrc"
$truecolor && src="$script_dir/themes/truecolor/tokyonight-$variant.neomuttrc"
[[ -r $src ]] || { print -u2 "tokyonight.neomutt: cannot read $src"; exit 1 }

local dest="${XDG_CONFIG_HOME:-$HOME/.config}/neomutt"
command mkdir -p "$dest"

local file
for file in "$script_dir"/themes/*.neomuttrc; do
  command cp -v "$file" "$dest/$file:t"
done
if $truecolor; then
  command mkdir -p "$dest/truecolor"
  for file in "$script_dir"/themes/truecolor/*.neomuttrc; do
    command cp -v "$file" "$dest/truecolor/$file:t"
  done
fi

local name="tokyonight-$variant.neomuttrc"
print "Installed to $dest."
print "Add this line to your neomuttrc:"
if $truecolor; then
  print "  source ${dest}/truecolor/${name}"
else
  print "  source ${dest}/${name}"
fi
if $truecolor; then
  print
  print "Reminder: the truecolor variant needs 'set color_directcolor = yes' (included"
  print "in the theme file) AND a TERM whose terminfo advertises 16M colors, e.g. xterm-direct."
  print "See the README for the full matrix."
fi