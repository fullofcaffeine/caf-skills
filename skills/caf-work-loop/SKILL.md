---
name: caf-work-loop
description: "Use when the owner asks to keep working until the Beads backlog or the Caf vision is done, to run unattended or in a loop, to continue autonomously, or to coordinate a swarm of agents on Cafetera or Caffeine tasks. Also use at the start of each loop iteration to choose the next task, and before committing, parking, delegating, or stopping."
license: "LicenseRef-Cafetera-Private-Unpublished"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:7d58ea3b61e35e9ef7fbd353e8bd53a1b98b6c285509431a01b11c9f233578b6. Selection digest: sha256:c2440263459139b4c1f8b2045867c0bdc48dafc82c70726f4add59690f5f8535. Effective AgentSpec digest: sha256:b14e133477d5934029c6e7aebd08d1ea0ed631de335579e3d36d4002e04a8803 -->

# Caf work loop

Keep the owner's Cafetera and Caffeine backlogs moving toward the vision in AGENTS.md without supervision, one verified task at a time, while every decision that belongs to the owner waits for the owner.

## Run the unattended Caf work loop

The owner's loop prompt names the goal (an epic and its plan) and the session facts. Session facts are, for example, the task order, the worker limit, and the dev-server ports. This skill owns every lasting loop rule. If the prompt and this skill disagree about a lasting rule, follow the prompt for this session, name the conflict in the iteration summary, and record one `cafetera-0jpj` task to move the change into this skill.

### Choose one task

1. List ready and in-progress work in each attended repository: `bd ready` and `bd list --status=in_progress` in Cafetera, and `bd -C ../caffeine ready` for Caffeine. Read each repository's own `AGENTS.md` before working in it.
2. Follow the task order in the plan that the prompt names. Prefer finishing an in-progress task assigned to this agent. Otherwise take the highest-priority ready task that is unassigned or assigned to this agent's role.
3. A task assigned to another agent role is eligible only when all three hold: the owner asked for that workstream, its Beads history shows no update in the last 24 hours, and no live session is updating it. Check the Beads comments and, for Caf work, `caf activity list --task <id>`.
4. Confirm the work is still needed against current source, history, tests, and open reviews before you claim or take over a task. Claim an unassigned task or a task of your own with `bd update <id> --claim`.
5. To take over an eligible task, run `bd update <id> --assignee <your agent id>`; a comment alone leaves the old owner in `bd ready`. Write one Beads comment with: the previous owner and their last update date; the branch and commits you reuse; the items you leave untouched; the checks already run; the open questions (`caf:agentspec:rule:cafetera-agent:exact-cross-repository-handoff`). Write one journal note. Then claim it with `bd update <id> --claim`.

### Do the work

Follow the repository's `AGENTS.md`: CML first, a failing test first, the smallest complete change, beginner-readable HxDoc, and the repository formatter. Record failed reuse and new gaps as Beads tasks instead of widening the current task.

For every step, find the existing Caf piece first and use it (`caf:agentspec:rule:caf-knowledge-first`). When none fits, extend Caf with the smallest piece at the right rung on a branch, with tests and the run that needed it (`caf:agentspec:rule:scoped-self-extension`). Turn each friction into a Caf default, such as refusal text, a `Next:` hint, a default record, or a task under the friction epic `cafetera-0jpj`. Never keep it only in a memory file (`caf:agentspec:rule:owner-prompt-to-default`). Take business facts from CML records and defaults; do not ask the owner for them.

Journal every decision, review verdict, worker handoff, merge, and friction with `caf note --task <loop epic>` (`caf:agentspec:rule:loop-journal`). Keep each long report, such as a review, at `.caf/evidence/<loop epic>/<sha256>.md`, and name that digest in the note.

At session start, `./bin/caf situation` prints the workspace, the selected policies, the catalog commands, and the open focus tasks in about ten lines.

Before you use a `caf` command, run `./bin/caf help --json` in Cafetera. It prints one JSON catalog of every command path with its purpose, options, examples, mode, action, and declared effects. Do not guess commands or flags. The catalog grants no effect; the host's effect policy still decides each run.

Before you write CML, run `./bin/caf help cml`: it first shows which tag to start with for a request such as a skill, a KB note, a workspace, a CLI command, or an approval, where the file goes, and which worked example to read, then lists every tag. Run `./bin/caf help cml <tag>` to see the tag's attributes and types, enum values in the `{Enum.Value}` form, what goes inside it, which tags it fits inside, and its worked example; `--json` prints the whole catalog. Do not guess tags or attributes.

### Review, verify, commit, and push

