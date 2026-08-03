#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
codex_root=${CODEX_HOME:-"$HOME/.codex"}
install_agents=0

if [[ ${1:-} == "--global-agents" ]]; then
  install_agents=1
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--global-agents]" >&2
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

for source in "$repo_root"/skills/*; do
  [[ -f "$source/SKILL.md" ]] || continue
  destination="$codex_root/skills/$(basename "$source")"
  link_owned_path "$source" "$destination"
done

link_owned_path "$repo_root/skills/README.md" "$codex_root/skills/README.md"

if [[ $install_agents -eq 1 ]]; then
  destination="$codex_root/AGENTS.md"
  source="$repo_root/AGENTS.md"
  link_owned_path "$source" "$destination"
fi
