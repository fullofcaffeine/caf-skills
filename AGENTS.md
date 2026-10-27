# Global working rule

Before substantial work on a new task, use `$calibrate-reasoning-effort`, state
the recommended level, and explain why in one sentence. A label records intent;
it does not prove the runtime setting changed.

## Finish owned pull requests

Creating or taking over a pull request includes ownership through review,
required checks, merge, and reconciliation. A push or an open PR is a checkpoint,
not completion. An explicit draft-only or review-only request limits this duty.

- Finish or unblock an existing owned PR before opening another. A documented
  dependency stack or independent work during an external block is an exception.
- Keep each PR bounded. Once its acceptance criteria and required checks pass,
  complete the authorized merge. Do not wait for unrelated product milestones
  or keep adding unrelated features to the same PR.
- Monitor checks on the current revision, address review feedback, and repair
  failures. A pending check is not a completed task. Do not restart a live check
  merely because a status observation timed out.
- Respect required approvals, branch protections, ownership, and explicit user
  stop instructions. Never bypass them to make the PR count smaller.
- If an external blocker prevents merge, keep the task open. Record the PR,
  exact blocker, responsible owner, evidence, and next action in the tracker.
  Recheck that blocker at the next continuation; do not leave an unexplained draft.
- After merge, verify the intended changes on the default branch. Reconcile the
  task and incorporated PRs, and clean up only owned branches or worktrees that
  contain no unique work. A superseded PR can be closed with a successor link;
  its unmerged work remains tracked until the successor lands.
- Report a PR task complete only after verified merge, or an explicit withdrawal
  or supersession that preserves the remaining work and its owner.

## Skill installation

Before you add or install a Codex skill, read `skills/README.md` and obey its
source ownership and installation rules.

## Beads client safety

Before any Beads operation in a repository, use its documented Beads wrapper
when present. Otherwise run `command -v bd`, `bd version`, and
`bd --readonly info --json`. Continue only after the read-only open succeeds
without schema skew. This handshake prevents an old client from touching a
newer database and prevents a newer client from silently migrating an older
database during ordinary work.

Use only that reviewed executable for the session. Do not write through
`go run ./cmd/bd`, package-manager aliases, temporary builds, bundled agent
clients, or `--ignore-schema-skew`. If schemas differ, stop writes and use the
`$beads` recovery workflow. Migrations are explicit toolchain work, not a side
effect of claiming or updating an issue.

## Haxe best practices

Apply these defaults in Haxe repositories unless a closer `AGENTS.md` defines a
stricter or target-specific contract.

- In Haxe 4 code, declare optional structure fields with `?`, such as
  `final ?name:String` or `var ?name:String`; do not introduce `@:optional` for
  that purpose. Keep field absence distinct from `Null<T>` and from optional
  function arguments, and preserve the target boundary's exact null/undefined
  semantics.
- Keep ordinary code strongly typed. Do not use `Dynamic`, `Any`, `untyped`,
  `Reflect`, unchecked `cast`, raw target injection, or broad host-language
  types as shortcuts around a design problem. When an external, compiler, or
  native API makes one unavoidable, contain it in the smallest boundary,
  validate immediately, return a concrete type, and document the reason and
  safety invariant beside the escape.
- Parse JSON, configuration, macro values, filesystem input, CLI input, and
  foreign-runtime data at explicit boundaries. Convert them immediately into
  precise typedefs, classes, abstracts, enums, or validated recursive value
  types; do not let untyped shapes flow into domain logic.
- Prefer Haxe-native modeling: concrete structural types, abstracts/newtypes,
  enum abstracts or typed enums for closed domains, generics, exhaustive
  pattern matching, typed adapters/codecs, and compiler diagnostics. Use raw
  strings primarily at protocol, CLI, JSON, filesystem, and compatibility
  boundaries, then narrow them as soon as practical.
- Actively look for distinctive Haxe features that materially improve the
  implementation or developer experience instead of treating Haxe as a thin
  syntax layer over the target language. Prefer compile-time typing, abstracts,
  enums and pattern matching, metadata, conditional compilation, and macros
  when they make ownership clearer, prevent invalid states, remove drift, or
  produce better diagnostics. Keep target-native code at genuine interop and
  tooling boundaries, and choose each feature for a concrete benefit rather
  than novelty.
- Let Haxe infer, default, derive, validate, or generate statically knowable
  behavior when that removes repetition without hiding ownership or target
  cost. Use macros for compile-time invariants or drift-prone boilerplate, not
  cleverness; keep their emitted surface understandable and tested.
- Prefer module-level functions and values for stateless module-owned behavior.
  Do not create an all-static shell class unless class identity, construction,
  inheritance, an interface, metadata, macro discovery, or a host export shape
  requires it.
