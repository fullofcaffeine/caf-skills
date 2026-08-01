---
name: explain-technical-work
description: Make specialized explanations understandable to capable newcomers without losing precision. Prefer familiar everyday language, avoid unnecessary technical or organization-specific jargon, and explain any exact specialist term that must remain. Use whenever Codex drafts, rewrites, or reviews material about a complex domain—including pull requests, engineering changes, research, data analysis, operations, security, policy, incidents, decisions, procedures, status reports, handoffs, documentation, or user guidance—that may assume missing project history, obscure why the work started, or leave practical value unclear.
---

# Explain Technical Work

Write so a reader can understand the practical problem and outcome before they need specialized or organization-specific knowledge. Preserve the full truth; improve the order and explanation of that truth.

Apply the method to the terms actually used in the current work. Do not carry a fixed glossary, a list of forbidden words, or assumptions from one project or field into another. Terms and examples in this skill illustrate the method; they are not special cases that define its scope.

## Plain language is the default

Do not make the reader learn internal vocabulary when familiar words can state
the same fact accurately. Before defining a specialized term, ask whether it
can simply be replaced. If it can, use the familiar wording and omit the term.

Keep an exact technical or organization-specific name only when the reader
needs it to run a command, find code, review a contract, search documentation,
or distinguish it from a genuinely different concept. Introduce the ordinary
action or relationship first, then give the exact name in parentheses when
useful. Explain the term at its first use in the same sentence or immediately
after it; never require the reader to infer its meaning or consult a glossary.

Replace compressed labels with what people or programs actually do. For
example, depending on context, wording such as “governance,” “scorecard,”
“lane,” “topology,” or “provenance” may be clearer as “repository safety
rules,” “which claims each test proves,” “one named test command,” “how the
parts connect,” or “where the expected result came from.” These are examples,
not a fixed replacement list. Choose wording from the real situation.

Apply this rule to titles, headings, summaries, tables, and bullets—not only to
the explanatory paragraphs. Avoid strings of unexplained specialist nouns
even when each individual word is technically correct.

## Workflow

### 1. Set the reader's starting point

Assume a capable reader who understands the broad field but is new to this particular system, study, organization, or procedure unless the task states otherwise. Do not assume knowledge of local acronyms, component names, process stages, issue labels, metrics, models, policies, team conventions, or specialized meanings.

State the practical outcome first:

- What did not work or was hard before?
- What works or becomes safer/easier now?
- Who notices the difference?
- What remains unfinished?

### 2. Reconstruct the origin and user value

Make the explanation stand on its own. A reader should not need to have
followed an earlier issue, review, incident, or conversation to learn why the
work exists.

Explain the causal chain:

1. **Normal workflow:** What was the user, operator, contributor, or system
   trying to do?
2. **Trigger:** What observation, failure, audit, support case, or missing
   guarantee revealed the need?
3. **Practical exposure:** What could the person experience—wrong output,
   stale results, unsafe behavior, manual work, slow feedback, uncertainty, or
   a release risk?
4. **Why the existing protection was insufficient:** What did it check, and
   what important path did it leave unproved?
5. **Value after the change:** What can the person now do more safely, quickly,
   predictably, or confidently?

Testing and infrastructure changes still need user value. If they intentionally
do not change successful runtime behavior, say that plainly and explain the
benefit as earlier detection, safer upgrades, reliable editor/watch builds,
repeatable releases, clearer failure recovery, or another concrete assurance.
Do not describe “more coverage” or “a new owner” as the value by itself.

If prior context is important, summarize the necessary fact in the current
document and link directly to the earlier issue, PR, incident, or decision.
Never use a link as a substitute for the summary. If the real origin is
unknown, say which evidence is available instead of inventing a story.

### 3. Give the smallest useful mental model

Before naming specialized concepts, explain the smallest useful relationship in ordinary verbs. Adapt the shape to the subject, for example:

```text
starting state or input -> action, decision, or transformation -> observable result
```

