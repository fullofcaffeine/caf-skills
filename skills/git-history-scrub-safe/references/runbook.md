# History Scrub Runbook

## 1. Preflight
- Confirm remote URL and default branch.
- Confirm whether default branch allows force-push.
- Enumerate target literals/regexes.

## 2. Backups
- `git bundle create ../repo-pre-scrub-<ts>.bundle --all`
- `tar -czf ../repo-working-tree-pre-scrub-<ts>.tgz --exclude=.git -C .. <repo-dir>`

## 3. Isolated rewrite
- `git clone --mirror <origin-url> /tmp/<repo>-scrub-<ts>.git`
- Prepare `replace-text` rules file.
- `git filter-repo --force --replace-text /tmp/<rules>.txt`

## 4. Verification (local mirror)
- `git fsck --full`
- `git log --all -S'<leak>' --oneline | wc -l` for each leak
- `git show-ref | wc -l`

## 5. Publish to `main_scrubbed` first
- `git push --force-with-lease origin <rewritten-main-ref>:refs/heads/main_scrubbed`

## 6. Validate remote `main_scrubbed`
- `git ls-remote origin refs/heads/main refs/heads/main_scrubbed`
- Mirror-check remote:
  - `git clone --mirror <origin-url> /tmp/<repo>-post-scrub-check.git`
  - `git -C /tmp/<repo>-post-scrub-check.git fsck --full`
  - `git -C /tmp/<repo>-post-scrub-check.git log main_scrubbed -S'<leak>' --oneline | wc -l` (must be 0)

## 7. Promote to `main`
- Archive old main:
  - `git push origin refs/heads/main:refs/heads/recovery/main-pre-scrub-<ts>`
- Promote scrubbed branch:
  - `git push --force-with-lease origin refs/heads/main_scrubbed:refs/heads/main`

## 8. Rollback (if needed)
- `git clone --mirror ../repo-pre-scrub-<ts>.bundle /tmp/<repo>-restore.git`
- `cd /tmp/<repo>-restore.git`
- `git remote set-url origin <origin-url>`
- `git push --force --mirror origin`

## 9. Post-checks
- `git ls-remote origin refs/heads/main refs/tags/<tag>`
- Re-run leak search against remote mirror clone.
- Announce history rewrite and required local reset/reclone instructions.

## Hard safety rule
- Never merge unrelated histories to reconcile rewritten vs old `main`.
  Use branch promotion (`main_scrubbed` -> `main`) only.
