---
name: product-designer
description: "Turn a product idea, feature, or UX correction into a reviewable outside-in design package: product intent, immutable visual candidates, owner disposition, complete screenflows, Application behavior, an implementation plan, and evidence. Use when designing or redesigning an app, screen, workflow, interaction, editor, responsive experience, or product slice before frontend implementation; when mockups must cover every user story and transition; or when an existing UI needs a durable design-to-code workflow. In Caf-managed projects, use inline CML and the narrowest Caf owners before native code."
license: "Apache-2.0"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:7cbadfa463347c9249a80bd6cb1a8ffb45730deb44be28021e9f841268adc8db. Selection digest: sha256:7c941a31cdaa09f3ab3967e23a3cab2edca54e5e1daa0d70bb927767883c26ab. Effective AgentSpec digest: sha256:78198771dea1121f96b42531e696b3202637b98ef1d06f37455e42c6d4a4179d -->

# Product Designer

Create order from product-design ambiguity. Move from intent to visual direction,
then simulate the experience, lower retained behavior to the product spec, and
only then implement it.

Do not treat a polished image as a working product. Do not treat a screenflow,
generated file, graph row, or model response as product authority or runtime
evidence.

## Follow the outside-in product-design gates

### Start with the project

1. Read the repository instructions and the current product, design, test,
   and recovery sources.
2. Check the live task and current implementation before proposing duplicate
   work. Preserve existing ownership and accepted design decisions.
3. Name the product slice, target users, desired outcome, platforms, known
   evidence, assumptions, constraints, authority boundaries, and non-goals.
4. Give every story, surface, state, transition, visual, and evidence
   expectation a stable ID. Reuse existing IDs where they already own meaning.

Use the repository's design directory. If it has no convention, use one bounded
directory such as `docs/design/<slice-id>/`. Do not create a second tracker or
semantic registry.

### Follow the outside-in gates

Do not skip a gate because later work looks easy. A gate can be a short artifact
when the product slice is small.

#### 1. Frame the product slice

Write a compact brief with:

- purpose and success outcome;
- users, jobs, and evidence-backed needs;
- assumptions and unresolved decisions;
- target platforms and adaptive constraints;
- data, semantic, task, provider, and effect owners;
- offline, permission, privacy, recovery, and destructive-action boundaries;
- explicit non-goals and the smallest useful release.

Ask one short question round only when an answer can materially change the
experience or implementation. Give a recommended default for each question.

#### 2. Establish visual direction

Inspect existing product UI, design tokens, accepted visual candidates, and
named references. Use donor products for behavior and design evidence only.

Generate or collect visual candidates when images materially clarify layout,
theme, density, hierarchy, responsive posture, or a complex interaction. Choose
the image route for the running harness:

- In Codex, use `$imagegen` for raster mockups.
- In Claude Code, which has no raster image tool, make each quick candidate as
  a code-native HTML, CSS, or SVG mockup and render it to PNG with Playwright.
  The PNG is the candidate. The mockup code is disposable and is not the start
  of implementation.
- In Claude Code, for a full package of GPT mockups, use `$oracle-review` with
  `caf-oracle --prompt-profile product-designer`. Use only the mockup files
  that its verified package export lists with digests.
- In another harness, use its own raster image tool or the code-native route.

Use `$frontend-design` only when implementation starts. Every route records
candidates the same way. Keep third-party identity, code, and assets out of the
result.

For each candidate, record:

- stable visual ID and file path;
- exact digest;
- target surface, state, viewport, and story refs;
- source and reference provenance;
- owner disposition: `accept`, `revise`, or `reject`;
- retained direction and intentional exclusions.

An accepted candidate guides presentation. It does not own behavior, data,
routes, components, or implementation.

#### 3. Author the screenflow

Read [screenflow.md](references/screenflow.md) completely. Build a screenplay of
the product before writing native UI code.

The screenflow must cover every retained user story and meaningful interaction:
entry, visible state, click or gesture, keyboard route, command or system event,
transition, result, failure, recovery, and exit. Include responsive and native
variants when they change the interaction.

Simulate each path as a deterministic walkthrough. A clickable prototype can
augment the walkthrough, but it cannot replace the stable transition model.
Stop when a story has an orphan state, an ownerless action, an unreachable
success state, or a failure with no safe outcome.

#### 4. Lower retained behavior to the product spec

