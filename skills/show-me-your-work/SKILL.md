---
name: show-me-your-work
description: "Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away. Independent review is risk-based, not automatic."
---

# Show me your work

For work a human reviews after the fact, a decision trail lets them reconstruct what was decided, why, and on what evidence, without rerunning the work or reading the whole transcript. Keep one canonical log so the trail is consistent and a future agent can find it.

## The format

A single TSV file, one row per decision. TSV because GitHub renders it as a sortable table, `column -s$'\t' -t` and spreadsheets read it, and a row appends with one command. Cells stay single-line. Evidence is a pointer, not prose.

Copy `references/decision-log-template.tsv` (the header row) to start a clean log. Columns:

- **ts.** ISO8601 timestamp. The timeline axis.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words. If a principle drove it, say it plainly (`explored options first, this was a one-way door`), not as a jargon tag.
- **evidence.** A link or path that proves it: commit SHA, PR number, `file:line`, or an artifact, trace, or screenshot path. Never a paragraph.
- **result.** The outcome or predicate state: `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open`.

An example, plain-spoken so a reviewer reads it at a glance. This is illustration only; don't copy these rows into a real log.

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Logging a row

Write each entry the way you'd tell a teammate what you did. Plain words, concrete actions, no AI speak or abstract jargon (the **unslop** skill applies to log text too). A reviewer should understand each row without decoding it.

Use the helper so rows stay well-formed: `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`. It stamps `ts`, writes the header on first use, strips stray tabs/newlines, and prefixes any cell starting with `=`, `+`, `-`, or `@` with a single quote so a reviewer opening the log in a spreadsheet doesn't trigger formula execution. A bare `printf` appending a row works too, but mind those same bytes if cells come from generated or user-supplied text.

Log decision points and checkpoints, not every action: a fork chosen, a unit completed with its verification result, a pivot or revert with its trigger, a blocker surfaced, a gate fixed. For loop runs, one row per iteration. Skip the trivial and self-evident.

## Where it lives

By default the log is a working artifact, not committed. Keep it at `decisions.tsv` in the work dir, or `.audit/<task-slug>.tsv` when several efforts run at once, and leave it out of git. Most work doesn't need a committed trail; the local log still keeps the run honest and can be discarded after.

Commit it only when the work is ambitious enough that a reviewer needs the trail to trust the result: a large cross-language port, a multi-week migration, anything where confidence has to be shown rather than assumed. A committed log renders as a table in the PR.

## Rules

- One row is one decision or checkpoint. If it doesn't fit on one line, the decision isn't crisp yet.
- Append-only. A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence produced by committed scripts over hand-made one-offs, so a reviewer can re-run it (the **encode-lessons-in-structure** principle skill).

## Audit the log against the transcript

At the end of the run, before handing back, check the log told the truth. Read this run's transcript under the active workspace's `agent-transcripts/` directory (the system prompt names the path). Don't glob across `~/.cursor/projects/*/`; that reads unrelated private chats. Walk the log against what actually happened:

- Every row maps to a real action. Cut invented or aspirational entries.
- Each row's evidence resolves and shows what the row claims.
- A fork, pivot, or abandoned approach that shaped the work but isn't logged is a gap. Add it.
- Drop padding. If nobody would audit a row, it doesn't earn its place.

Fix the log, not the story. If the work diverged from what a row claims, the row is wrong.

## Decide whether independent review is worth it

A trail does not automatically require a subagent review. For routine, bounded,
reversible work with decisive focused checks, finish with the main agent's log
self-audit. Do not spawn a reviewer or add an `Attention` footer merely because
a trail exists, the run was long, many files changed, or extra confidence would
be nice.

Require an independent review when at least one of these is true:

- The user explicitly asks for an independent review.
- A repository rule, active task label, or another selected skill requires one.
- The work changes security or authorization boundaries, release admission or
  public compatibility claims, provenance, destructive data migrations,
  irreversible external state, or similarly consequential policy.
- A plausible wrong result could survive the available tests because evidence
  is contradictory, the oracle is weak, or the implementation and verification
  share the same risky assumption.
- A long unattended run contains consequential judgment calls that the user
  cannot cheaply reconstruct from the trail and artifacts.

Do not treat these as sufficient reasons on their own:

- documentation or formatting changes;
- a mechanical refactor with a deterministic checker and cheap rollback;
- elapsed time, diff size, row count, task prestige, or green CI;
- the generic possibility that another agent might notice something.

Before spawning, compare the review's likely marginal safety value with its
token, latency, and coordination cost. Prefer focused tests, invariant checks,
or a bounded main-agent second pass when they answer the actual risk more
directly. If the task's governing reasoning policy calls for a second pass but
does not require a separate agent, a deliberate main-agent pass is sufficient.

When review is justified, use the lowest effective reviewer effort. Use a fresh
Sol context and `high` for a bounded but subtle implementation review; use
`xhigh` for release, security, provenance, migration, broad compatibility, or
other high-consequence evidence; use `max` only when a miss would be unusually
expensive and tightly coupled. Never use a stronger setting just because it is
available.

Give the reviewer a compact packet: the request and acceptance criteria, trail
path, transcript path when exposed, relevant diff or artifacts, verification
results, and the concrete risks to check. Do not pass the intended verdict. Ask
the reviewer to flag weak evidence, skipped checks, risky choices, and material
gaps—not to redo the whole task.

Only when an independent review actually ran, end the final reply with an
`Attention` section. Name the model and list material flags or `No flags`. When
no review ran, do not claim one and do not add an empty review footer.

## Optional Oracle planning and review

Use `$oracle-review` only when the task independently meets that skill's high
threshold: the work is genuinely critical and also unusually hard, materially
undefined, non-convergent, disputed by consequential evidence, or in need of a
slower higher-quality challenge. Oracle may clarify and plan before
implementation or independently review a plan or completed result. A generic
review, a slow review, a large task, or a desire for extra confidence is not
enough.

Oracle does not automatically require a preliminary Sol review, and this skill
does not automatically trigger Oracle. When an ordinary review already exists
and its gap motivates escalation, include that report, this trail, the relevant
diff, verification evidence, and the known gap. Let caf-oracle own prompts,
bundles, dispatch state, replies, and dispositions; add trail rows only for the
escalation decision, request identity/status, and reconciled outcome. Do not
claim planning or review closure until the response is reconciled against
repository evidence. Let `$oracle-review` own its threshold, automation,
recovery, reconciliation, and archive format.

## Reviewing the trail

Read top to bottom, follow the evidence pointers, spot-check. GitHub renders a committed TSV as a table; `column -s$'\t' -t decisions.tsv` renders it in a terminal. A row whose evidence doesn't resolve, or whose result is unverified, is the audit catching a gap.

## Composing this skill

Other skills route their audit trail here instead of inventing one. Reference it by name and let it own the format; don't restate the columns.
