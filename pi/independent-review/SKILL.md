---
name: independent-review
description: "Use when the owner asks for a brainstorm, a design review, or an independent review, says \"ask Fable\" or \"ask Oracle\", or asks \"are we aligned\". Also use when you consider whether a Fable or Oracle review is recommended."
license: "LicenseRef-Cafetera-Private-Unpublished"
---

<!-- GENERATED skill projection. Edit selected CML and source assets, not this directory. Package digest: sha256:17ca679e6d86b0e57c0302b40f1c79b3f2f237ecf82ce3dc18cffe90d0ade31e. Selection digest: sha256:05ad2eaa4674a8dcbdbee27a41bd7849c794f815d1f82c444ef632ce68d643dc. Effective AgentSpec digest: sha256:f0a61fd6c11cfac9c77cc34e2a7c463dfd6eaae1ce83acc8aaa2da270b0b653d -->

# Independent review

Send an agent to Caf's brainstorm and design-review routine at the moment the agent needs it.

## Find and use the independent-review routine

Run `caf describe caf:concept:model:independent-review-v0` and use the routine that it prints. Its status line copies the state of the record. That state is not an owner approval.

That record owns the routine. This skill does not copy it. If the `caf` command is not available, read `caf/workspace/IndependentReview.hx` in the Cafetera repository.

Reason: An agent wrote review briefs by hand because search did not find the routine. A skill description matches the words that the owner uses.

Examples:
- The owner says "ask Fable about this plan". Print the concept record, and then brief Fable as the record says.

Limits:
- No copy of the routine, and no claim that a harness loaded or followed this skill.

Authority boundary: This skill points at a record. It grants no source write, tool, provider, reviewer, task, or effect authority.
