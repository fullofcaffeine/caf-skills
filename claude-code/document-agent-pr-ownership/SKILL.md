---
name: document-agent-pr-ownership
description: "Record clear, public ownership and provenance whenever an AI agent creates, updates, hands off, or takes over a pull request. Use when opening or substantially revising a PR, when work was prepared by a named third-party agent, when several agents share a repository, or when a reviewer needs to know why a different agent created the branch and who should finish it."
license: "Apache-2.0"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:fd2a68aac164cacc11b8d0b927dfe2f129f2cdaf2c7b138345d075aa0e38688f. Selection digest: sha256:7c941a31cdaa09f3ab3967e23a3cab2edca54e5e1daa0d70bb927767883c26ab. Effective AgentSpec digest: sha256:6c6b670fb81e6f628fcf14f8e170d2094ac01ee8826c6eef88dd2636485d5c7c -->

# Document Agent PR Ownership

Make agent involvement understandable without requiring private conversation
history. Agent attribution supplements the technical PR explanation; it never
replaces the problem, user value, design, examples, or verification evidence.

## Record agent provenance in pull requests

### Creating a PR

Add a short `Agent provenance` section to every agent-created PR description.
It must state:

- the human-readable agent name or role that prepared the work;
- why that agent was assigned or became involved;
- the task, issue, or handoff context that led to the PR;
- whether that agent retains responsibility for review fixes, rebasing, and
  merge, or whether the PR is explicitly handed off; and
- any boundary a new agent should respect before taking over.

Example:

```markdown
## Agent provenance

Prepared by the GameCarry agent after it was assigned the development-session
Bead and its focused runtime closure work. GameCarry retains ownership of
review fixes, rebasing, and the final merge. Other agents should review or
comment without modifying this branch unless the user records a handoff.
```

Do not write only `Prepared by <agent>`. Explain why that agent created the PR
and what the attribution means operationally.

### Updating or handing off a PR

If ownership changes, update the PR description and add a timestamped comment
that names the former owner, new owner, reason, exact head, and remaining work.
Do this before the new agent pushes changes.

If another agent discovers the PR but is not taking it over, leave the branch
unchanged. Add a coordination comment only when it prevents ambiguity or
duplicate effort.

### Review and merge boundary

Before changing an agent-created PR, inspect its provenance section, comments,
review requests, and recent activity. Do not infer abandonment merely from a
stale merge base or elapsed time. Ask the user or recorded owner when ownership
is unclear and overlapping edits would be risky.

Agent provenance is coordination metadata, not evidence that the PR is sound.
The normal exact-head review, CI, documentation, security, and merge rules still
apply.

Reason: Reviewers need to know which agent prepared the work, why, and who finishes it, without that attribution replacing the technical explanation.

Examples:
- A different agent takes over a branch. Update the provenance section to record the handoff and the new owner.
- An agent opens a pull request. Add a short Agent provenance section naming the agent, why it was involved, and the owner who finishes the work.

Limits:
- Do not include private transcripts or hidden reasoning.
- Do not let attribution replace the problem, user value, design, examples, or verification evidence.

Authority boundary: This skill guides writing and review only. It grants no source write, tool, provider, task, or effect authority.
