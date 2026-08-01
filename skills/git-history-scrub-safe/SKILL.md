---
name: "git-history-scrub-safe"
description: "Safely remove sensitive strings or path leaks from Git history with verified backups, isolated mirror rewrite, integrity checks, rollback, and protected-branch-aware push strategy. Use when any tracked or historical commit contains secrets, machine-local paths, tokens, or private identifiers that must be scrubbed."
---

# Git History Scrub Safety

## Overview
Use this workflow to scrub sensitive content from Git history without risking irreversible repo damage.
Always treat history rewrite as a production migration: backup first, rewrite in isolation, verify, then push with branch-protection awareness.
Default promotion model: **keep `main` untouched until scrub is proven**, publish rewrite to `main_scrubbed`, validate, then atomically promote `main_scrubbed` to `main`.

## Workflow
1. Inventory the leak scope.
2. Create two backups.
3. Rewrite in an isolated mirror clone.
4. Verify integrity and leak removal.
5. Publish scrubbed history to `main_scrubbed` first.
6. Validate remote `main_scrubbed` state.
7. Promote `main_scrubbed` to `main` (with archival of old `main`).
8. Validate remote state.
9. Document recovery and follow-ups.

## Step 1: Inventory leak scope
- Identify exact leaked patterns and where they appear:
  - `git log --all -S'<literal>' --oneline`
  - `git grep -n '<literal>' $(git rev-list --all)` only when needed (can be expensive).
- Classify patterns before rewriting:
  - `exact literals` (preferred)
  - `generic regex patterns` (use narrowly)
- Avoid broad replacements unless necessary.

## Step 2: Create backups (mandatory)
Create both backups before rewriting any history:
- Full ref backup bundle:
  - `git bundle create ../repo-pre-scrub-<timestamp>.bundle --all`
- Working tree archive:
  - `tar -czf ../repo-working-tree-pre-scrub-<timestamp>.tgz --exclude=.git -C .. <repo-dir>`
- Record backup paths in the run notes.

## Step 3: Rewrite in isolated mirror clone
- Clone as mirror (all refs/tags):
  - `git clone --mirror <origin-url> /tmp/<repo>-scrub-<timestamp>.git`
- Build replace rules file (`literal==>replacement` and optional `regex:` rules).
- Run rewrite:
  - `git filter-repo --force --replace-text /tmp/<rules>.txt`
- Never rewrite directly in the main working repo.

## Step 4: Verify before any push
Run all of these inside the mirror clone:
- Integrity:
  - `git fsck --full`
- Leak checks:
  - `git log --all -S'<original-literal>' --oneline | wc -l`
  - Repeat for every target pattern.
- Spot-check replacement presence where expected.
- Confirm ref inventory remains plausible:
  - `git show-ref | wc -l`

## Step 5: Staged publish strategy (branch-protection aware)
- Check branch protection/push rules first.
- Do **not** touch `main` yet.
- Push rewritten branch first:
  - `git push --force-with-lease origin <rewritten-main-ref>:refs/heads/main_scrubbed`
- If force is blocked for new branch updates, coordinate admin policy first.
- Do not push hidden refs (e.g., `refs/pull/*`).

## Step 6: Validate `main_scrubbed` before promotion
- Verify remote refs:
  - `git ls-remote origin refs/heads/main refs/heads/main_scrubbed`
- Re-clone mirror and verify scrub/integrity against `main_scrubbed`:
  - `git clone --mirror <origin-url> /tmp/<repo>-post-scrub-check.git`
  - `cd /tmp/<repo>-post-scrub-check.git`
  - `git fsck --full`
  - `git log main_scrubbed -S'<leak>' --oneline | wc -l` (must be `0`)
- Run CI on `main_scrubbed` (or temporary PR target) and require green status.

## Step 7: Promote scrubbed branch to main
- Archive old main first:
  - `git push origin refs/heads/main:refs/heads/recovery/main-pre-scrub-<timestamp>`
- Promote scrubbed:
  - `git push --force-with-lease origin refs/heads/main_scrubbed:refs/heads/main`
- Optional cleanup after confirmation:
  - keep `main_scrubbed` for a cooling period, then delete if desired.

## Step 8: Rollback plan (prepared before promotion)
If anything goes wrong, restore from bundle via mirror:
1. `git clone --mirror ../repo-pre-scrub-<timestamp>.bundle /tmp/<repo>-restore.git`
2. `cd /tmp/<repo>-restore.git`
3. `git remote set-url origin <origin-url>`
4. `git push --force --mirror origin`

## Step 9: Post-promotion validation
- Verify remote default branch SHA and critical tags:
  - `git ls-remote origin refs/heads/main refs/tags/<tag>`
- Re-run leak checks against remote mirror clone.
- Run CI guard/test subset relevant to touched docs/scripts.
- Announce rewrite impact to collaborators:
  - everyone must re-clone or hard-reset local clones.

## Safety rules
- Never skip backups.
- Never run destructive history rewrite on primary working clone.
- Never attempt partial recovery guesses; restore from backup if uncertain.
- Prefer precise literal replacements over broad regex.
- Keep a machine-readable run log (commands + outcomes + timestamps).
- Never resolve rewritten-history divergence by merging unrelated histories into `main`.
  Promotion must be ref replacement (`main_scrubbed -> main`), not history stitching.

## Resources
- Use `references/runbook.md` as the execution checklist.
- Use `references/prompt-template.md` to run this workflow in another repo.
