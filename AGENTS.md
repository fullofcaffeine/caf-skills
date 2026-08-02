# Global working rule

Before substantial work on a new task, use `$calibrate-reasoning-effort`, state
the recommended level, and explain why in one sentence. A label records intent;
it does not prove the runtime setting changed.

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
- Let Haxe infer, default, derive, validate, or generate statically knowable
  behavior when that removes repetition without hiding ownership or target
  cost. Use macros for compile-time invariants or drift-prone boilerplate, not
  cleverness; keep their emitted surface understandable and tested.
- Prefer module-level functions and values for stateless module-owned behavior.
  Do not create an all-static shell class unless class identity, construction,
  inheritance, an interface, metadata, macro discovery, or a host export shape
  requires it.
- Prefer named record-shaped inputs for DTOs, requests, outcomes, policies, and
  configuration. Avoid long positional constructors, especially more than
  five to seven scalar parameters or adjacent `Bool`, `Int`, and `String`
  values whose order is easy to confuse.
- Use externs to model real host/native APIs and keep them precise. Keep raw
  target facades available when compatibility or interop requires them, but
  prefer semantic Haxe wrappers when they improve safety and readability
  without changing target behavior.
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
