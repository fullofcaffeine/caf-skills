---
name: calibrate-reasoning-effort
description: Assess task complexity, recommend the lowest effective Codex reasoning setup—low, medium, high, xhigh, max, or ultra—and automatically apply it for subsequent turns whenever a supported host or bundled App Server control is available. Use before substantial work, whenever scope or risk changes, when starting or claiming a task, choosing a thinking label, planning an agent run, answering which reasoning level is appropriate, or balancing quality against latency and token usage. Optimize total expected task cost, including verification, failed attempts, rework, and coordination; do not choose a superficially cheap level that is likely to require more iterations, and release any level as soon as another level becomes the lowest effective choice.
---

# Calibrate Reasoning Effort

Choose the cheapest setup likely to complete the task correctly and efficiently.
Calibrate before substantial work on each new task, then recalibrate only when
the task's risk or shape changes. Minimize total expected work, not the
reasoning tokens spent in the first turn:

```text
total expected cost =
  reasoning tokens
  + tools and verification
  + expected rework
  + coordination
  + probability of a wrong decision × cost of its consequences
```

## Required quick start

Calibration has three required steps when runtime control is available:

1. Recommend and announce the lowest effective level.
2. Apply that level immediately for subsequent turns.
3. At every stable phase boundary or task closure, reassess and immediately
   apply the newly appropriate level. Treat `max` as the shortest necessary
   decision lease and release it as soon as that decision window closes.

When applying `high`, `xhigh`, or `max`, name the concrete risk or decision
window that warrants the extra cost and the evidence or phase transition that
will trigger recalibration. Do this in the same update as the upshift so the
level has an exit condition from the start.

Do not stop after writing a recommendation or task label. First prefer a direct
host/orchestrator effort control. Otherwise, when `CODEX_THREAD_ID` and
`CODEX_HOME` are present, run the bundled helper before beginning substantial
work:

```sh
node <skill-dir>/scripts/apply-reasoning-effort.mjs <level>
```

The helper checks the existing App Server control socket itself. Do not assume
control is unavailable merely because no reasoning tool or socket environment
variable appears in the visible tool list. Report the helper's
`{"applied":true}` result as applying only to subsequent turns. If it fails,
report the concise cause and continue at the available setting; never claim the
active turn changed.

The lowest plausible level is often not the lowest effective level. Spending a
little more reasoning up front is cheaper when a weak first pass would cause
several edit-test-debug loops or an expensive incorrect decision.
Ambiguity raises the probability of a wrong decision. A broad blast radius and
poor reversibility raise its consequence cost. Use those relationships to make
the tradeoff explicit without turning calibration into a fake-precise score.

## Treat effort as a phase-scoped lease

Apply a reasoning level only for as long as the current task or task phase
justifies it. The setting is not a sticky session default and must not remain
elevated merely because an earlier phase was difficult.

- Recalibrate at a stable phase boundary when the remaining work materially
  changes shape—for example, after an architecture decision is accepted, a
  safe seam is isolated, an ambiguous failure becomes a deterministic
  reproducer, or a risky implementation becomes mechanical verification.
- Do not retain a level merely because the next phase belongs to the same task.
  Calibrate the work that remains, not the hardest work already completed.
- Immediately apply the newly appropriate level for subsequent turns. The new
  level may be lower or higher; choose by expected total cost, not by momentum.
- Be increasingly deliberate about releasing expensive levels. In particular,
  use `max` only for the shortest necessary tightly coupled decision window.
  Once that decision is settled and the remaining implementation or validation
  is adequately served by `xhigh`, `high`, `medium`, or `low`, downgrade before
  continuing substantial work.
- Apply the same rule to every level: keep it while it remains the lowest
  effective choice, then change it when another level becomes more appropriate.
- Do not oscillate for individual commands or downgrade in the middle of an
  unresolved reasoning-dependent operation. A phase boundary must reflect a
  real reduction in ambiguity, consequence, blast radius, or verification
  difficulty.

Higher reasoning levels consume more tokens and latency, but token cost alone
is not a reason to downgrade. Releasing an elevated level too early can create
more rework than it saves; retaining it after the risk has passed is also
wasteful.

### Required effort-release check

At every task closure and every stable phase boundary, explicitly ask whether
the current level is still the lowest effective level for the remaining work.
If it is not, apply the newly appropriate level before the next substantial
turn.

- Treat `max` as an exceptional, tightly bounded lease. Recalibrate
  immediately after the compiler-wide, release, provenance, or similarly
  high-consequence decision that justified it is settled. Do not carry `max`
  into bounded implementation, routine verification, documentation, waiting,
  or hand-off work unless that next phase independently meets the `max`
  criteria.
- Apply the same release rule to `xhigh`, `high`, `medium`, and `low`. A level
  may move down or up when the work changes; prior difficulty is not evidence
  that the next phase needs the same setting.
