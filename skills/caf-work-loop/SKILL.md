---
name: caf-work-loop
description: "Use when the owner asks to keep working until the Beads backlog or the Caf vision is done, to run unattended or in a loop, to continue autonomously, or to coordinate a swarm of agents on Cafetera or Caffeine tasks. Also use at the start of each loop iteration to choose the next task, and before committing, parking, delegating, or stopping."
license: "LicenseRef-Cafetera-Private-Unpublished"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:7eff69afdaa37434122369374c971e6637224be8f33650c898179c1cc4fd7c4b. Selection digest: sha256:ecbf267e91204d0cad7c0131fca3435e6047f89ec12673b0fbf134614ca7f38d. Effective AgentSpec digest: sha256:b3aaff32fc9c29f7b33f381ca3a6579b7a8bc1875920eb834298601d6db81644 -->

# Caf work loop

Keep the owner's Cafetera and Caffeine backlogs moving toward the vision in AGENTS.md without supervision, one verified task at a time, while every decision that belongs to the owner waits for the owner.

## Run the unattended Caf work loop

## Choose one task

1. List ready and in-progress work in each attended repository: `bd ready` and `bd list --status=in_progress` in Cafetera, and `bd -C ../caffeine ready` for Caffeine. Read each repository's own `AGENTS.md` before working in it.
2. Prefer finishing an in-progress task assigned to this agent. Otherwise take the highest-priority ready task that is unassigned or assigned to this agent's role.
3. A task assigned to another agent role is eligible only when the owner has asked for that workstream and its Beads history shows no update in the last 24 hours. Never take over a task that another live session is updating.
4. Confirm the work is still needed against current source, history, tests, and open reviews before claiming it. Claim it with `bd update <id> --claim`.

## Do the work

Follow the repository's `AGENTS.md`: CML first, a failing test first, the smallest complete change, beginner-readable HxDoc, and the repository formatter. Record failed reuse and new gaps as Beads tasks instead of widening the current task.

## Verify before committing

1. Run the focused suite for the change.
2. Copy exactly the change into a clean sibling worktree under the same parent directory as the repository, without the owner's unrelated uncommitted files. Run the complete gate there (`./bin/check` in Cafetera).
3. When the CLI bytes change, update every recorded CLI digest pin in the same change.
4. Commit locally with a Conventional Commit message only after the gate passes and the staged diff equals the gated worktree diff. Never push, force, publish, or open a pull request unless the owner asks.
5. Close the task with the commit, commands, and results as evidence.

## Park what belongs to the owner

Do not guess. Record the exact question in the task notes, leave the task open, and continue with another eligible task when the work needs any of these:

- an owner decision about scope, wording, priority, or a drifted copy;
- a license, publication, or repository-policy approval;
- a destructive, outward-facing, or credential-related action;
- changes outside the attended repositories.

## Review deeply with Fable or Oracle

Send architecture decisions, broad reviews, and non-converging work to an independent reviewer: a Fable subagent, or Oracle through the oracle-review skill when it can receive enough exact context. Check every load-bearing claim against current source before acting on it, and track each confirmed tension as a Beads task.

## Coordinate a swarm

The orchestrator runs on Fable or Opus. It owns task selection, integration, and every commit to the main branch. Give each worker exactly one claimed task, one isolated worktree, the exact inputs and acceptance, and a stopping condition. Keep competing writers in separate worktrees, serialize integration, and gate the integrated result again. Keep the swarm small; add a worker only when independent tasks make the total work cheaper or safer. A worker's report is evidence to verify, not acceptance.

## Stop and report

Stop when no eligible task remains, when two consecutive iterations fail the gate for the same reason, or when the owner's pending decisions block all remaining work. End every iteration with two lines: what was done (commit and task) and what is next. While a long gate runs, wait for its completion notification instead of polling.

Reason: An unattended loop is only safe when task choice, verification, commits, and owner decisions follow the same written rules in every harness and every iteration.

Examples:
- The gate fails twice for the same unrelated stage. Stop the loop and report the failing stage and its evidence instead of retrying.
- The ready list holds a P0 measurement task and a P1 task that needs a license approval. Take the measurement task, and record the license question in the other task's notes.
- Two independent tasks are ready. The orchestrator gives each worker one task and one worktree, then integrates and gates the combined result before one commit at a time.

Limits:
- No claim that a worker's report is accepted work before the integrated gate passes.
- No push, publication, pull request, credential change, or destructive action without the owner.
- No takeover of a task another live session is updating.

Authority boundary: This skill organizes task selection, verification, and coordination. It grants no repository, task, provider, credential, publication, or effect authority beyond what the owner and each repository already allow.
