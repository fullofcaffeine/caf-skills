---
name: wait-for-completion
description: "Wait for background builds, tests, reviews, or jobs without repeated model-driven status checks. Use when starting background work, choosing how to await completion, or resuming from a completion notification."
license: "Apache-2.0"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:d0449d6b3b7fccc5ba5c04ee89513a0724d8f0674638eb4e1cada48ce4c149d6. Selection digest: sha256:a83562d44ceb4040307a1e3cbf34058e2b73013da2dbd9ea4ad52516eb4a0cce. Effective AgentSpec digest: sha256:a40101bacb205af84641bbb506e4717a4529c4ba94bb8ba7396dcc45f794e6a6 -->

# Wait for completion

Use passive waiting by default. Lower reasoning effort alone does not make
repeated polling efficient.

- Before yielding, retain the owner task, exact run handle, evidence location,
  deadline, and next action in the existing task or run record.
- Prefer the host's completion notification or event-backed wait. Verify that
  it can resume this task; a background PID alone provides no wake guarantee.
- Do useful independent work when available. Otherwise yield through the
  supported wait mechanism. Do not repeatedly read logs, inspect processes, or
  call status tools merely to discover completion.
- Active checking needs a concrete reason: the user asks for status, a safety
  or deadline concern arises, notification fails, or the host has no supported
  completion wake. State the reason and use the smallest bounded fallback.
  No polling daemon, model-driven sleep/check loop, or repeated unchanged updates.
  Missing wake support does not permit repeating bounded checks indefinitely,
  including across automatic goal-continuation turns.
- A timer wake is not a completion signal. If automatic resumption is unavailable,
  say so; preserve the handoff instead of claiming you will be notified.
- On completion, read terminal evidence and resume the recorded work. A quiet
  log, missing process, or elapsed deadline does not prove success. Do not restart
  a job just because a wait timed out. Respect host responsiveness limits.
- When only waiting, request low effort through available controls. Recalibrate
  before substantive diagnosis or edits. Never change the selected model.

## Wait passively for background completion

## Codex capability routing

Check the tools exposed by this host, not just their names:

- Prefer an exact-job completion subscription that resumes the owning thread.
  Verify that route before promising automatic resumption.
- `exec_command` returning a `session_id` only gives a terminal handle.
  Repeated empty `write_stdin` calls are polling, even with long timeouts.
- `functions.wait` resumes an outstanding `functions.exec` cell, not an
  arbitrary shell job. If the cell merely polls a terminal, wrapping it does
  not make that workflow event-driven.
- Thread/agent wait tools wait for their documented task handles. Do not pass
  a shell session ID or spawn an agent merely to poll on your behalf.
- App Server completion events can support a native adapter. The adapter must
  correlate the job and resume its owner; an event shown in the UI is not proof
  of that route. The `notify` agent-turn-complete hook is not a subprocess wake.

If no suitable route is exposed, report the limitation once, retain the run
record, and yield control. Do not invent a scheduler, launch a second App
Server, or claim that this skill installs a wake mechanism.

## Caf ownership

Reuse `caf:agentspec:rule:background-wait-reasoning-low` in the explicitly
selected `caf:agentspec:policy:managed-workspace-bootstrap`. Its inline CML owner
is `modules/system/agentspec/src/caf/system/agentspec/AgentSpecBootstrapPolicy.hx`
in Cafetera. Native systems own job state; Beads owns task state. Graph views
make these references discoverable, not authoritative.

This shared skill is native guidance, not an installed scheduler or proof of
enforcement. Caf package admission and digest-pinned selection are separate
from native skill installation. Do not fabricate them or require Caf tooling
when the host already offers an honest passive wait.

Reason: Polling spends tokens without speeding the work; a recorded handle and a verified wake resume the owner when the result exists.

Examples:
- A full test gate runs for several minutes. Record the run handle and evidence path, yield through the host notification, and read the result once on wake.
- The host has no completion notification. Report that limitation and use one bounded check with a stated reason.

Limits:
- Do not create a polling daemon or a sleep-and-check loop.
- Do not treat a timer expiry as completion evidence.

Authority boundary: This skill guides writing and review only. It grants no source write, tool, provider, task, or effect authority.
