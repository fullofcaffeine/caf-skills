---
name: caf-work-loop
description: "Use when the owner asks to keep working until the Beads backlog or the Caf vision is done, to run unattended or in a loop, to continue autonomously, or to coordinate a swarm of agents on Cafetera or Caffeine tasks. Also use at the start of each loop iteration to choose the next task, and before committing, parking, delegating, or stopping."
license: "LicenseRef-Cafetera-Private-Unpublished"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:2cab4bc8194f2f7985b56a9308a146a0a375d9ecc803807cc646758c958a4339. Selection digest: sha256:d2b941569679f9206a7c8bde04c5f24781cb86596adc38bfdd6592f4ad5086a1. Effective AgentSpec digest: sha256:dac0b5af8e6c3cfef706e0ee143effc47657a5d553714c5886b364ac46bcb1a7 -->

# Caf work loop

Keep the owner's Cafetera and Caffeine backlogs moving toward the vision in AGENTS.md without supervision, one verified task at a time, while every decision that belongs to the owner waits for the owner.

## Run the unattended Caf work loop

### Choose one task

1. List ready and in-progress work in each attended repository: `bd ready` and `bd list --status=in_progress` in Cafetera, and `bd -C ../caffeine ready` for Caffeine. Read each repository's own `AGENTS.md` before working in it.
2. Prefer finishing an in-progress task assigned to this agent. Otherwise take the highest-priority ready task that is unassigned or assigned to this agent's role.
3. A task assigned to another agent role is eligible only when the owner has asked for that workstream and its Beads history shows no update in the last 24 hours. Never take over a task that another live session is updating.
4. Confirm the work is still needed against current source, history, tests, and open reviews before claiming it. Claim it with `bd update <id> --claim`.

### Do the work

Follow the repository's `AGENTS.md`: CML first, a failing test first, the smallest complete change, beginner-readable HxDoc, and the repository formatter. Record failed reuse and new gaps as Beads tasks instead of widening the current task.

Decide from Caf knowledge first: find the existing piece with `caf situation`, `caf help`, and `caf kb`. When none fits, propose the smallest new piece at the right rung on a branch, with tests. Journal each loop event (intent, decision, claim with evidence, question, blocker) with `caf note --task ID`.

At session start, `./bin/caf situation` prints the workspace, the selected policies, the catalog commands, and the open focus tasks in about ten lines.

Before you use a `caf` command, run `./bin/caf help --json` in Cafetera. It prints one JSON catalog of every command path with its purpose, options, examples, mode, action, and declared effects. Do not guess commands or flags. The catalog grants no effect; the host's effect policy still decides each run.

Before you write CML, run `./bin/caf help cml`: it first shows which tag to start with for a request such as a skill, a KB note, a workspace, a CLI command, or an approval, where the file goes, and which worked example to read, then lists every tag. Run `./bin/caf help cml <tag>` to see the tag's attributes and types, enum values in the `{Enum.Value}` form, what goes inside it, which tags it fits inside, and its worked example; `--json` prints the whole catalog. Do not guess tags or attributes.

### Verify, commit, and push

1. Run the focused suite for the change.
2. Copy exactly the change into a clean sibling worktree under the same parent directory as the repository, without the owner's unrelated uncommitted files. Run the complete gate there (`./bin/check` in Cafetera).
3. When the CLI bytes change, update every recorded CLI digest pin in the same change.
4. One review and one passing gate is the normal path. Both name the exact commit that reaches the target branch. Rerun them only when their evidence is stale, such as after a new commit.
5. Commit with a Conventional Commit message after the gate passes and the staged diff equals the gated worktree diff. Push reviewed, gated work yourself in Cafetera, F12E, and Caffeine, except a range that touches approval-bearing paths (`caf/locks/**`, `caf/agents/**`, `caf/policies/**`, `scripts/hooks/**`, `.beads/hooks/**`): the owner merges and pushes that range. Never force-push, deploy, or publish unless the owner asks.
6. After the commit reaches the checkout that the installed `caf` points to, run `./bin/install-caf` there. It rebuilds the CLI and writes the generated `.claude/CLAUDE.md`, so the installed `caf` never lags the main branch.
7. Before handoff, verify the merged result once on the exact commit. Close the task with the commit, commands, and results as evidence.

### Park what belongs to the owner

Do not guess. Record the exact question in the task notes, leave the task open, and continue with another eligible task when the work needs any of these:

- an owner decision about scope, wording, priority, or a drifted copy;
- accepting an approval record or a policy re-pin: prepare it on a branch; the owner accepts an approval record with `caf approve RECIPE --accept --proposal D`, or merges and pushes a policy re-pin; never run `--accept` or pass `--i-am-the-owner`;
- a push of an approval-bearing range, a license, a deploy, or a publication;
- a destructive or credential-related action;
- changes outside the attended repositories.

Reach the owner through the harness permission prompt where supported; otherwise give one exact command. Never freeze unrelated merges to keep an owner command applicable.

### Review deeply with Fable or Oracle

Send architecture decisions, broad reviews, and non-converging work to an independent reviewer: a Fable subagent, or Oracle through the oracle-review skill when it can receive enough exact context. Check every load-bearing claim against current source before acting on it, and track each confirmed tension as a Beads task.

### Coordinate a swarm

The orchestrator runs on Fable or Opus. It owns task selection, integration, and every commit to the main branch. Give each worker exactly one claimed task, one isolated worktree, the exact inputs and acceptance, and a stopping condition. Keep competing writers in separate worktrees, serialize integration, and gate the integrated result again. Keep the swarm small; add a worker only when independent tasks make the total work cheaper or safer. A worker's report is evidence to verify, not acceptance.

### Stop and report

Stop when no eligible task remains, when two consecutive iterations fail the gate for the same reason, or when the owner's pending decisions block all remaining work. End every iteration with two lines: what was done (commit and task) and what is next. While a long gate runs, wait for its completion notification instead of polling.

Reason: An unattended loop is only safe when task choice, verification, commits, and owner decisions follow the same written rules in every harness and every iteration.

Examples:
- The gate fails twice for the same unrelated stage. Stop the loop and report the failing stage and its evidence instead of retrying.
- The ready list holds a P0 measurement task and a P1 task that needs a license approval. Take the measurement task, and record the license question in the other task's notes.
- Two independent tasks are ready. The orchestrator gives each worker one task and one worktree, then integrates and gates the combined result before one commit at a time.

Limits:
- No claim that a worker's report is accepted work before the integrated gate passes.
- No push of an approval-bearing range, deploy, publication, pull request, credential change, or destructive action without the owner.
- No takeover of a task another live session is updating.

Authority boundary: This skill organizes task selection, verification, and coordination. It grants no repository, task, provider, credential, publication, or effect authority beyond what the owner and each repository already allow.
