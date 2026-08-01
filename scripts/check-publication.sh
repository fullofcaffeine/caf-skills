#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
mode=${1:-}

files=()
if [[ -d "$repo_root/.git" && "$mode" == "--all" ]]; then
  while IFS= read -r -d '' file; do files+=("$repo_root/$file"); done < <(git -C "$repo_root" ls-files -z)
elif [[ ! -d "$repo_root/.git" ]]; then
  while IFS= read -r -d '' file; do files+=("$file"); done < <(find "$repo_root" -path "$repo_root/.git" -prune -o -type f -print0)
else
  while IFS= read -r -d '' file; do files+=("$repo_root/$file"); done < <(git -C "$repo_root" diff --cached --name-only --diff-filter=ACMR -z)
fi

if [[ ${#files[@]} -eq 0 ]]; then
  exit 0
fi

bad=0
for file in "${files[@]}"; do
  relative=${file#"$repo_root"/}
  case "$relative" in
    backups/*|.audit/*|decisions.tsv|*.zip|*.tar|*.tar.gz|repomix-output*)
      echo "publication-safety: forbidden artifact: $relative" >&2
      bad=1
      ;;
  esac
  case "$(basename "$relative" | tr '[:upper:]' '[:lower:]')" in
    .env|.env.local|.env.production|.npmrc|.pypirc|.netrc|auth.json|credentials|credentials.json)
      echo "publication-safety: secret-bearing filename: $relative" >&2
      bad=1
      ;;
  esac
done

if [[ -n "${HOME:-}" ]]; then
  for file in "${files[@]}"; do
    if grep -nF -- "$HOME" "$file"; then
      echo "publication-safety: machine-local home path found in ${file#"$repo_root"/}" >&2
      bad=1
    fi
  done
fi

if [[ $bad -ne 0 ]]; then
  exit 1
fi

echo "publication-safety: passed (${#files[@]} files checked)"