For a hierarchy, comparison, causal claim, or lifecycle, use the corresponding small mental model instead of forcing everything into a pipeline. Name the formal concept or owning component only after explaining what it does. Use a small example when prose alone would leave the reader guessing.

### 4. State the positive operational contract

When explaining a mechanism, rule, annotation, flag, permission, API, policy,
compiler feature, or relationship, do not lead with a list of things it does
not do. First explain its positive contract in concrete terms:

1. **Actor or owner:** What component, person, process, or value applies the
   rule or performs the action?
2. **Recipient or target:** Who or what receives access, data, control, state,
   or a result?
3. **Granted operation or transformation:** What exact action becomes allowed,
   required, selected, checked, generated, retained, or rejected?
4. **Scope and timing:** Which declarations, values, requests, phases, builds,
   or lifetimes are affected, and when?
5. **Reason:** What concrete need makes this mechanism appropriate here, and
   why is the ordinary/default path insufficient?
6. **Observable consequence:** What changes in source checking, generated
   output, runtime behavior, stored data, network behavior, user experience,
   or failure handling?

Add limitations and non-effects only after that contract is clear. When saying
“this does not provide ownership,” “this is compile-time only,” or another
negative distinction, name the separate mechanism that actually owns or
enforces that concern when it matters. Do not collapse independent axes such
as access, visibility, lifetime, ownership, validation, execution, storage, and
transport into one vague idea.

For a transitional mechanism, also state what it stands in for and the
condition that should remove or revisit it. For a durable mechanism, state the
invariant that keeps its authority bounded. Keep the explanation proportional:
a compact comment may cover the contract in three sentences, while a public or
surprising boundary may need a small before/after example.

Use this as a rejection check:

```text
Weak:  X is compile-time only; it emits no runtime check.
Useful: X lets A perform operation B on C during phase D. We use it because E.
        The compiler then produces F; runtime concern G is enforced separately
        by H, so X emits no runtime check.
```

The letters are relationship placeholders, not a required writing template.
If the reader still cannot say “who can now do what, to which thing, when, and
with what consequence,” the explanation is incomplete.

### 5. Audit terminology

Treat a term as jargon when a newcomer could reasonably assign it a different meaning. This includes:

- acronyms, symbols, abbreviations, and local labels;
- ordinary words used in a narrow field-specific or organization-specific way;
- internal components, methods, metrics, categories, protocols, stages, or policy names;
- noun stacks and compressed phrases that hide several operations;
- metaphors whose concrete behavior is not stated.

At first use, define the term with this pattern:

```text
<term> means <plain description> here. It matters because <practical consequence>.
For example, <small concrete case>.
```

Use that pattern as a check, not as mandatory prose. A parenthetical definition, short example, diagram, or earlier explanation may be clearer. Do not rely on typography or capitalization as explanation.

An accurate technical term is not automatically the clearest wording. Prefer a
familiar alternative when it preserves the meaning. When the exact term must
carry the argument, define it at first use and retain it where readers need it
for search, implementation, review, or further study.

### 6. Replace compressed labels with actions

When a dense label compresses several actions, unpack it into an ordered sequence of verbs. For example, a phrase such as “version-checked coordinated update” might mean:

1. record which input version the work used;
2. compute the proposed changes without publishing them;
3. reject the result if the input changed;
4. publish all changes together if validation succeeds.

After explaining the sequence, introduce the formal or local name if it helps later discussion. Do not treat this example's wording as a preferred vocabulary for unrelated domains.

### 7. Show before, problem, and after

Use the most concrete evidence available:

- the relevant starting input, observation, rule, configuration, or state;
- the actual wrong result, behavior, diagnostic, uncertainty, risk, or practical cost;
- the corrected result, changed behavior, or new decision after the work.

When output was never produced, say so and show the real failure boundary. Never invent a plausible-looking output. Label simplified examples as illustrative.

Explain observable consequences in the vocabulary of the current domain—for example ordering, uncertainty, retries, identity, permissions, data loss, latency, compatibility, cost, safety, or failure handling. Do not substitute an inventory of internal names for the practical result.

