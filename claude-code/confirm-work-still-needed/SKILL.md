---
name: confirm-work-still-needed
description: "Verify that a tracked task, bug, roadmap item, audit finding, pull request, shared-library proposal, or suggested next priority is unresolved and available before recommending, claiming, planning, or implementing it. Use with Beads, GitHub Issues, Linear, TODO lists, audits, Oracle reviews, release reports, open PR queues, older handoffs, and reusable dependencies where another consumer or agent can already own overlapping work."
license: "Apache-2.0"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:f9fd1d161db8d2e453f5ee16e3836799cd07c19437ef02c78566eda8e13a4db7. Selection digest: sha256:a83562d44ceb4040307a1e3cbf34058e2b73013da2dbd9ea4ad52516eb4a0cce. Effective AgentSpec digest: sha256:1836fb439d9c7a94acceb790aa0b98f0fff74a9316ff5b8aef5cda95dfd27d2c -->

# Confirm Work Still Needed

Treat an open tracker item as a lead, not proof that implementation is missing.
Confirm the gap against current source, history, tests, remote review state, and
shared-library coordination records before creating a branch or recommendation.

## Confirm the work is still needed before claiming it

## Verification workflow

1. Read the complete work item. Include its acceptance criteria, design, notes,
   dependencies, timestamps, and external links. Record the exact missing or
   broken behavior.
2. Identify the repository that owns the behavior. Identify every named
   reusable dependency or shared library that can own part of the change.
3. Establish the current baseline without changing it. Inspect repository
   status, current and remote revisions, recent merges, and relevant open pull
   requests. Fetch remote metadata when it can be stale and the fetch is safe.
4. Inspect each relevant pull request's description, comments, branch, review
   history, originating agent, and handoff state.
5. Search current source, tests, workflows, and documentation for the exact
   failure signature and acceptance invariant. Prefer diagnostics, commands,
   API names, emitted tokens, and policy wording over a title-only search.
6. Trace path history and use `git log -S` or `git log -G` for the invariant.
   Identify associated commits and merged pull requests.
7. Run the smallest faithful, non-publishing check that distinguishes “still
   broken” from “already fixed.” Do not run a full suite only to establish that
   a task exists.
8. Classify the item before acting:

   - **Confirmed unresolved:** current source or a focused reproduction shows
     the gap.
   - **Partially resolved:** some criteria landed. Rewrite the task around the
     exact remainder.
   - **Already resolved:** current behavior, tests, and history identify the
     fixing commit or pull request.
   - **Invalidated:** current architecture or product rules make the old
     request inapplicable.
   - **Unknown:** decisive evidence needs external state or another experiment.

9. Take the matching action:

   - For confirmed work, report the evidence and then claim or plan it.
   - For partial work, update the tracker before implementation.
   - For resolved work, do not create duplicate code or a duplicate PR. Update
     or close the stale item when authorized.
   - For invalidated or unknown work, preserve the evidence and request the
     smallest decision or experiment.

## Shared-library duplication preflight

Use this preflight when the proposed work changes a reusable library, compiler,
framework, schema, generated contract, toolchain, or adapter with several
consumers.

1. Use `$beads` in the owner repository. Complete its client and database
   compatibility preflight.
2. List records with the current label
   `coordination:shared-library-history`.
3. Read the complete current channel and every relevant archived successor or
   predecessor that it links.
4. Follow relevant task, PR, branch, commit, design, CML, and consumer refs.
5. Inspect known consumer work named by repository instructions, dependency
   locks, manifests, or channel entries. Do not scan unrelated sibling folders.
6. Compare behavior and ownership. Similar names alone do not prove overlap.

A channel `intent` entry is not a permanent lock. Verify that its task, branch,
or PR is still active. A missing channel is not proof that work is absent.
Continue the ordinary source, history, tracker, and PR checks.

Before implementation, append an intent entry through `$beads` when the
repository policy authorizes it. After landing, handoff, abandonment, or
supersession, append the matching outcome. The authoritative task and PR retain
ownership.

## Agent-owned pull requests

An open PR prepared by another active agent is not unclaimed work because it is
ready, behind the base branch, or waiting for review. Leave its rebase, fixes,
and merge with that agent.

When another agent owns the PR:

1. Name the recorded owner and cite the PR evidence.
2. Recommend that the originating agent finish it.
3. If coordination is ambiguous, leave a concise PR comment that preserves the
   existing ownership.
4. Add or update the shared-library channel when several consumers need the
   same ownership fact.
5. Select the next independent task.

Provenance is not a permanent lock. A takeover is valid when the user reassigns
the PR, the originating agent records a handoff, or current evidence shows that
the work is abandoned. Record the transfer publicly before modifying the
branch.

## Recommendation rule

Before answering “what is next?”, verify at least the proposed top item. For an
older or high-priority item, inspect enough competing candidates to identify
the real next gap.

Also verify that no active task, PR, or shared-library intent already owns the
same public seam. If one exists, preserve its owner and select independent work
unless the user requests a takeover.

Do not infer these claims:

- open status means code is missing.
- an old failure transcript describes current behavior.
- absent task-to-PR linkage means no PR exists.
- a tracker export is the live tracker.
- a stale intent entry still owns active work.
- a green historical PR proves current behavior after later changes.
- a shared-library channel replaces source, Git, task, or PR checks.

## Minimum evidence by item type

- **Bug:** current focused reproduction or a test that fails when the bug is
  present, plus the relevant implementation path.
- **Feature:** present or absent public behavior and the smallest owning fixture
  or contract.
- **Release or security policy:** current workflow permissions, executable
  policy tests, required live host state, and the establishing commit or PR.
- **Documentation task:** current authoritative guide, navigation links, and the
  behavior or command that the guide explains.
- **External review finding:** current revision versus reviewed revision, with
  each recommendation marked integrated, applicable, or obsolete.
- **Shared-library change:** owner-repository source and tests, current task and
  PR state, coordination-channel evidence, and at least one affected consumer
  when compatibility is part of the claim.

## Reporting

Keep the result short and auditable:

```text
Tracker claim: <what it says remains>
Current evidence: <source, test, history, PR, and coordination evidence>
Classification: <confirmed unresolved | partial | resolved | invalidated | unknown>
Ownership: <task, PR, and shared-library owner or none>
Action: <claim | update | close | coordinate | experiment>
```

If the tracker or coordination entry is stale, state that fact and identify the
current evidence. Do not blame the tracker or channel for a verification step
that an agent skipped.

Reason: An open tracker item is only a lead; current source, history, tests, reviews, and coordination records decide whether work remains.

Examples:
- A shared library has an overlapping proposal. Link or update the existing owner's work instead of starting a duplicate.
- An old bug is open. Reproduce it against current source and check recent history and open pull requests before creating a branch.

Limits:
- Do not scan unrelated repositories without a freshness reason.
- Do not treat an open issue or old failure as proof that work is missing.

Authority boundary: This skill guides writing and review only. It grants no source write, tool, provider, task, or effect authority.
