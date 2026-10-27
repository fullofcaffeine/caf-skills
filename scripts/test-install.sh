#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
fixture_root=$(mktemp -d)
trap 'rm -rf "$fixture_root"' EXIT

export CODEX_HOME="$fixture_root/codex"
export CLAUDE_CONFIG_DIR="$fixture_root/claude"
"$repo_root/scripts/install.sh"
"$repo_root/scripts/install.sh"

for source in "$repo_root"/skills/*; do
  [[ -f "$source/SKILL.md" ]] || continue
  destination="$CODEX_HOME/skills/$(basename "$source")"
  [[ -L "$destination" ]]
  [[ $(readlink "$destination") == "$source" ]]
done

[[ -L "$CODEX_HOME/skills/README.md" ]]
[[ $(readlink "$CODEX_HOME/skills/README.md") == "$repo_root/skills/README.md" ]]
[[ ! -e "$CODEX_HOME/skills/oracle-review" ]]

for source in "$repo_root"/claude-code/*; do
  [[ -f "$source/SKILL.md" ]] || continue
  destination="$CLAUDE_CONFIG_DIR/skills/$(basename "$source")"
  [[ -L "$destination" ]]
  [[ $(readlink "$destination") == "$source" ]]
done
[[ ! -e "$CLAUDE_CONFIG_DIR/skills/README.md" ]]

echo "caf-skills installer fixture passed"

export CODEX_HOME="$fixture_root/selective"
export CLAUDE_CONFIG_DIR="$fixture_root/selective-claude"
"$repo_root/scripts/install.sh" --skill wait-for-completion
"$repo_root/scripts/install.sh" --skill wait-for-completion
[[ -L "$CODEX_HOME/skills/wait-for-completion" ]]
[[ -L "$CLAUDE_CONFIG_DIR/skills/wait-for-completion" ]]
[[ ! -e "$CLAUDE_CONFIG_DIR/skills/simple-english" ]]
[[ ! -e "$CODEX_HOME/skills/README.md" ]]
[[ ! -e "$CODEX_HOME/skills/calibrate-reasoning-effort" ]]
if "$repo_root/scripts/install.sh" --skill ../escape; then
  echo "invalid skill name was accepted" >&2
  exit 1
fi
mkdir "$CODEX_HOME/skills/keep-it-simple"
if "$repo_root/scripts/install.sh" --skill keep-it-simple; then
  echo "existing installation was replaced" >&2
  exit 1
fi
[[ -d "$CODEX_HOME/skills/keep-it-simple" && ! -L "$CODEX_HOME/skills/keep-it-simple" ]]
echo "selective installation preserves unrelated entries and refuses replacement"
