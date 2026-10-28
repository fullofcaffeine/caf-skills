---
name: beads
description: "Use Beads (`bd`) safely for durable issue tracking, dependencies, blockers, handoff, shared memory, and cross-agent shared-library coordination. Trigger in any repository containing `.beads`, when asked to find, claim, create, update, close, migrate, synchronize, or recover Beads work, when an important change affects a reusable library with several consumers, or when Beads reports a client/database schema mismatch. Prefer repository pins or wrappers and always perform a read-only compatibility preflight before writes."
license: "Apache-2.0"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:48ebef3a4d17c58a36728d8125508b4a6db55d46863e05d8b74b072a5b662d1f. Selection digest: sha256:a83562d44ceb4040307a1e3cbf34058e2b73013da2dbd9ea4ad52516eb4a0cce. Effective AgentSpec digest: sha256:8cdb0428b726bbc028d8116638d86393734d5a0f368059f27f8758cbcf64fe5d -->

# Beads

Use Beads as the durable source of truth for work that must survive an agent or
session. Use the repository's reviewed wrapper or `bd-toolchain` pin. Never let
shell `PATH` order decide which database client opens shared issue data.

## Use Beads as the durable task record

## Identify the target first

Name the repository that owns the issues before each command. When operating on
another repository, pass that directory explicitly:

```bash
bd -C /path/to/repository ready
```

`-C` selects both the repository pin and the database. Do not run plain `bd`
from repository x when repository y owns the intended record.

## Mandatory compatibility preflight

Run the repository's documented Beads wrapper when one exists. Otherwise run
this preflight from the target repository before its first Beads operation and
before the first write after compaction or handoff:

```bash
command -v bd
bd-toolchain check
bd --readonly info --json
```

Continue only when the toolchain check verifies the pinned executable and the
read-only database open succeeds without schema skew.

For a pinned fresh checkout with no database, `bd-toolchain check` can report
`readonly_preflight=not-applicable:no-database`. Run only the repository's
documented `bd bootstrap --yes` recovery or `bd init` command next. The ordinary
read-only preflight applies after that one creation operation.

If `bd-toolchain` is unavailable and the repository has not adopted it, follow
the repository's stricter wrapper or pin. At minimum run:

```bash
command -v bd
bd version
bd --readonly info --json
```

Use only that reviewed executable for the session. Do not use
`--ignore-schema-skew` for writes.

## Missing pin or client

Treat a missing `.beads-toolchain` file or unavailable pinned client as a
toolchain problem. Do not choose a nearby binary.

1. Read the repository's agent instructions and toolchain documentation.
2. Identify the reviewed client revision, checksum, and expected schema.
3. Add those reviewed bytes with `bd-toolchain add`.
4. If authorized, record the pin with `bd-toolchain use ID --repository DIR`.
5. Run `bd-toolchain check --repository DIR` before a database write.

Pinning writes only `.beads-toolchain`. It must not create or migrate the
database. Never select a client only because it can read the current schema.

## Linked worktrees that predate repository tooling

A linked worktree can share a Git repository while its branch predates the
reviewed Beads wrapper. Do not bypass hooks or use an ambient client.

Resolve the primary worktree from Git's common directory:

```bash
common_dir=$(git rev-parse --git-common-dir)
case "$common_dir" in
  /*) ;;
  *) common_dir=$(cd "$common_dir" && pwd -P) ;;
esac
primary_root=$(cd "$common_dir/.." && pwd -P)
```

Use the reviewed wrapper from `primary_root` when repository instructions name
one. Otherwise use the primary repository pin and pass the database owner with
`bd -C`. Require the ordinary read-only preflight before each first write.

## Normal issue workflow

After the preflight, run `bd prime` and follow the live repository guidance:

```bash
bd prime
bd ready --json
bd show ISSUE --json
bd update ISSUE --claim --json
bd create "Short title" \
  --description="Why this exists and what completion requires" \
  --type=task --priority=2 --json
bd close ISSUE --reason="Completed" --json
```

Prefer non-interactive commands and JSON output. Never use `bd edit`. Do not
close unfinished work or create a Markdown checklist as a competing tracker.
Use `bd remember` only for small keyed knowledge that later `bd prime` calls
must inject. A memory value is mutable and is not an append-only activity log.

Use repository-owned synchronization wrappers. Do not treat
`.beads/issues.jsonl` as the database, run `bd import` during ordinary sync, or
call a raw Dolt push when the repository requires a guarded wrapper.

## Shared-library coordination channel

Use a coordination channel when a repository owns a library, compiler,
framework, schema, generated contract, toolchain, or adapter consumed by more
than one project. Read the channel before substantial work that can change a
public seam or duplicate another consumer's upstream work.

