# ~/.zshrc

# ---------------------------------------------------------------------------
# Powerlevel10k instant prompt. MUST stay at the very top.
# Anything that may write to stdout/stderr or need console input must go ABOVE
# this block; everything else goes below.
# ---------------------------------------------------------------------------
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# ---------------------------------------------------------------------------
# PATH
#
# `typeset -U path` keeps PATH deduplicated (first occurrence wins), which stops
# it from doubling every time a zsh is nested inside another zsh.
# Entries are pruned at the end, so listing something that doesn't exist yet is
# harmless rather than a wasted stat on every command lookup.
# ---------------------------------------------------------------------------
typeset -U path PATH

# JAVA_HOME first, since it feeds into path below.
# 2>/dev/null so a missing JDK can never break the instant prompt.
export JAVA_HOME="$(/usr/libexec/java_home -v 24 2>/dev/null)"

path=(
  "$HOME/.local/bin"                                # claude, codex
  "${ASDF_DATA_DIR:-$HOME/.asdf}/shims"             # asdf-managed runtimes
  "$JAVA_HOME/bin"
  /opt/homebrew/opt/postgresql@16/bin
  /usr/local/bin
  /usr/libexec                                      # java_home, PlistBuddy
  $path                                             # homebrew + system, from .zprofile
)

# Drop entries that aren't existing directories.
path=($^path(N-/))

# ---------------------------------------------------------------------------
# Oh My Zsh
# ---------------------------------------------------------------------------
export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="powerlevel10k/powerlevel10k"

# Update automatically, no prompt.
# `auto` is used rather than the default `prompt` because prompt mode only
# records that it asked when you answer y/n/Enter -- dismissing it any other
# way leaves the timer unset, so the blocking network `git ls-remote` re-fires
# on EVERY new shell (~220ms). auto always writes the timer, so the network
# check happens once per 13 days (default) instead. Tune with:
#   zstyle ':omz:update' frequency <days>
# Note: when an update lands, oh-my-zsh re-execs this shell.
zstyle ':omz:update' mode auto

plugins=(
    git
    history
    dirhistory
    encode64
    jsontools
    zsh-autosuggestions
    zsh-syntax-highlighting   # must stay last
)

source "$ZSH/oh-my-zsh.sh"

# ---------------------------------------------------------------------------
# Build flags (homebrew keg-only deps)
# ---------------------------------------------------------------------------
export LDFLAGS="-L/opt/homebrew/opt/postgresql@16/lib -L/opt/homebrew/opt/libyaml/lib -L/opt/homebrew/opt/openssl@3/lib"
export CPPFLAGS="-I/opt/homebrew/opt/postgresql@16/include -I/opt/homebrew/opt/libyaml/include -I/opt/homebrew/opt/openssl@3/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/postgresql@16/lib/pkgconfig:/opt/homebrew/opt/libyaml/lib/pkgconfig:/opt/homebrew/opt/openssl@3/lib/pkgconfig"

# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------
HISTSIZE=50000
SAVEHIST=50000          # was 10000, so 80% of in-memory history was discarded

# ---------------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------------
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1

# ---------------------------------------------------------------------------
# Prompt config
# ---------------------------------------------------------------------------
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
