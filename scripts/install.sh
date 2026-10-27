#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
codex_root=${CODEX_HOME:-"$HOME/.codex"}
# Claude Code reads skills from its config directory; CLAUDE_CONFIG_DIR overrides it.
claude_root=${CLAUDE_CONFIG_DIR:-"$HOME/.claude"}
install_agents=0
selected_skill=""

if [[ $# -eq 2 && $1 == "--skill" ]]; then
  selected_skill=$2
  if [[ ! $selected_skill =~ ^[a-z0-9][a-z0-9-]*$ || ! -f "$repo_root/skills/$selected_skill/SKILL.md" ]]; then
    echo "unknown or invalid skill: $selected_skill" >&2
    exit 2
  fi
elif [[ ${1:-} == "--global-agents" ]]; then
  install_agents=1
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--global-agents | --skill NAME]" >&2
  exit 2
fi

mkdir -p "$codex_root/skills"

link_owned_path() {
  local source=$1
  local destination=$2
  if [[ -L "$destination" && $(readlink "$destination") == "$source" ]]; then
    echo "already linked: $destination"
  elif [[ -e "$destination" || -L "$destination" ]]; then
    echo "refusing to replace existing path: $destination" >&2
    exit 1
  else
    ln -s "$source" "$destination"
    echo "linked: $destination -> $source"
  fi
}

# Links the generated Claude Code projection of one skill when it exists.
link_claude_skill() {
  local source="$repo_root/claude-code/$1"
  [[ -f "$source/SKILL.md" ]] || return 0
  mkdir -p "$claude_root/skills"
  link_owned_path "$source" "$claude_root/skills/$1"
}

if [[ -n "$selected_skill" ]]; then
  link_owned_path "$repo_root/skills/$selected_skill" "$codex_root/skills/$selected_skill"
  link_claude_skill "$selected_skill"
  exit 0
fi

for source in "$repo_root"/skills/*; do
  [[ -f "$source/SKILL.md" ]] || continue
  destination="$codex_root/skills/$(basename "$source")"
  link_owned_path "$source" "$destination"
done

link_owned_path "$repo_root/skills/README.md" "$codex_root/skills/README.md"

for source in "$repo_root"/claude-code/*; do
  [[ -f "$source/SKILL.md" ]] || continue
  link_claude_skill "$(basename "$source")"
done

if [[ $install_agents -eq 1 ]]; then
  destination="$codex_root/AGENTS.md"
  source="$repo_root/AGENTS.md"
  link_owned_path "$source" "$destination"
fi