The channel is discovery history. It does not own tasks, branches, pull
requests, source, releases, or permission to edit another agent's work.

### Locate the channel

Run the target repository's Beads preflight. Then search the live database:

```bash
bd list --label coordination:shared-library-history --all --json
```

Require zero or one current channel. If several records have the current
label, stop and reconcile them. Do not guess from titles or stale exports.

When a current channel exists:

1. Read its complete description, notes, links, and comments.
2. Follow every entry relevant to the proposed public seam.
3. Inspect each cited task, pull request, branch, commit, and handoff state.
4. Treat a stale intent entry as a lead. Verify its current task and PR state.

An absent channel does not prove that no related work exists. Continue with
source, history, task, and pull-request checks.

### Classify the channel as non-actionable

Prefer a repository-defined non-actionable record type when one exists.
Otherwise use this portable Beads shape:

- type: `decision`.
- status: `deferred`.
- labels: `coordination:shared-library-history`, `non-actionable`.
- no assignee and no claim.
- no dependency edge that blocks product or library work.

Do not create the channel as a task, feature, bug, chore, or epic. Do not close
it after one change. The deferred status keeps it out of `bd ready`. Use
`relates-to` links for referenced work instead of blocking dependencies.

Create a channel only when the repository is shared, no current channel exists,
and the user or repository policy authorizes the write. Use the same reviewed
client and verify the created record through a fresh read.

### Append intent and outcome entries

Use comments because they are durable, timestamped, and append-only:

```bash
bd comments CHANNEL --json
bd comments add CHANNEL "ENTRY"
```

Append an `intent` entry after the real task is selected and before substantial
implementation or a public upstream proposal. Append another entry when the
state materially changes.

Use this compact record:

```text
state: intent | progress | handoff | landed | abandoned | superseded
agent: <stable agent role or id>
task: <authoritative task ref>
scope: <public seams or behavior affected>
consumers: <known affected consumers>
refs: <branch, PR, commit, CML, design, or evidence refs>
summary: <what is planned, proved, deferred, or transferred>
next: <owner and exact next action, when one exists>
```

Do not add a comment for every local edit. Add one when another consumer can
otherwise duplicate work or depend on an obsolete seam. Never store secrets,
private reasoning, raw transcripts, credentials, or unreviewed personal data.

If comments become expensive to review, create one related successor. Move the
canonical label to the successor, label the old record
`coordination:shared-library-history-archive`, and add bidirectional pointers.
Keep only one current channel.

### Preserve authority boundaries

- The live task owns task status and assignment.
- The pull request records branch ownership and review handoff.
- Git records implementation history.
- Provider and runtime systems own their mutable facts.
- The coordination channel makes these owners discoverable.

When Caf/CML is available, accepted CML can describe the policy, stable refs,
scope, and expected relationships. A Caf graph can project the links. Neither
CML nor the graph replaces current Beads comments, Git history, or PR state.

## Recover a client/schema mismatch

When the read-only open reports different client and database schemas:

1. Stop all Beads writes.
2. Preserve the error, repository path, client path and version, pin, and both
   schema numbers.
3. Inspect the repository's reviewed pin before checking a newer release.
4. Build any candidate in isolation.
5. Test the candidate only with read-only `info` and `ready` calls.
6. Update or import a client only with explicit authority.
7. Repeat the normal preflight.

Do not downgrade or hand-edit migration records, copy a database backward,
implicitly migrate, or use a temporary source build for writes.

## Explicit migrations

Treat a schema upgrade as a separate coordinated project. Identify one
authoritative clone, back up the database and a semantic export, inspect every
migration, run the explicit migration, verify issue and dependency parity,
publish the database, and update every participating repository pin.

An ordinary issue command must never be the first operation by a newer client.

## Handoff

Follow `bd prime` at completion. Update or close only the issue that the agent
owns. Append the shared-library channel outcome when another consumer needs the
result. Run required gates, inspect Git status, and report unsynchronized work.
Supporting documents and local plans do not replace the Beads lifecycle record.

Reason: Task data shared by several agents must not depend on shell PATH order or the caller's directory, so every command names its client and target.

Examples:
- A session ends with open work. Record status and the next action in the existing issue before stopping.
- An agent works in a second repository. Run bd -C with that repository's path instead of relying on the current directory.

Limits:
- Do not copy task state into Markdown plans or memory files.
- Do not let shell PATH order choose the Beads client.

Authority boundary: This skill guides writing and review only. It grants no source write, tool, provider, task, or effect authority.