In a Caf-managed project, read [caf-mapping.md](references/caf-mapping.md)
completely. Update the narrowest inline CML owner before implementation:

- Application for portable purpose, capabilities, surfaces, and conformance;
- Application Target for native-family expectations;
- Test Strategy and Coverage for lanes and behavior-to-evidence links;
- Assembly for exact selected relationships;
- Infra, Ops, and CafOps for desired topology, operation intent, and ordered
  planning;
- artifacts, observations, evidence, actions, and receipts for native proof.

Treat the screenflow as a readable and executable projection over those stable
refs until a reusable typed gap is proved. Do not add a universal screen,
component, or transition schema merely to store a design document.

Outside Caf, preserve the same IDs and traceability in the project's accepted
specification format.

#### 5. Plan one vertical tracer

Select the smallest path that proves the architecture and the main experience.
Link each implementation task to exact story, surface, transition, visual, and
evidence refs. Keep product policy in the product and reusable fixes in their
owning libraries.

Before coding, confirm that:

- the visual candidate has an explicit disposition;
- every tracer transition has a specified result and failure path;
- the authority and mutation owner are visible;
- accessibility and non-pointer routes are defined;
- direct native build, debug, export, and recovery paths remain available.

#### 6. Implement through the native stack

Use `$frontend-design` for frontend work. Follow the repository's language,
framework, target, typing, and generated-source rules. Implement stable IDs and
observable behavior from the spec; do not translate mockup pixels blindly.

Keep layout, camera, selection, drawing, preview, cache, and other presentation
state local and deletable unless an accepted owner says otherwise.

#### 7. Verify and reconcile

Run focused checks first, then the repository's required gate. Collect evidence
for behavior, accessibility, responsive or adaptive layout, offline and
recovery behavior, performance where relevant, and visual direction.

Walk every screenflow again against the working product. Record each row as:

- `proved`: observed evidence satisfies the transition;
- `drift`: the implementation intentionally differs, with reason and evidence;
- `failed`: the product does not satisfy the retained behavior;
- `blocked`: a named external or human decision is required.

Update the visual disposition, screenflow, product CML, tests, and task evidence
in the same change when product meaning changes. Do not rewrite an expectation
to hide a failing implementation.

### Use Oracle only for independent help

Use `$oracle-review` with its product-designer profile when consequential product
decisions remain ambiguous, a broad independent review can prevent expensive
rework, the requester explicitly delegates product discovery to Oracle, or a
harness without a raster image tool needs a full mockup package.

Oracle can propose questions, stories, flows, and mockups. The driving agent
must inspect the response, record a local disposition, and lower only accepted
meaning into the ordinary workflow. Do not dispatch Oracle for routine local
design work, and do not copy its request ledger or browser lifecycle into this
skill.

### Completion checklist

- The brief distinguishes facts, assumptions, owners, and non-goals.
- Visual candidates have digests and explicit dispositions.
- Every story has a complete simulated path and no orphan refs.
- Application scenarios or the project spec own retained behavior before
  native code.
- Implementation tasks trace to stories, transitions, visuals, and evidence.
- Working product evidence covers the relevant happy, failure, recovery,
  accessibility, responsive, offline, and performance paths.
- Intentional drift is explicit.
- Generated views and client projections can be deleted and rebuilt.

Reason: A mockup or screenflow that skips a gate hides orphan states, ownerless actions, and unproved behavior until implementation, where they cost the most to fix.

Examples:
- In Claude Code, a dashboard needs a quick layout candidate. Write one HTML and CSS mockup, render it to PNG with Playwright, and record the PNG with the same stable visual ID, path, digest, and owner disposition as any other candidate.
- In Codex, a dashboard needs a layout direction. Generate two raster candidates with $imagegen, record each with a stable visual ID, path, and digest, and ask the owner to accept, revise, or reject each one.

Limits:
- Do not call an image API directly; that route needs a declared secret and owner approval.
- Do not treat a mockup image, its source code, or an Oracle response as product authority or implementation.

Authority boundary: This skill guides product design. It grants no source write, tool, provider, image, Oracle, task, or effect authority.

## Included assets

These files are part of the exact package closure. Including a file grants nothing by itself. This guidance-only package declares no actions or effects and includes no helper to run.

- `references/caf-mapping.md` — reference; none
- `references/screenflow.md` — reference; none
