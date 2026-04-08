#!/usr/bin/env python3
import json, sys, subprocess, os
from datetime import datetime

data = json.load(sys.stdin)

# ── Extract data ──
model = data.get("model", {}).get("display_name", "?")
ctx = data.get("context_window", {})
pct_raw = ctx.get("used_percentage", 0) or 0
pct = int(pct_raw)
remaining = int(ctx.get("remaining_percentage", 100) or 100)
ctx_size_full = ctx.get("context_window_size", 200000) or 200000

# Autocompact buffer is ~16.5% of context window — subtract it for real usable space
compact_buffer = int(ctx_size_full * 0.165)
ctx_size = ctx_size_full - compact_buffer

# Context window tokens (derived from percentage — the authoritative source)
# pct_raw is % of full window, recalculate against usable space
ctx_used = int(ctx_size_full * pct_raw / 100)
ctx_left = max(0, ctx_size - ctx_used)

# Recalculate percentage against usable space (excludes autocompact buffer)
usable_pct_raw = (ctx_used / ctx_size * 100) if ctx_size > 0 else 0
usable_pct = min(int(usable_pct_raw), 100)
usable_remaining = max(0, 100 - usable_pct)

# Cumulative session totals (across all API calls, NOT context window)
sess_in = ctx.get("total_input_tokens", 0) or 0
sess_out = ctx.get("total_output_tokens", 0) or 0


def get_git_branch():
    try:
        r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                           capture_output=True, text=True, timeout=1)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""

def short_cwd():
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]
    parts = cwd.split("/")
    if len(parts) > 3:
        cwd = "/".join(parts[:1] + [".."] + parts[-2:])
    return cwd

git_branch = get_git_branch()
cwd = short_cwd()
now = datetime.now().strftime("%I:%M %p").lstrip("0")

# ── Colors ──
RST  = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"
CYAN    = "\033[96m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
ORANGE  = "\033[38;5;208m"
PURPLE  = "\033[38;5;141m"
TEAL    = "\033[38;5;80m"

# ── Theme by usage level (against usable space) ──
if usable_pct >= 90:
    accent = RED; icon = "🔴"
    alert = f" {RED}{BOLD}⚠ CRITICAL {usable_remaining}% LEFT — AUTOCOMPACT SOON{RST}"
elif usable_pct >= 80:
    accent = ORANGE; icon = "🟠"
    alert = f" {ORANGE}⚡{usable_remaining}% left{RST}"
elif usable_pct >= 70:
    accent = YELLOW; icon = "🟡"; alert = ""
elif usable_pct >= 40:
    accent = GREEN; icon = "🟢"; alert = ""
else:
    accent = CYAN; icon = "🔵"; alert = ""

# ── Gradient progress bar ──
bar_width = 20

def grad(pos, w):
    r = pos / max(w - 1, 1)
    if r < 0.4:  return "\033[38;5;51m"
    if r < 0.6:  return "\033[38;5;47m"
    if r < 0.75: return "\033[38;5;226m"
    if r < 0.9:  return "\033[38;5;208m"
    return "\033[38;5;196m"

exact = usable_pct_raw * bar_width / 100
full = int(exact)
part = exact - full
pchars = " ▏▎▍▌▋▊▉█"
pidx = min(int(part * 8), 8)

bar = ""
for i in range(bar_width):
    if i < full:
        bar += f"{grad(i, bar_width)}█"
    elif i == full and full < bar_width:
        bar += f"{grad(i, bar_width)}{pchars[pidx]}"
    else:
        bar += f"{GRAY}░"
bar += RST

# ── Helpers ──
def fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000:     return f"{n/1_000:.1f}K"
    return str(n)

# ── Separator ──
sep = f" {DIM}│{RST} "

# ── Single horizontal line ──
parts = []

# Model + icon
parts.append(f"{icon} {BOLD}{WHITE}{model}{RST}")

# Git branch
if git_branch:
    parts.append(f"{PURPLE} {git_branch}{RST}")

# Progress bar + percentage + context tokens (authoritative from %)
parts.append(f"{bar} {accent}{BOLD}{usable_pct}%{RST} {WHITE}{fmt(ctx_used)}{RST}{DIM}/{fmt(ctx_size)}{RST}")

# Tokens left
parts.append(f"{TEAL}{fmt(ctx_left)}{RST}{DIM} left{RST}")

# Session cumulative totals
parts.append(f"{BLUE}▲{RST}{BLUE}{fmt(sess_in)}{RST}{DIM}in{RST} {MAGENTA}▼{RST}{MAGENTA}{fmt(sess_out)}{RST}{DIM}out{RST}")

# CWD + time
parts.append(f"{DIM}{cwd} {now}{RST}")

# Alert
if alert:
    parts.append(alert)

print(sep.join(parts))