- Increase release-check frequency with cost: inspect `high` at major phase
  boundaries and inspect `xhigh` or `max` as soon as the risky decision or
  synthesis window closes.
- When entering `high`, `xhigh`, or `max`, record the expected release trigger.
  When that trigger occurs, recalibrate before doing more substantial work;
  do not postpone the check until the whole tracked task closes.
- If another task or phase is already known, recommend and apply its level in
  the closure update. If no next work is known, record that the elevated lease
  ended and calibrate when work resumes instead of inventing a task merely to
  choose a setting.

## Calibrate

1. Read the requested outcome, constraints, and available acceptance evidence.
   Inspect only enough local context to understand the task shape; do not turn
   calibration into a separate research project.
2. Judge these signals qualitatively:
   - ambiguity: how much of the problem or success criterion is unknown;
   - consequence: the cost of a wrong decision, especially one that looks right;
   - blast radius: how many components, repositories, users, people, or external
     systems can be affected;
   - novelty: whether a proven local pattern or test oracle exists;
   - reversibility: how cheaply a wrong choice can be detected and undone;
   - verification cost: how slow, noisy, or expensive decisive validation is;
   - likely rework: how many edit-test-debug loops a weak first pass may cause;
   - coordination cost: the overhead of synchronizing people or agents;
   - decomposition: whether meaningful independent workstreams can safely run
     in parallel.
3. Select the level from the table below. Let a severe signal dominate an
   average of many harmless signals; do not use a mechanical point score.
4. Announce the recommendation before substantial work, usually in one line:

   `Recommended reasoning: high — dependency invalidation can silently reuse stale work, so the task needs careful invariants and differential tests.`

5. Immediately apply the recommended level for subsequent turns when a runtime
   control is available. This is a required part of using the skill, not an
   optional suggestion. Prefer a direct host or orchestrator reasoning-effort
   control. Otherwise, if `CODEX_THREAD_ID` and `CODEX_HOME` are available, run:

   ```sh
   node <skill-dir>/scripts/apply-reasoning-effort.mjs <level>
   ```

   Replace `<skill-dir>` with this skill's directory and `<level>` with the
   selected value. The helper locates and checks the control socket under
   `CODEX_HOME`; do not pre-emptively skip it because a socket-specific
   environment variable is absent. Do not ask for approval for this scoped
   settings update. Treat an `{"applied":true}` result as proof only for
   subsequent turns. If no supported control is available, say the
   recommendation was not applied and continue with the current setting. For a
   direct Codex TUI without a control socket, recommend launching future
   sessions with `codex-controlled`; do not start a second App Server beside
   the active embedded session.
6. Proceed without asking for approval unless another instruction requires a
   pause. If the repository uses `thinking:*` task labels, apply the matching
   label.
7. Recalibrate only when evidence changes the task shape. Do not oscillate
   between levels for individual commands inside one stable task.

## Select a level

| Level | Use when | Typical examples |
| --- | --- | --- |
| `low` | The work is mechanical, local, unambiguous, readily reversible, and has a fast deterministic check. | Formatting, a literal rename, updating one known value. |
| `medium` | The task is a bounded implementation or CI/tooling change using known patterns, but needs coordinated edits or a focused test. | Routine CI wiring, a small API addition, a straightforward bug with a reproducer. |
| `high` | Correctness depends on complex debugging, multi-component behavior, performance, dependencies, concurrency, lifecycle, or several validation layers. The seam is still bounded. | Dependency graph observation, process cleanup, compiler lowering, cache-key design without reuse. |
| `xhigh` | Architecture, compatibility, release, security, provenance, or broad semantic decisions could produce believable wrong behavior or unsafe state. Require a deliberate second pass. | Semantic cache reuse, security boundaries, data migration, broad compatibility or release gates. |
| `max` | This is among the hardest tightly coupled single-agent reasoning work, where a wrong design would be very expensive and cannot be safely split. | Selecting a compiler-wide semantic boundary, changing 1.0 evidence policy, high-impact provenance strategy. |
| `ultra` | The task genuinely benefits from coordinated parallel agents with meaningful independent workstreams that can later be synthesized. | A cross-repository compatibility audit with independent target reviews, or research plus isolated implementation and validation streams. |

These six levels describe GPT-5.6 Sol reasoning setups. When it is available,
prefer GPT-5.6 Sol for this workflow. `max` increases
single-agent reasoning. `ultra` uses subagents and should be selected only when
parallel work has clear ownership and reduces total wall-clock or review risk.
If subagents are unavailable or the task cannot be split safely, choose the
appropriate single-agent level instead of calling the task ultra.

## Recommend versus apply

Keep these actions distinct:

1. **Recommend:** state the lowest effective level and one-sentence reason. When
   requested, also return the machine-readable record below. This is always
   possible.