- Keep source files cohesive, readable, and easy to review. Split a file when
  it accumulates independent responsibilities, lifecycle owners, change
  reasons, or test seams; name the resulting modules after the behavior they
  own and keep their boundaries strongly typed. Do not wait for a file to
  become a large catch-all, but also avoid mechanical one-type-per-file
  fragmentation when closely related private types form one clear module.
- Prefer named record-shaped inputs for DTOs, requests, outcomes, policies, and
  configuration. Avoid long positional constructors, especially more than
  five to seven scalar parameters or adjacent `Bool`, `Int`, and `String`
  values whose order is easy to confuse.
- Use precise externs first when Haxe consumes an existing host or target
  library. Use the library's exported API directly when the compiler can
  represent it safely. Do not add a handwritten target-language wrapper only
  because the dependency uses the target language. If a binding generator
  exists, generate the required externs and inspect every untyped or
  unsupported fallback.
- If direct extern use exposes a reusable compiler gap, reduce it to a
  framework-neutral fixture. Fix the gap in the compiler repository through
  its normal isolated worktree, review, and merge process. Update the
  consumer's compiler lock only after the compiler change merges. Then
  regenerate the target output and prove the original application path.
- Keep handwritten native code only for an unexported API or a proven unsafe
  or unsupported interop boundary. Document the native requirement, typed
  contract, effects, tests, removal condition, and reason that an extern or
  compiler fix is insufficient. Native code must not own product policy.
- Treat authored Haxe as the source of truth. Never repair generated target
  files to make a check pass. Generated JavaScript, TypeScript, PHP, Rust, Go,
  Ruby, and other target output is still a product and review surface: inspect
  it for readable types, names, imports, evaluation order, native idiom,
  source correlation, and avoidable runtime scaffolding.
- Fix generic compiler, standard-library, or lowering gaps at their lowest
  reusable owner with a reduced framework-neutral fixture. Do not encode
  downstream paths, product schemas, names, diagnostics, or generated text as
  compiler recognition rules.
- For meaningful behavior, start with the smallest faithful failing contract
  and an independently authored expectation or specification. Preserve the
  focused regression, then prove one vertical tracer bullet through authored
  Haxe, generation/compilation, native target checking, and a real runtime or
  system observer before multiplying fixtures.
- Add concise HaxeDoc for non-obvious modules, types, macros, externs, metadata,
  lifecycle or security boundaries, and complex functions. Explain why the
  abstraction exists, what contract it preserves, how it works, and any
  important target or safety constraint; do not narrate obvious assignments.

## Oracle planning and review

- Treat the globally installed `$oracle-review` skill as the canonical authority
  for Oracle eligibility, planning and review modes, caf-oracle automation, and
  composition with `$show-me-your-work`. Load and follow the skill rather than
  duplicating its criteria or maintaining a separate manual handoff here.

## Public attribution and privacy

- Do not put a person's full or legal name in public-facing repository
  content, including commits, pull requests, issues, comments, release notes,
  documentation, generated artifacts, or agent-provenance sections, unless
  that person explicitly requests the exact public use.
- Use a role such as `repository owner`, `maintainer`, or `requester`, or an
  approved public handle when attribution is needed. Apply the same rule to
  private repositories that may later become public.
- Before publishing or pushing public-facing text, scan the authored content
  for full-name references and replace them with role-based attribution. Do
  not rewrite Git author metadata or existing history unless explicitly asked.

## Commit Messages

- Keep the conventional-commit subject concise, then add a useful commit body
  for every non-trivial change. Write the body in friendly, beginner-readable
  language so someone who does not already know the project or domain internals
  can understand what problem was solved.
- Explain what changed, why it matters, and how it was verified. Call out
  important behavior or output changes and name any intentionally deferred
  scope so the commit does not imply broader closure than it provides.
- Prefer concrete descriptions of the old and new behavior over a list of
  filenames or internal type names. Technical details are welcome, but
  introduce them in plain language and make the practical outcome clear first.

## Interactive host responsiveness

- Treat long, CPU- or memory-intensive local builds, full test suites, native
  compiles, renders, and packaging as background work when an interactive
  editor shares the host. Apply background scheduling once at the process root
  so every child inherits it. On macOS, use
  `taskpolicy -b nice -n 10 ./bin/check` when both commands are available.
  On other hosts, use `nice -n 10 ./bin/check` when `nice` is available.
  Use a repository-owned background wrapper when one exists.
- Keep Codex, its app server, the editor, interactive development servers,
  watch loops, live play sessions, and performance measurements at their
  intended priority. Reduced scheduling priority is a responsiveness control,
  not valid timing evidence.
- If an active background process tree causes contention, verify its exact root
  command and ownership before using `renice 10 -p` on that root and its current
  descendants. Do not target broad process names, unrelated work, or kill a
  process unless it is confirmed stale and the user authorized termination.
