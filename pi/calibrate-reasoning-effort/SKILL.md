---
name: calibrate-reasoning-effort
description: "Assess task complexity, recommend the lowest effective reasoning setup—low, medium, high, xhigh, max, or ultra—and automatically apply it for subsequent turns while preserving the currently selected model, including GPT-6 Astra and GPT-5.6 Sol, whenever a supported host control or the bundled harness-detecting helper is available. Use before substantial work, whenever scope or risk changes, when starting or claiming a task, choosing a thinking label, planning an agent run, answering which reasoning level is appropriate, or balancing quality against latency and token usage. Before max or ultra, recommend oracle-review when a slower independent review can receive enough exact context. Treat every level as a phase-scoped lease, release it as soon as a cheaper level becomes effective, and keep max or xhigh only for the shortest necessary decision window."
license: "Apache-2.0"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:f7b5af895706d134d2ab5eb7c74ea3e32fad5df24a510764659768ba7ecc34c6. Selection digest: sha256:a83562d44ceb4040307a1e3cbf34058e2b73013da2dbd9ea4ad52516eb4a0cce. Effective AgentSpec digest: sha256:ea4326c1ff73a1a0dc68b21a3ab8f34941e5aac199cc3a76e7e6e7743f3022b3 -->

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

## Calibrate, apply, and release the reasoning lease

## Required quick start

Calibration has three required steps when runtime control is available:

1. Recommend and announce the lowest effective level.
2. Apply that level immediately for subsequent turns.
3. Before recommending `max` or `ultra`, assess whether `$oracle-review` can
   receive enough exact context and provide a useful independent pass.
4. Before the next substantial action after a stable phase boundary, reassess
   and immediately apply the newly appropriate level. Treat every setting as a
   phase lease, never as a task or session default. Keep `max` and `xhigh` only
   for the shortest necessary decision window.

For every level, name the current phase and its release trigger. When applying
`high`, `xhigh`, or `max`, also name the concrete risk or decision window that
warrants the cost. Do this in the same update as the change. When the trigger
occurs, apply the lower level before another substantial edit, test, diagnosis,
or planning step. Do not wait for the task to close or for the user to ask.

Do not stop after writing a recommendation or task label. First prefer a direct
host/orchestrator effort control. Otherwise, run the bundled helper before
beginning substantial work. It detects the harness: Codex when
`CODEX_THREAD_ID` and `CODEX_HOME` are present, Claude Code when
`CLAUDECODE=1`:

```sh
node <skill-dir>/scripts/apply-reasoning-effort.mjs <level>
```

On Codex, the helper checks the existing App Server control socket itself. Do not assume
control is unavailable merely because no reasoning tool or socket environment
variable appears in the visible tool list. Report the helper's
`{"applied":true}` result as applying only to subsequent turns. If it fails,
report the concise cause and continue at the available setting; never claim the
active turn changed.

On Claude Code, a running session cannot change its own effort; only the
user's `/effort` command can. The helper returns `{"applied":false}` with that
route. Run the phase's work in a subagent with the requested effort and the
current model, and recommend `/effort <level>` when the main session itself
must change. A subagent's effort applies only to that subagent's work.

Searching or inspecting the visible tool list is not an application attempt.
If no direct effort-control tool is callable, invoke the bundled helper
immediately; do not spend another turn merely reporting a recommendation or
apparent lack of control. Do not say that the host control is unavailable until
the helper has actually returned a failure. Keep these status words exact:

- `recommended` means the level was selected but has not been proved active;
- `applied` means a direct control or the helper returned success for subsequent
  turns, or a subagent runs the phase at that level;
- `unavailable` means every applicable control path was attempted and failed.

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

Use this hard boundary:

- A lease covers one named reasoning-dependent phase, not an issue, goal,
  conversation, or implementation project.
- Recheck the lease after each decisive result that settles ambiguity, fixes an
  architecture, isolates a reproducer, or provides a deterministic checker.
- If a cheaper level is now effective, apply it before the next substantial
  action. A later failure can justify a new lease; possible future difficulty
  does not justify retaining the old one.
- Treat a user's concern about token use or latency as an immediate
  recalibration signal, while still choosing the lowest level that protects
  correctness.

- Recalibrate at a stable phase boundary when the remaining work materially
  changes shape—for example, after an architecture decision is accepted, a
  safe seam is isolated, an ambiguous failure becomes a deterministic
  reproducer, or a risky implementation becomes mechanical verification.
