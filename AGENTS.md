# Global working rule

Before substantial work on a new task, use `$calibrate-reasoning-effort`, state
the recommended level, and explain why in one sentence. A label records intent;
it does not prove the runtime setting changed.

## Oracle review escalation

- Use `$oracle-review` only for the hardest work: a consequential architecture,
  security, provenance, migration, release, or cross-repository decision that
  remains ambiguous after deep local investigation; repeated attempts that no
  longer converge on a stable invariant; or a critical completed task whose
  normal independent review is demonstrably incomplete.
- When that threshold is crossed, say why, stop disputed implementation, build
  the checked GPT-5.6 Pro handoff under `/tmp/oracle`, and wait for the human to
  return the response. Oracle is advisory and never replaces repository
  evidence, tests, CI, owner decisions, or the standard `show-me-your-work`
  reviewer. Do not invoke it for routine debugging, unfamiliar code, slow work,
  a large but bounded diff, or a generic desire for another opinion.

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
