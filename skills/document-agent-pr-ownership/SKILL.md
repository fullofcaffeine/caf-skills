---
name: document-agent-pr-ownership
description: Record clear, public ownership and provenance whenever an AI agent creates, updates, hands off, or takes over a pull request. Use when opening or substantially revising a PR, when work was prepared by a named third-party agent, when several agents share a repository, or when a reviewer needs to know why a different agent created the branch and who should finish it.
---

# Document Agent PR Ownership

Make agent involvement understandable without requiring private conversation
history. Agent attribution supplements the technical PR explanation; it never
replaces the problem, user value, design, examples, or verification evidence.

## Creating a PR

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

## Updating or handing off a PR

If ownership changes, update the PR description and add a timestamped comment
that names the former owner, new owner, reason, exact head, and remaining work.
Do this before the new agent pushes changes.

If another agent discovers the PR but is not taking it over, leave the branch
unchanged. Add a coordination comment only when it prevents ambiguity or
duplicate effort.

## Review and merge boundary

Before changing an agent-created PR, inspect its provenance section, comments,
review requests, and recent activity. Do not infer abandonment merely from a
stale merge base or elapsed time. Ask the user or recorded owner when ownership
is unclear and overlapping edits would be risky.

Agent provenance is coordination metadata, not evidence that the PR is sound.
The normal exact-head review, CI, documentation, security, and merge rules still
apply.
