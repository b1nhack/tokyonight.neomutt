# tokyonight.neomutt

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![NeoMutt](https://img.shields.io/badge/NeoMutt-2021--02--05%2B-blue.svg)](https://neomutt.org/)
[![Variants](https://img.shields.io/badge/variants-4-7aa2f7.svg)](#变体)

[English](README.md) | **简体中文**

**[Tokyo Night](https://github.com/folke/tokyonight.nvim) 的 [NeoMutt](https://neomutt.org/) 主题。**

四种配色 —— `night`、`storm`、`moon`、`day` —— 自 folke 的 tokyonight.nvim 移植，覆盖 **NeoMutt 文档记载的全部配色对象**：index、pager、sidebar、compose、引用文本、正文标记、状态栏计数器。

<p align="center">
  <img src="assets/preview-night.svg" alt="Tokyo Night night 预览" width="760">
</p>

| storm | moon | day |
| :---: | :---: | :---: |
| ![storm 预览](assets/preview-storm.svg) | ![moon 预览](assets/preview-moon.svg) | ![day 预览](assets/preview-day.svg) |

## 特性

- **完整覆盖** —— 全部 55 个可配色对象，对照 NeoMutt 的对象注册表（`color/commands.c` 里的 `ColorFields`）逐一核实并用真实二进制测试：`sidebar_*`（9 个）、`compose_*`（5 个）、引用 0–9 级、index 逐列颜色、`attach_headers`、`warning`/`message`/`prompt`/`options`、`italic`、帮助页斑马纹（`stripe_even`/`stripe_odd`——手册的表格里都还没收录它们）、状态栏计数器高亮（`New: 2`、`Flag: 1`……）。
- **两种色深变体** —— 256 色版在任何终端都能用；truecolor 版使用精确调色板。
- **即插即用** —— 对象集合与流行的 catppuccin/neomutt 主题同构（并且是其超集），切换只需改一行。
- **确定性生成** —— 全部文件由单一调色板定义生成（`scripts/generate_themes.py`），各变体永不漂移。

## 环境要求

| 变体 | 需要 |
| :-- | :-- |
| `themes/*.neomuttrc`（256 色） | 任意 NeoMutt、任意终端 |
| `themes/truecolor/*.neomuttrc` | NeoMutt ≥ 2021-02-05、truecolor 终端，**且** TERM 的 terminfo 宣告 16M 色 |

### truecolor 的坑（务必阅读）

NeoMutt 接受 `#RRGGBB` 颜色的前提是**两条同时满足**：

1. `set color_directcolor = yes`（truecolor 主题文件已替你设置），**且**
2. curses 的 `COLORS`（来自 terminfo）为 16 777 216 —— 即 `TERM` 类似 `xterm-direct`；`xterm-256color` 是**不行**的。

缺任何一条，启动时都会看到其中一种报错：

```text
Direct colors support disabled: color normal #c0caf5 default   ← 缺 (1)
color normal #c0caf5 default: color not supported by term      ← 缺 (2)
```

注意 NeoMutt **不看** `$COLORTERM=truecolor`。如果改不了 `TERM`（ssh、tmux 场景），直接用 256 色版即可——那是精心挑选的近似色，观感依然在线。

## 安装

### 方式一 —— 安装脚本

```zsh
git clone git@github.com:b1nhack/tokyonight.neomutt.git
cd tokyonight.neomutt
./install.sh night               # night | storm | moon | day
./install.sh --truecolor night   # 精确色板变体
```

四种变体都会复制到 `~/.config/neomutt/`（truecolor 版在 `truecolor/` 子目录里），以后切换无需重装。安装脚本会打印你所选变体对应的准确 `source` 行。

### 方式二 —— 手动

```zsh
mkdir -p ~/.config/neomutt
cp themes/tokyonight-night.neomuttrc ~/.config/neomutt/
```

然后在 `neomuttrc` 里加：

```muttrc
source ~/.config/neomutt/tokyonight-night.neomuttrc
```

### 切换变体

source 不同的文件即可，后 source 的生效：

```muttrc
source ~/.config/neomutt/tokyonight-night.neomuttrc
# source ~/.config/neomutt/tokyonight-storm.neomuttrc
```

## 变体

| 主题 | 背景色 | 适用场景 |
| :-- | :-- | :-- |
| `tokyonight-night` | `#1a1b26` | 默认款：干净、深邃的暗蓝夜色 |
| `tokyonight-storm` | `#24283b` | 更柔和的蓝灰风暴 |
| `tokyonight-moon` | `#222436` | 饱和度更高的「月光」色 |
| `tokyonight-day` | `#e1e2e7` | 浅色变体，适合明亮环境 |

## 颜色映射

NeoMutt 对象与 tokyonight.nvim 调色板 token 的对应（night 色值；其余变体替换为对应 token）：

| NeoMutt 对象 | token | night |
| :-- | :-- | --: |
| `normal` | 前景色 | `#c0caf5` |
| `error` | red | `#f7768e` |
| `warning` | yellow | `#e0af68` |
| `message` | green | `#9ece6a` |
| `options`、`attachment` | magenta | `#bb9af7` |
| `prompt`、`compose_header` | blue + 粗体 | `#7aa2f7` |
| `progress` | blue 于 `bg_highlight` 上 | `#7aa2f7` / `#292e42` |
| `status` | `fg_dark`；计数器：`New:` 绿、`Del:`/`Flag:` 红、`Post:` 黄 | `#a9b1d6` |
| `indicator` | 前景于 `bg_highlight` 上 | `#c0caf5` / `#292e42` |
| `tree`、`index_tree` | `fg_dark` | `#a9b1d6` |
| `tilde`、`signature` | comment | `#565f89` |
| `markers` | orange | `#ff9e64` |
| `hdrdefault` | `fg_dark` | `#a9b1d6` |
| `header` | blue（标签视为标题） | `#7aa2f7` |
| `attach_headers` | `dark5` | `#737aa2` |
| `search` | 前景于 `bg_search` 上 | — / `#3d59a1` |
| `bold`、`underline`、`italic` | 前景 + 对应属性 | `#c0caf5` |
| `stripe_even` / `stripe_odd`（帮助页） | 透明 / `bg_dark` | — / `#16161e` |
| `index ~N`（新邮件） | green | `#9ece6a` |
| `index ~F`（星标）、`~D`（待删） | red | `#f7768e` |
| `index ~T`（已标记） | magenta | `#bb9af7` |
| `index_number`、`index_size` | `dark3` | `#545c7e` |
| `index_date` | comment | `#565f89` |
| `index_flags` | orange | `#ff9e64` |
| `index_collapsed` | yellow | `#e0af68` |
| `index_label` | magenta | `#bb9af7` |
| `index_tags`、`index_tag` | `green1` | `#73daca` |
| `index_author` | blue，仅作用于无旗标色的行 | `#7aa2f7` |
| `index_subject` | 前景，仅作用于无旗标色的行 | `#c0caf5` |
| `sidebar_background` | `fg_dark` 于 `bg_dark` 上 | `#a9b1d6` / `#16161e` |
| `sidebar_divider` | `bg_highlight` | `#292e42` |
| `sidebar_highlight` | 前景于 `bg_highlight` 上 | `#c0caf5` / `#292e42` |
| `sidebar_indicator` | blue | `#7aa2f7` |
| `sidebar_new` / `sidebar_unread` / `sidebar_flagged` | green / yellow / red | `#9ece6a` / `#e0af68` / `#f7768e` |
| `sidebar_ordinary` | `dark5` | `#737aa2` |
| `sidebar_spool_file` | teal | `#1abc9c` |
| `compose_security_none` / `_sign` / `_encrypt` / `_both` | `dark5` / cyan / blue / `green1` | — |
| `quoted` | `fg_dark`；往下依次 cyan、`blue5`、comment、`dark5`、`dark3`… | `#a9b1d6` |
| `body` —— 邮箱地址与 URL | teal（NeoMutt 的链接色） | `#1abc9c` |
| `body` —— `*粗体*` / `_下划线_` / `/斜体/` | `blue5` + 对应属性 | `#89ddff` |

几个有意为之的选择，写给想改的人：

- **`index_author` / `index_subject` 使用补集模式 `!(~N|~F|~T|~D)`** —— 逐列颜色会叠加在整行颜色之上，无条件给这两列着色会冲淡整行的旗标色。补集模式让它们只在没有旗标色的行上着色：既拿到逐列样式，又保住「新邮件是绿色」的经典效果。
- 背景几乎全部使用 `default`（透明），主题能自然适配你的终端背景；只有 `indicator`、`search`、`progress`、斑马纹和 sidebar 自带底色。

## 自定义

主题文件就是普通 muttrc，直接改完重新 source 即可。几个常用追加：

```muttrc
# 给未读邮件的作者列上色
color index_author magenta default "~N"

# 给整条状态栏上底色
color status default #292e42
```

用 `uncolor` 恢复默认：

```muttrc
uncolor index "~N"      # 去掉绿色的新邮件整行
uncolor body *          # 去掉全部正文正则
```

## 重新生成主题与预览

```zsh
python3 scripts/generate_themes.py    # 从调色板渲染 themes/
python3 scripts/generate_previews.py  # 从 themes/truecolor/ 渲染 assets/
```

## 致谢与许可

- 调色板：[folke/tokyonight.nvim](https://github.com/folke/tokyonight.nvim) —— Apache License 2.0，已注明出处（见 [LICENSE](LICENSE)）。
- 主题结构受 [catppuccin/neomutt](https://github.com/catppuccin/neomutt) 启发，并扩展到全对象覆盖。
- 本仓库代码：MIT。