- Do not retain a level merely because the next phase belongs to the same task.
  Calibrate the work that remains, not the hardest work already completed.
- Immediately apply the newly appropriate level for subsequent turns before
  continuing substantial work. The new level can be lower or higher. Choose by
  expected total cost, not by momentum.
- Be increasingly deliberate about releasing expensive levels. In particular,
  use `max` only for the shortest necessary tightly coupled architecture or
  synthesis decision. Once the seam and decisive verification strategy are
  known, downgrade before implementation or validation unless that next phase
  independently qualifies for `max`. Apply the same rule to `xhigh` after its
  compatibility, release, security, or provenance decision is settled.
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

### Foreground waits and monitoring

Treat a foreground wait as a stable phase boundary when the only remaining
work is polling or reading a terminal status.

1. Record the level that the substantive task will probably need when work
   resumes.
2. Apply `low` before waiting or monitoring. Status polling does not benefit
   from carrying a more expensive reasoning level.
3. Keep user updates and the monitoring cadence required by the host; lowering
   effort must not make the agent abandon the wait.
4. When the external work finishes or produces a result that needs judgment,
   recalibrate and apply the lowest effective level for that next phase. Restore
   the recorded level when the task shape is unchanged; choose a different
   level when the result changes the risk or ambiguity.

Do not lower merely because one tool call is slow when the agent is still
reasoning, editing, coordinating, or interpreting partial results concurrently.
The downgrade is for a genuine wait-only phase. Escalate before diagnosing a
failure, changing code, or making a consequential completion decision.

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
4. If the candidate is `max` or `ultra`, apply the Oracle-first check below.
5. Announce the recommendation before substantial work, usually in one line:

   `Recommended reasoning: high — dependency invalidation can silently reuse stale work, so the task needs careful invariants and differential tests.`

6. Immediately apply the recommended level for subsequent turns when a runtime
   control is available. This is a required part of using the skill, not an
   optional suggestion. Prefer a direct host or orchestrator reasoning-effort
   control. Otherwise, run the bundled helper:

   ```sh
   node <skill-dir>/scripts/apply-reasoning-effort.mjs <level>
   ```

   Replace `<skill-dir>` with this skill's directory and `<level>` with the
   selected value. On Codex, the helper locates and checks the control socket under
   `CODEX_HOME`; do not pre-emptively skip it because a socket-specific
   environment variable or visible tool is absent. A tool-list search does not
   satisfy this step. Do not ask for approval for this scoped
   settings update. Treat an `{"applied":true}` result as proof only for
   subsequent turns. If no supported control is available, say the
   recommendation was not applied and continue with the current setting. On
   Claude Code, follow the subagent route above. For a
   direct Codex TUI without a control socket, recommend launching future
   sessions with `codex-controlled`; do not start a second App Server beside
   the active embedded session.
7. Proceed without asking for approval unless another instruction requires a
   pause. If the repository uses `thinking:*` task labels, apply the matching
   label.
8. Recalibrate only when evidence changes the task shape. Do not oscillate
   between levels for individual commands inside one stable task.

## Check Oracle before max or ultra

Before recommending local `max` or `ultra`, recommend `$oracle-review` first
when all these conditions hold:

- the decision benefits from a slower independent planning or review pass;
- exact repository sources, current evidence, constraints, and the decision
  question can be packaged without hiding decisive private or live state;
- waiting for the response does not create a larger operational risk; and
- the driving agent can reconcile the advisory answer against current local
  evidence before implementation or acceptance.

Oracle is especially useful for architecture synthesis, compatibility and
migration choices, critical result review, conflicting evidence, and work that
does not converge. State why Oracle is useful and identify the exact decision
or artifact it will review. Use the canonical `$oracle-review` skill. Do not
invent a manual browser or transcript workflow.

Recommend local `max` first when the hard part depends on immediate compiler or
test feedback, fast repository-local inspection, confidential state that cannot
be packaged safely, an active incident, or another condition that makes an
external review incomplete or too slow. Use `ultra` only when real independent
local workstreams also justify subagents. Oracle is an independent reviewer,
not a substitute name for `ultra`.

If Oracle is selected, use the lowest effective local level to prepare exact
context and continue independent work. Recalibrate when the response arrives.
Oracle advice remains advisory and does not accept a plan, change, or effect.