### 8. Layer detail instead of removing it

Use this order:

1. practical outcome;
2. concrete example;
3. plain-language mechanism;
4. exact internal names and invariants;
5. verification, limitations, and deferred work;
6. authoritative references.

Keep exact identifiers, formulas, classifications, and source names when they support searchability, reproduction, implementation, or review. Introduce them after the reader knows why they matter.

### 9. Add useful references

Link directly to the best next source: a primary study, dataset, standard, policy, public documentation, source contract, decision record, focused test, benchmark method, or incident record. Describe what each link helps the reader understand.

Do not use a pile of links as a substitute for explanation. Prefer primary sources for claims about behavior.

### 10. Run the first-read check

Before publishing, verify:

- Can a capable newcomer explain the problem and outcome after one read?
- Can the reader state what caused this work to start and how it improves a
  real workflow, rather than merely naming the internal mechanism?
- Is every specialized or overloaded term defined before it carries the argument?
- Could any specialized term be replaced with familiar wording without losing
  meaning, and has every term that remains been explained at first use?
- For every important mechanism, can the reader identify the actor, target,
  granted operation or transformation, scope, reason, and observable
  consequence?
- Do negative distinctions come after the positive contract and name the
  separate mechanism responsible for the excluded concern when relevant?
- Are compound labels expanded into concrete steps?
- Does the example connect input to real behavior or output?
- Are limitations and uncertainty explicit?
- Can an expert still find exact names, invariants, tests, and references?

If understanding requires opening the implementation first, rewrite the explanation.

## Output-Specific Guidance

### Change proposals and decision records

Use clear **Why**, **What**, and **How** sections when they fit. Add the concrete before/problem/after example near **Why**. Explain tradeoffs and rejected alternatives in terms of outcomes, maintenance, evidence, risk, cost, and affected people before internal structure.

### Pull request descriptions

Write a PR as a standalone review document, not as a patch inventory or an
issue-thread continuation. Near the top:

1. identify the normal user or contributor workflow;
2. define the relevant subsystem in plain language;
3. explain what triggered the change and link prior context when useful;
4. show the concrete failure, gap, or uncertainty and its consequence;
5. state the user-facing value, including when that value is prevention or
   confidence rather than new visible behavior.

Then explain the implementation boundary, examples, verified profiles or
environments, limitations, and exact tests. Introduce internal class, plan,
fixture, Bead, or workflow names only after the reader understands why they
matter. A heading named **Why** is not sufficient when its content begins with
repository-local facts such as “there was no owner” or “the gate was missing.”
Translate those facts into the workflow and risk they left unprotected.

### Short change records

Keep the subject concise. In the body, explain the previous state, the new state, why the difference matters, verification, and intentionally deferred scope. Avoid an inventory of files, fields, or internal labels as the main explanation.

### Problems, incidents, status reports, and handoffs

Lead with the current observable state, impact, blocker or uncertainty, next meaningful outcome, and evidence. Define local status labels, severity categories, stages, and confidence terms when they first appear.

### Guides, documentation, and announcements

Separate the reader's action and expected result from deeper internals. Put the practical path first and link detailed reasoning, implementation, methodology, or governance material instead of forcing it into the quick path.

### Research, analysis, and policy

State the question, evidence, conclusion, confidence, and limitations separately. Define measures and categories before interpreting them. Distinguish observation from inference and recommendation, and do not make a causal or normative claim sound like a directly measured fact.

## Quality Boundary

Do not confuse newcomer-friendly language with simplification that changes the claim. Never:

- hide an important limitation;
- describe an internal milestone as user-ready behavior;
- replace an exact failure with a vague success/failure statement;
- use an analogy that contradicts the real mechanism;
- remove technical detail merely because it needs explanation;
- assume that a familiar-looking word is universally understood.

For cross-domain rewrite examples, read [references/examples.md](references/examples.md).
