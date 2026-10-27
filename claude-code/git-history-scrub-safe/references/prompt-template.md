# Prompt Template: Safe History Scrub

Use this prompt in another repo:

```text
Run a safe git history scrub for this repository.

Requirements:
1) Discover and list all commits/refs containing these sensitive patterns:
   - <PATTERN_1>
   - <PATTERN_2>
2) Create mandatory backups first:
   - full git bundle (--all)
   - working tree archive
3) Perform rewrite only in an isolated mirror clone using git-filter-repo replace-text rules.
4) Verify integrity and scrub success before any push:
   - git fsck --full
   - zero hits for target patterns via git log -S
5) Use staged promotion:
   - push rewritten history to `main_scrubbed` first
   - validate remote `main_scrubbed`
   - only then promote `main_scrubbed` to `main`
6) Archive old `main` to `recovery/main-pre-scrub-<ts>` before promotion.
7) Never merge unrelated histories as a recovery strategy.
8) If force push is blocked, stop and provide exact admin actions required.
9) Provide rollback commands from backup bundle.
10) Provide a final report with:
   - backup file paths
   - rewritten refs
   - verification outputs
   - any residual risks.

Be extremely careful and do not skip safety checks.
```
