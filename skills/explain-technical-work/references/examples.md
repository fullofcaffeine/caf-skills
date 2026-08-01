# Cross-domain examples

Use these only as demonstrations of the method, not as a glossary, a trigger list, or canned wording. Derive the terms that need explanation from the task at hand.

## Internal testing language

Compressed:

> Add product-surface scorecards with reciprocal lane ownership and provenance.

Clearer:

> Record what each part of the product claims to support and which named tests
> actually prove it. Check the relationship in both directions so a passing
> browser test cannot be borrowed as evidence for an unrelated command-line
> feature. For each expected result, also record where that expectation came
> from.

If a reviewer needs the exact configuration names, introduce them afterward:
the repository stores this relationship in its `productSurfaces` entries, and
calls each named test command a `lane`.

## Software architecture

Compressed:

> Add revision-aware cache invalidation.

Clearer:

> The service used to reuse cached results without proving they came from the current configuration. It now records the configuration version with each result and discards the result when those versions differ. Here, “invalidation” means deciding that a cached value is no longer safe to reuse.

## Data migration

Compressed:

> Perform an online dual-write cutover with backfill reconciliation.

Clearer:

> While the old database remains live, new writes go to both databases. Historical rows are then copied to the new database, and a comparison job reports anything that differs. Traffic moves to the new database only after those checks pass. “Dual write” is the temporary period in which one request updates both stores.

## Infrastructure

Compressed:

> Use an atomic blue-green deployment.

Clearer:

> Build the new version in a separate environment, test it without serving users, and then switch the router from the old environment to the new one in a single routing change. If health checks fail, keep routing to the old version. “Blue-green” is the practice of keeping those two complete environments side by side during the switch.

## Machine learning

Compressed:

> Gate promotion on distribution-drift metrics.

Clearer:

> Before replacing the current model, compare the new model's input and output distributions with the validated baseline. Block release when the agreed metrics move beyond their limits. “Distribution drift” means that the data pattern seen by the model has changed enough that past evaluation may no longer predict current behavior.

## Security

Compressed:

> Rotate the signing root and preserve trust continuity.

Clearer:

> Introduce a new top-level signing key while clients still trust the old one. Publish a signed transition record that lets clients verify the new key through the old key, then remove the old key only after supported clients have updated. “Trust continuity” means clients can verify the change without accepting an unverified key.

## Pre-output failure

Misleading:

> Before, the tool generated an unsafe configuration.

Accurate when no output existed:

> Before, validation stopped the build before any configuration was generated:
>
> ```text
> policy conflict: two owners selected the same resource
> ```
>
> The change makes that diagnostic identify both owners and the configuration step that introduced the conflict. It does not claim that an old generated file existed.

## Mechanism described only by non-effects

Too shallow:

> The annotation is compile-time only. It creates no runtime permission check
> and does not own the referenced value.

Clearer:

> The annotation tells the language type checker that one named collaborator
> may call this otherwise private constructor. Other callers still receive the
> normal private-access error. We use the exception so construction stays
> centralized without making the constructor public to the whole program.
> After access is accepted, code generation emits the same constructor call it
> would emit from inside the declaring type; no runtime permission object or
> branch is added. The constructed value's lifetime is still governed by the
> program's separate ownership rules.

The reusable lesson is not about a particular annotation. Explain the actor,
recipient, newly allowed operation, scope, reason, generated or runtime
consequence, and then the separate rules behind important non-effects.

## Operational flag

Too shallow:

> Dry-run mode does not publish anything.

Clearer:

> Dry-run mode reads and validates the same inputs as a real publication,
> computes the proposed changes, and reports what would be written, but stops
> before the commit step. Operators use it to review target selection and
> validation errors without changing remote state. It may still perform reads
> and local computation; transaction and authorization rules remain the
> responsibility of the real publish step.