2. **Apply:** immediately use an exposed host control or the bundled App Server
   helper to set the recommended effort for subsequent turns. When either
   control exists, application is mandatory. Never claim the active turn
   changed merely because a recommendation, task label, or update request was
   written.

A `thinking:*` label records intent; it does not prove the runtime setting
changed.

## Capability boundary

Do not claim to change the active agent's reasoning effort unless the current
environment exposes a tool or control that actually does so. In many Codex
sessions, the agent can recommend a level but the user or hosting surface must
apply it through its model/reasoning control. A task label documents the needed
care; it does not prove that the runtime setting changed.

Codex App Server clients can automate the handoff between turns. The bundled
helper sends `thread/settings/update` with the current `CODEX_THREAD_ID` through
`codex app-server proxy`; client glue may instead send the chosen value as
`effort` in `turn/start`. Both paths apply to subsequent turns. Neither can
retroactively change a turn already in progress.

For local CLI use, `codex-controlled` starts or reuses one Unix-socket App
Server per `CODEX_HOME` and launches the TUI against it. Multiple TUI instances
may share that server safely because the helper updates only the thread named by
the calling process's `CODEX_THREAD_ID`.

When an orchestrator explicitly supports selecting model and reasoning effort
for a new turn or agent, use that control only within the user's authority.
Report one of these outcomes after the recommendation:

- `Applied reasoning for subsequent turns: <level>.`
- `Reasoning recommendation not applied: <concise cause>.`

Continue with the available setting and never report an automatic switch that
did not occur.

For automation, return this compact record when the host asks for a
machine-readable decision:

```json
{"effort":"high","reason":"Dependency invalidation can silently reuse stale work.","mode":"single-agent","recalibrate_on":["scope expands","behavior oracle becomes unclear"]}
```

Use `mode: "multi-agent"` only with `effort: "ultra"`. Keep the ordinary
human-facing recommendation to one sentence unless more detail is requested.

## Calibration checks

Use these contrasting cases to verify that calibration follows risk and total
cost rather than diff size or prestige:

| Case | Recommendation | Why |
| --- | --- | --- |
| Change one authorization condition in a tiny file. | `xhigh`, single-agent | The diff is tiny, but a plausible mistake crosses a security boundary and deserves a second pass. |
| Apply a huge generated rename with an exact deterministic checker and cheap rollback. | `low`, single-agent | File count is large, but reasoning is mechanical and decisive verification is cheap. |
| Resolve one tightly coupled compiler architecture decision through sequential investigation and validation. | `max`, single-agent | The work is difficult, but parallel agents would add coordination without independent ownership. |
| Audit four independent target integrations, then synthesize compatibility evidence. | `ultra`, multi-agent | Independent workstreams can run concurrently and materially reduce elapsed time and review risk. |

If a supposedly mechanical rewrite lacks a decisive checker, raise it to
`medium`. If the independent streams cannot be cleanly owned and synthesized,
do not call sequential complexity `ultra`.

## Avoid false economy

- Do not pick `low` merely because the requested diff is small. A one-line cache
  key, authorization rule, or ABI change can be high risk.
- Do not pick `high` merely because many files change. A generated or mechanical
  rewrite with a strong checker may still be low or medium.
- Do not treat a red test, unfamiliar filename, or tedious verification as an
  automatic escalation. Escalate when the model or safe seam is unclear.
- Increase upfront effort when feedback is slow or a plausible wrong result can
  pass ordinary tests.
- Prefer a lower level when the task has an exact reproducer, a narrow owner,
  fast checks, and a cheap rollback—even if the surrounding domain is complex.
- Account for verification. A correct-looking answer without decisive evidence
  is not a cheaper completion.

## Escalate or reduce

Escalate one or more levels when:

- the task expands across an unplanned boundary;
- the governing invariant or behavior oracle becomes unclear;
- two bounded attempts fail for different reasons;
- validation is too weak to distinguish a plausible wrong result; or
- release, security, provenance, or irreversible external state enters scope.

Reduce the level for a newly isolated implementation subtask when research has
already fixed the design, the remaining edit is mechanical, and a focused test
fully checks it. Keep the parent decision at its original level.

For `xhigh` and `max`, plan an independent second pass before closure. For
`ultra`, name the independent workstreams, give each the lowest effective local
effort, and synthesize their evidence before deciding.

## Respect explicit choices

If the user explicitly chooses a level, use it when the environment supports
it. Briefly warn when it is likely to increase total cost or risk—for example,
`low` on a subtle cache invalidation change or `ultra` on a task with no useful
parallel split—but do not silently claim a different level was used.

Do not browse model documentation during routine calibration. Check current
official OpenAI documentation only when the user asks for verification or when
the available model or effort controls conflict with this skill.
