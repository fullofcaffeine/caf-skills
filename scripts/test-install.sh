#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
fixture_root=$(mktemp -d)
trap 'rm -rf "$fixture_root"' EXIT

export CODEX_HOME="$fixture_root/codex"
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

echo "caf-skills installer fixture passed"

export CODEX_HOME="$fixture_root/selective"
"$repo_root/scripts/install.sh" --skill wait-for-completion
"$repo_root/scripts/install.sh" --skill wait-for-completion
[[ -L "$CODEX_HOME/skills/wait-for-completion" ]]
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
