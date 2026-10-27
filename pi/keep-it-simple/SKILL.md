---
name: keep-it-simple
description: "Find the clearest complete design with the least accidental complexity while preserving the full goal, production quality, safety, correctness, maintainability, developer experience, and evidence. Use when work adds safeguards, schemas, modules, abstractions, wrappers, adapters, planners, workflows, skills, retries, compatibility paths, state, configuration, or tests; when similar work may already exist in the current repository, history, tracker, sibling project, dependency, or upstream; when considering cross-project extraction or consolidation; when a solution feels complicated or overengineered; or when the user asks for KISS, elegance, simplicity, less code, fewer layers, no duplication, or \"as simple as possible, but not simpler.\" Never use this skill to cut scope, quality, or proof merely to reduce effort."
license: "Apache-2.0"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:0cb842dee1a0b28cef6bb613cce4b52673b592850f184c47e5a7e3546e0652d0. Selection digest: sha256:891cc23644e39140d565408a22ff4e12973c2a2a4a513311cbaff0a8b09061a0. Effective AgentSpec digest: sha256:104701101d96c8ef328dff2b0d34b33b4b98f8e11ffd983affab8a54bfbe6a9c -->

# Keep It Simple

Build the clearest complete solution. Simplicity means an elegant design with
few concepts and clear ownership. It does not mean the fewest lines, the least
work, or only the smallest patch.

Remove accidental complexity. Keep purposeful complexity when it achieves or
protects a real requirement. The full goal includes the user's stated vision,
production quality, safety, correctness, maintainability, developer experience,
and proportionate evidence. A credible near-term need can justify work now when
doing it later would create a worse boundary or substantial rework.

## Choose the clearest complete design

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

## Reuse before build

Run a proportionate reuse audit before adding a durable concept or a substantial
implementation path.

1. State the useful outcome and invariant without using the proposed new name.
2. Search the current code, tests, architecture decisions, live tracker, and Git
   history for that invariant and its effects. Search named sibling, dependency,
   legacy, or upstream projects when the task cites them as likely owners.
3. Compare behavior and ownership, not similar names. Record which component
   owns intent, mutable facts, effects, evidence, and recovery.
4. Check whether the tracked work is still open and whether a current owner or
   active implementation already exists. Reuse or rescope the narrowest owner
   before creating another issue.
5. Choose one result: reuse unchanged, extend the current owner, extract one
   shared lower layer, replace and delete the weaker path, or keep a temporary
   duplicate at a real external, version, availability, or recovery boundary.
6. For a temporary duplicate, name the boundary, the canonical future owner,
   the direct fallback, and a tested deletion or promotion gate. Do not call it
   reusable until a second real consumer preserves the same invariant.

Stop the audit when evidence is sufficient for the decision. Do not search every
repository or create a comparison document when a local symbol search and one
owner check answer the question.

If two active owners could become parallel frameworks, pause the dependent
implementation. Ask the owners to agree on the shared seam, or request focused
independent architecture review when the correct owner remains ambiguous.

## Prefer direct designs

- Prefer one authority, one owner, and one path for each effect.
- Prefer semantic or typed platform primitives over custom tracking state.
- Keep temporary provider or runtime details out of durable contracts.
- Re-resolve changing external state instead of preserving stale references.
- Remove incidental checks when they reject a valid flow.
- Add one narrow guard for a named failure instead of a general framework.
- Use an event or authoritative state transition before adding polling or retry logic.
- Reuse an existing boundary before adding another wrapper, adapter, or configuration option.
- Keep product-specific policy and native bindings with the product when a
  shared lower layer is extracted.
- Delete superseded code in the same migration when no real compatibility
  boundary requires both paths.

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

Reason: Simplicity means few concepts and clear ownership; cutting scope or proof only moves complexity to later.

Examples:
- A change adds a wrapper that only forwards calls. Remove the wrapper and call the owner directly.
- Similar code exists in a sibling project. Reuse or extract it with a clear owner instead of copying it.

Limits:
- Do not cut scope, quality, safety, or proof merely to reduce effort.
- Do not remove purposeful complexity that protects a real requirement.

Authority boundary: This skill guides writing and review only. It grants no source write, tool, provider, task, or effect authority.
