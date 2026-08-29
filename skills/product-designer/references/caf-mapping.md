# Caf product-design mapping

Use existing Caf owners to describe a product from the outside in. Craft is the
highest owner-facing view of the product-design workflow, not a universal
schema that absorbs every narrower contract.

## Contents

1. [Ownership map](#ownership-map)
2. [Visual and screenflow artifacts](#visual-and-screenflow-artifacts)
3. [Skill ownership](#skill-ownership)
4. [Recovery](#recovery)

## Ownership map

| Product-design meaning | Narrow Caf owner |
| --- | --- |
| Portable product purpose and capabilities | Application |
| Portable screen or workspace meaning | Application Surface |
| Given, When, Then behavior | Application conformance case |
| Native-family expectations | Application Target |
| Outside-in recommendations and composed design view | Craft |
| Test topology and behavior coverage | Test Strategy and Test Coverage |
| Exact selected records and implementations | Assembly |
| Desired infrastructure topology | Infra |
| Operation intent | Ops |
| Deterministic plan and evidence order | CafOps |
| Native mutation request | Action and effect policy |
| Attempted or completed native effect | Artifact, observation, evidence, and Receipt |
| Mutable provider, task, Git, client, or runtime fact | Its native owner |
| Navigation and relationship view | Rebuildable graph, VFS, headless, or search projection |

Use inline CML-HX for declarative project meaning when the selected package
supports it. Use ordinary typed Haxe for composition, validation, algorithms,
and native adapters that do not belong in declarative CML.

## Visual and screenflow artifacts

A visual candidate is immutable evidence with a digest and disposition. It can
be linked to a surface and state. It does not own product behavior.

A screenflow is a design-time projection over stable Application Surface,
conformance, command, event, evidence, and target refs. It can drive validation,
graph views, walkthroughs, prototype playback, and implementation planning.
It does not create a second application model.

Promote a reusable screenflow schema only after a minimized fixture proves an
invariant that existing typed owners cannot express and a second independent
consumer confirms the same meaning.

## Skill ownership

- AgentSpec owns agent guidance and applicability rules.
- Skill Package owns reusable package identity, exact static assets, source
  locks, supported clients, and AgentSpec links.
- Skill Selection owns exact package and parent choices for a workspace.
- WorkContext owns evidence admitted to one run.
- Native clients own installed directories, sessions, tools, and availability.
- Graph and VFS views make the package discoverable. They do not activate it.

Oracle is an optional external planning or review adapter. Oracle responses are
advisory evidence until the driving agent records a disposition and lowers
accepted meaning through the normal owners.

## Recovery

The graph can be the user-facing recovery entry point, but it is not the backup.

Use this chain:

```text
authored CML selections
  + exact Git/source locks
  + digest-verified backup artifacts
  + machine-local bindings
  -> CafOps materialization plan
  -> native filesystem/client actions
  -> generated skill and configuration projections
  -> receipts and fresh verification
  -> rebuilt graph/VFS/headless/search views
```

Git remains source-version authority. Backup artifacts preserve recoverable
bytes. Local bindings choose physical directories without putting machine paths
in portable CML. Secrets remain provider-owned references. Delete generated
client directories and graph indexes during recovery tests, then prove that the
same selected inputs reproduce the expected package and projection digests.
