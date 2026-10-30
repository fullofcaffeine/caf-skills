# Screenflow contract

Use this contract to simulate a product slice between visual selection and
implementation. Keep it small enough to review and complete enough to expose
missing behavior.

## Contents

1. [Records](#records)
2. [Required paths](#required-paths)
3. [Simulation](#simulation)
4. [Validation](#validation)
5. [Example](#example)

## Records

Use stable IDs and explicit refs. Adapt field names to the project's accepted
format. Do not create a new semantic authority only to match this outline.

### Story

- `id`
- actor and goal
- entry condition
- success and safe-exit conditions
- acceptance refs
- flow refs

### Scene

A scene is one surface in one meaningful state.

- `id`
- surface ref and state name
- visual candidate ref
- visible purpose and primary action
- authority or provenance cues the user must see
- responsive or native variant refs
- accessibility route

Typical state names include `loading`, `ready`, `empty`, `editing`, `offline`,
`invalid`, `permission-denied`, `stale`, `conflict`, `saving`, `success`, and
`recovery-required`. Include only states that can occur.

### Transition

- `id`
- source scene ref
- trigger: pointer gesture, keyboard gesture, command, system event, or timer
- preconditions
- requested action and its owner
- destination scene ref or terminal result
- visible result
- data and effect boundary
- failure destination or safe terminal outcome
- recovery transition ref
- evidence expectation ref

Record meaningful interaction, not incidental animation. A hover needs a row
only when it reveals necessary information or changes behavior.

### Flow

- `id`
- story refs
- ordered entry transition
- included scene and transition refs
- success exit
- cancel or safe exit
- recovery route
- cross-device or cross-channel handoff when applicable

## Required paths

Cover the paths that can occur for the slice:

- first use and returning use;
- ready and empty;
- create, inspect, edit, save, cancel, and undo where applicable;
- validation and stale input;
- offline and reconnect;
- unavailable dependency or provider;
- permission and authentication;
- conflict and retry or replay;
- destructive confirmation and recovery;
- pointer, keyboard, assistive-technology, and touch routes;
- compact, wide, and native-family variants that change interaction.

Do not invent states only to complete this list.

## Simulation

Walk each story from its entry condition to success and safe exit.

For each step, state:

1. what the user sees;
2. what the user or system does;
3. which owner receives the request;
4. what changes and what must not change;
5. the next visible state;
6. the failure and recovery route;
7. the evidence that will prove the implementation.

Use a table, a graph view, or a lightweight clickable prototype. Keep the
stable record set independently readable so a prototype implementation cannot
silently redefine behavior.

## Validation

Fail the design gate when any of these conditions is true:

- a story has no flow;
- a flow has no entry, success exit, or safe exit;
- a referenced scene or transition does not exist;
- a non-terminal scene has no outgoing transition;
- a failure state has no recovery or explicit terminal outcome;
- an action has no authority or effect owner;
- a transition changes accepted data through presentation state;
- a pointer-only path has no required accessible alternative;
- a visual has no screen/state role or disposition;
- an implementation task has no story and transition refs;
- evidence cannot distinguish success from believable failure.

## Example

```text
Story STORY-CAPTURE-01: capture a thought while offline

Scene SCENE-INBOX-READY
  surface: SURFACE-INBOX
  state: ready-offline
  visual: VISUAL-INBOX-WIDE-02

Transition TX-CAPTURE-OPEN
  from: SCENE-INBOX-READY
  trigger: keyboard "C" or pointer "Capture"
  owner: local Caffeine draft store
  to: SCENE-CAPTURE-EDITING
  failure: SCENE-LOCAL-WRITE-FAILED
  evidence: EVIDENCE-CAPTURE-OPEN

Transition TX-CAPTURE-SAVE
  from: SCENE-CAPTURE-EDITING
  trigger: keyboard "Command+Enter" or pointer "Save locally"
  owner: local Caffeine draft store
  result: one stable draft identity appears in Inbox
  must-not-change: accepted KB and remote provider records
  to: SCENE-INBOX-CAPTURED
  recovery: TX-CAPTURE-RETRY
  evidence: EVIDENCE-CAPTURE-RESTART
```
