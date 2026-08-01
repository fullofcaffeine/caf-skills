---
name: oracle-review
description: Prepare and reconcile rare, manual GPT-5.6 Pro (Oracle) reviews for exceptionally complex architecture, security, provenance, migration, release, or non-converging engineering work. Use when local xhigh/max investigation still leaves consequential competing designs, repeated attempts do not produce a stable invariant, or a critical completed task's normal independent review is demonstrably incomplete. Do not use for routine debugging, ordinary red tests, large-but-bounded changes, or generic requests for extra confidence.
---

# Oracle review

Use GPT-5.6 Pro as a slow, human-mediated architecture and review escalation.
Treat its response as technical evidence, never as repository authority or a
replacement for implementation, tests, CI, owner decisions, or the normal
`show-me-your-work` reviewer.

## Enforce the threshold

Require an Oracle review only when at least one condition is concrete:

- A high-consequence architecture, security, provenance, migration, release,
  or cross-repository semantic decision still has multiple defensible designs
  after an xhigh/max local investigation.
- Two materially different attempts or ready-then-reopened cycles have exposed
  new semantic categories without producing a stable invariant or safe seam.
- Evidence or reviewers disagree in a way that can plausibly authorize an
  incorrect critical release or completion claim.
- A completed critical task's normal `show-me-your-work` reviewer failed to
  inspect required evidence, missed a known counterexample, or returned generic
  conclusions that cannot support closure.

Do not escalate merely because a diff is large, a gate is red, work is slow or
tedious, the code is unfamiliar, or another opinion might be interesting. For
ordinary work, inspect the repository, reduce the failure, and run focused
tests. When the threshold is crossed, say why, stop disputed implementation,
and wait for the response or an explicit smaller-scope waiver.

## Prepare a request

1. Run the status command before creating anything:

   ```sh
   python3 <skill-dir>/scripts/oracle_request.py status --project-root "$PWD"
   ```

   Tell the user about every pending request for this project. If a pasted
   response could match several requests, ask which request ID it belongs to.

2. Initialize a request:

   ```sh
   python3 <skill-dir>/scripts/oracle_request.py init \
     --project-root "$PWD" \
     --task <short-slug> \
     --purpose architecture
   ```

   Use `--purpose non-convergence` or `--purpose critical-review` when that is
   the actual trigger. `init` refuses to hide an existing pending request;
   acknowledge it and pass `--allow-pending` only when a second request is
   genuinely distinct.

3. Read `references/prompt-template.md` and
   `references/request-spec.md`. Fill the generated `PROMPT.md` and
   `request.local.json`. Use a whole primary-repository pack when the safe seam
   is unknown across several subsystems. Use exact selective paths for bounded
   questions and reference repositories. Prefer one XML per repository.

4. Prepare the upload:

   ```sh
   python3 <skill-dir>/scripts/oracle_request.py prepare --request <request-dir>
   ```

   The command pins Repomix, preserves line numbers, verifies the requested
   inventory, checks for file races and secrets, records revisions/diffs and
   hashes, and writes `bundle.zip`. Do not bypass a failed completeness or
   security check. Git-state metadata and patches are limited to the selected,
   non-omitted paths; selective packs never disclose unrelated working-tree
   names or content. `MANIFEST.json` and `SOURCE_INVENTORY.tsv` are entries inside
   the ZIP, not loose request-directory files. Inspect them and the listing
   before handoff, for example with `unzip -p <bundle.zip> MANIFEST.json`,
   `unzip -p <bundle.zip> SOURCE_INVENTORY.tsv`, and `unzip -l <bundle.zip>`.

5. Give the user the exact ZIP path and ask them to upload it to GPT-5.6 Pro,
   paste `PROMPT.md`, and return the complete response here. Never upload,
   automate the browser, call a paid API, or silently substitute another model.

## Reconcile and archive

When the user pastes the response:

1. Match it to a pending request and save it verbatim as
   `ORACLE_RESPONSE.md` in that request directory.
2. Reproduce every material claim against the current repository. Classify it
   as retained, rejected, deferred, or requiring an owner decision. Record
   that analysis in `DISPOSITION.md`, including proving tests and evidence
   gaps. Request a new Oracle pass only when the task still depends on approval
   of a materially changed revision.
3. Record the durable outcome in the project's tracker, decision log, or review
   document when one exists. `/tmp` is not durable project history.
4. Archive only after both files are non-empty:

   ```sh
   python3 <skill-dir>/scripts/oracle_request.py archive --request <request-dir>
   ```

The archive moves to `/tmp/oracle/archived/<project>/<request-id>/`. Never
delete or overwrite an existing request.

## Compose with show-me-your-work

Run the normal fresh-context Sol reviewer first. Oracle is an additional gate
only for a critical task and only when concrete review inadequacy remains. Put
the original request, decision trail, ordinary reviewer report, relevant diff,
verification evidence, and known missed case in the Oracle packet. Do not use
Oracle merely because the first reviewer found no issues.
