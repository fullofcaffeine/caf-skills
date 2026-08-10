---
name: keep-it-simple
description: Reduce plans, implementations, fixes, reviews, and refactors to the smallest design that still meets the stated goal and preserves required safety, correctness, and evidence. Use when work adds safeguards, abstractions, wrappers, retries, compatibility paths, state, configuration, or tests; when a solution feels bloated or overengineered; or when the user asks for KISS, simplicity, less code, fewer layers, or "as simple as possible, but not simpler."
---

# Keep It Simple

Build the smallest reliable solution. Remove complexity that does not protect a
stated goal, invariant, or observed failure.

## Use the simplicity test

1. State the required outcome.
2. List the safety and correctness invariants that must remain true.
3. Map each new layer to one requirement, observed failure, or decisive test.
4. Remove, merge, or narrow anything without that mapping.
5. Prefer the lowest owner and the platform's native behavior.
6. Prove the result with one focused regression and the smallest real acceptance path.

Do not keep code because it might become useful. Add a new mechanism only when
current evidence shows that the simpler design cannot meet the goal.

## Prefer direct designs

- Prefer one authority, one owner, and one path for each effect.
- Prefer semantic or typed platform primitives over custom tracking state.
- Keep temporary provider or runtime details out of durable contracts.
- Re-resolve changing external state instead of preserving stale references.
- Remove incidental checks when they reject a valid flow.
- Add one narrow guard for a named failure instead of a general framework.
- Use an event or authoritative state transition before adding polling or retry logic.
- Reuse an existing boundary before adding another wrapper, adapter, or configuration option.

## Do not make it simpler than the goal allows

Keep complexity when removing it would weaken a required invariant. High-cost
failures can justify a small, explicit guard even when the normal flow looks
simple.

Examples include durable intent before an irreversible effect, exact identity
before a destructive action, validation at an untrusted boundary, and a
one-shot rule after an uncertain result.

When complexity remains, explain the named failure it prevents and the test
that proves it. If no such explanation exists, simplify again.

## Stop adding layers

Stop when the required outcome and invariants pass their focused tests and one
real acceptance path. Treat speculative improvements as follow-up work unless
they prevent a concrete contract failure.

Do not multiply fixtures, retries, abstractions, or recovery modes after the
acceptance evidence is sufficient. A new failure can reopen the design with new
evidence.
