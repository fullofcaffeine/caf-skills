---
name: keep-it-simple
description: Find the clearest complete design with the least accidental complexity while preserving the full goal, production quality, safety, correctness, maintainability, developer experience, and evidence. Use when work adds safeguards, abstractions, wrappers, retries, compatibility paths, state, configuration, or tests; when a solution feels complicated or overengineered; or when the user asks for KISS, elegance, simplicity, less code, fewer layers, or "as simple as possible, but not simpler." Never use this skill to cut scope, quality, or proof merely to reduce effort.
---

# Keep It Simple

Build the clearest complete solution. Simplicity means an elegant design with
few concepts and clear ownership. It does not mean the fewest lines, the least
work, or only the smallest patch.

Remove accidental complexity. Keep purposeful complexity when it achieves or
protects a real requirement. The full goal includes the user's stated vision,
production quality, safety, correctness, maintainability, developer experience,
and proportionate evidence. A credible near-term need can justify work now when
doing it later would create a worse boundary or substantial rework.

## Use the simplicity test

1. State the complete outcome before reducing the design.
2. List the quality, safety, correctness, lifecycle, and evidence invariants.
3. Identify credible near-term needs that materially affect today's boundary.
4. Compare direct designs and choose the one with the fewest independent concepts
   that fully achieves the outcome.
5. Map each remaining layer to a requirement, likely failure, durable design
   boundary, or decisive test.
6. Remove, merge, or narrow only the complexity that has no sufficient reason.
7. Prefer the correct lowest owner and the platform's native behavior.
8. Prove the result with focused regressions and a representative real acceptance
   path. Add broader evidence when the risk or claim requires it.

Use judgment. A need does not require an existing production failure. Product
direction, a hard-to-change public boundary, repeated maintenance cost, a known
security risk, or a concrete developer-experience goal can also justify a little
more work. Do not add machinery for an unspecified hypothetical future.

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

Never use KISS to:

- narrow an explicit goal without the user's agreement;
- postpone the core architecture only because the correct work is larger;
- weaken type safety, security, error handling, compatibility, portability,
  maintainability, developer experience, or verification;
- accept a temporary shortcut that creates more total complexity or predictable
  rework; or
- optimize for line count, implementation speed, or the number of tests at the
  expense of a trustworthy result.

It can be simpler overall to do slightly more now. This is true when the work
removes a duplicate path, establishes one durable owner, makes a public boundary
harder to misuse, enables a stated product direction, or avoids likely rework.
Keep that work focused and explain why it reduces total complexity.

## Stop adding layers

Stop when the complete outcome and its invariants have proportionate evidence.
Do not stop at a minimal tracer bullet when the stated goal also requires a
durable public API, production hardening, portability, extraction, or another
explicit quality.

Do not multiply fixtures, retries, abstractions, or recovery modes after the
acceptance evidence is sufficient. Treat ungrounded generalization as follow-up
work. A new requirement or failure can reopen the design with new evidence.