## Select a level

| Level | Use when | Typical examples |
| --- | --- | --- |
| `low` | The work is mechanical, local, unambiguous, readily reversible, and has a fast deterministic check. | Formatting, a literal rename, updating one known value. |
| `medium` | The task is a bounded implementation or CI/tooling change using known patterns, but needs coordinated edits or a focused test. | Routine CI wiring, a small API addition, a straightforward bug with a reproducer. |
| `high` | Correctness depends on complex debugging, multi-component behavior, performance, dependencies, concurrency, lifecycle, or several validation layers. The seam is still bounded. | Dependency graph observation, process cleanup, compiler lowering, cache-key design without reuse. |
| `xhigh` | Architecture, compatibility, release, security, provenance, or broad semantic decisions could produce believable wrong behavior or unsafe state. Require a deliberate second pass. | Semantic cache reuse, security boundaries, data migration, broad compatibility or release gates. |
| `max` | Oracle was unsuitable or insufficient, and this is among the hardest tightly coupled single-agent reasoning work. A wrong design would be very expensive and cannot be safely split. | Selecting a compiler-wide semantic boundary that depends on immediate local feedback, changing 1.0 evidence policy, high-impact provenance strategy. |
| `ultra` | Oracle was unsuitable or insufficient, and the task genuinely benefits from coordinated parallel agents with meaningful independent workstreams that can later be synthesized. | A cross-repository compatibility audit with independent target reviews, or research plus isolated implementation and validation streams. |

These six levels calibrate the model that is already selected. They support
GPT-6 Astra, GPT-5.6 Sol, and other host-supported reasoning models. Never
select, prefer, or migrate to a different model as part of calibration; change
only the reasoning effort. `max` increases single-agent reasoning. `ultra` uses
subagents and should be selected only when parallel work has clear ownership
and reduces total wall-clock or review risk. If subagents are unavailable or
the task cannot be split safely, choose the appropriate single-agent level
instead of calling the task ultra.

## Recommend versus apply

Keep these actions distinct:

1. **Recommend:** state the lowest effective level and one-sentence reason. When
   requested, also return the machine-readable record below. This is always
   possible.
2. **Apply:** immediately use an exposed host control or the bundled helper to
   set the recommended effort for subsequent turns. When either
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

Claude Code reads its effort setting at session start, and only the user's
`/effort` or `/model` command changes the main session. The Agent tool accepts
an effort for each subagent it starts. To reach a higher effort for one phase,
delegate that phase to a subagent with the same model and the requested effort,
then reconcile its result in the main session.

When an orchestrator exposes both model and reasoning controls for a new turn
or agent, preserve the selected model and set only reasoning effort. Do not
populate or change a model field as a side effect of calibration.
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
| Review a packageable cross-system architecture decision with stable evidence. | `$oracle-review`, then recalibrate | A slower independent pass can challenge the design before an expensive local lease. |
| Resolve one tightly coupled compiler architecture decision through immediate compile feedback that Oracle cannot observe. | `max`, single-agent | The work is difficult, local evidence changes quickly, and parallel agents would add coordination without independent ownership. |
| Audit four independent target integrations after Oracle cannot receive decisive private evidence. | `ultra`, multi-agent | Independent local workstreams can run concurrently and materially reduce elapsed time and review risk. |

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

Do not browse model documentation during routine calibration. Check the current
official documentation for the harness and model provider only when the user
asks for verification or when the available model or effort controls conflict
with this skill.

Reason: Effort that stays too low causes rework, and effort that stays too high wastes tokens and latency; applying and releasing a phase-scoped level through the harness's real control keeps total cost low without claiming a change that did not happen.

Examples:
- On Claude Code, the helper reports applied false with the /effort route. Run the hard phase in a subagent with the requested effort and the same model, and recommend /effort for the main session.
- On Codex, the helper reports applied true for harness codex. Report the level as applied for subsequent turns only, never for the active turn.

Limits:
- Do not change the selected model as part of calibration.
- Do not report an effort as applied when the helper or host control did not return success.

Authority boundary: This skill guides effort choice and may run its bundled helper within the package's effect ceilings. It grants no source write, task, provider, model, or other effect authority.

## Included assets

These files are part of the exact package closure. Inclusion does not permit helper execution.

- `scripts/apply-reasoning-effort.mjs` — helper; effectful-adapter