1. Workers run only the focused lanes for what they changed. After a rebase that changes only pins, run `./bin/update-pins --check` and the affected lanes.
2. Each task gets one independent review on its exact commit, then its fixes (`caf:agentspec:rule:review-gate-and-stop`). Start the verdict note with the verdict (approved, changes requested, or inconclusive) and the commit.
3. The coordinator integrates one task at a time: rebase the worker branch, then merge it fast-forward only into the local main branch. Each task gets exactly one complete gate on the integrated commit. Never run two gates at once. `pgrep -f 'bin/chec[k]$|check(\.js)? ru[n]|check-bootstra[p]'` shows a running gate.
4. In Cafetera, the installed CLI holds a compiled copy of the check plan. So first rebuild it from the integrated commit: run `PATH=$(dirname $(command -v lix)):$PATH ./bin/install-caf` in the checkout that the installed `caf` points to. Then run the gate as `caf check run` from that repository root, and read its exit code as the gate result. Make it the whole background command. You may redirect its output to a file, but never add `;`, `echo`, or a pipe, because then the shell reports a different exit code. Read the exit code in the completion notice. Each stage keeps its output and a Receipt under `build/caf/check/runs/`. Use `./bin/check` instead when the change touches `haxe_libraries/`, because only `./bin/check` runs `lix download`. Also use `./bin/check` when the installed CLI cannot be rebuilt from the gated commit, for example in a worktree whose commit the installed `caf` was not built from.
5. When the CLI bytes change, update every recorded CLI digest pin in the same change.
6. Commit with a Conventional Commit message. Push reviewed, gated work yourself in Cafetera, F12E, and Caffeine. A range that touches approval-bearing paths (`caf/locks/**`, `caf/agents/**`, `caf/policies/**`, `scripts/hooks/**`, `.beads/hooks/**`) goes through the owner push prompt: run `caf push-approval-paths` as one plain command. Never force-push, deploy, or publish unless the owner asks.
7. After each merge, run `scripts/hooks/beads-export.sh sync`. The `./bin/install-caf` run in step 4 also writes the generated `.claude/CLAUDE.md`, so the installed `caf` never lags the main branch.
8. Before handoff, verify the merged result once on the exact commit. Close the task with the commit, commands, and results as evidence.

### Park what belongs to the owner

The owner wants report-only operation. Do every step that you can and may do yourself (`caf:agentspec:rule:act-dont-ask`). Do not guess. Record the exact question in the task notes, leave the task open, and continue with another eligible task when the work needs any of these:

- an owner decision about scope, wording, priority, or a drifted copy;
- accepting an approval record or a policy re-pin: prepare it on a branch. Only the owner accepts it (`caf:agentspec:rule:owner-only-approval`). Never accept it yourself and never pass `--i-am-the-owner`;
- a merge of approval-record or policy wording, or a push of an approval-bearing range;
- an outward effect, such as a license, a new repository, DNS, a deploy, or a publication;
- a destructive or credential-related action;
- a harness or permission refusal: never work around it, and never edit harness settings such as `~/.claude/settings.json`;
- changes outside the attended repositories.

Put all owner items into one message, with one exact command for each. Reach the owner through the harness permission prompt where supported. Never freeze unrelated merges to keep an owner command applicable.

### Review deeply with Fable or Oracle

Send architecture decisions, broad reviews, and non-converging work to an independent reviewer: a Fable subagent, or Oracle through the oracle-review skill when it can receive enough exact context. Check every load-bearing claim against current source before acting on it, and track each confirmed tension as a Beads task.

### Coordinate a swarm

Any capable model can coordinate. The coordinator owns task selection, integration, and every commit to the main branch. Give each worker exactly one claimed task, one isolated worktree, the exact inputs and acceptance, and a stopping condition (`caf:agentspec:rule:cafetera-agent:bounded-worker-delegation`). Keep competing writers in separate worktrees, serialize integration, and gate the integrated result again. Keep the swarm small and within the worker limit in the prompt. Add a worker only when independent tasks make the total work cheaper or safer. A worker's report is evidence to verify, not acceptance.

### Stop and report

Stop when no eligible task remains, when two consecutive iterations fail the gate for the same reason, or when everything left needs the owner. End every iteration with two lines: what was done (commit and task) and what is next. While a long gate runs, wait for its completion notification instead of polling.

Reason: An unattended loop is only safe when task choice, verification, commits, and owner decisions follow the same written rules in every harness and every iteration.

Examples:
- The gate fails twice for the same unrelated stage. Stop the loop and report the failing stage and its evidence instead of retrying.
- The owner asked for the calendar workstream. A ready calendar task is assigned to another agent that has not updated it in three days, and no session is working on it. Set yourself as its assignee with `bd update ID --assignee`, write one handoff comment, and write one journal note before you work on it.
- The ready list holds a P0 measurement task and a P1 task that needs a license approval. Take the measurement task, and record the license question in the other task's notes.
- Two independent tasks are ready. The coordinator gives each worker one task and one worktree, then integrates and gates the combined result before one commit at a time.

Limits:
- No claim that a worker's report is accepted work before the integrated gate passes.
- No push of an approval-bearing range, deploy, publication, pull request, credential change, or destructive action without the owner.
- No takeover of a task another live session is updating.

Authority boundary: This skill organizes task selection, verification, and coordination. It grants no repository, task, provider, credential, publication, or effect authority beyond what the owner and each repository already allow.
