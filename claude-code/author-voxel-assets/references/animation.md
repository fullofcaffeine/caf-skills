# Voxel animation choices

A static voxel model stores shape and color. Animation needs a separate clip,
time, and playback contract.

## Select the smallest faithful representation

### Model frames

Use one complete voxel model for each key frame. This route fits enemies,
characters, liquids, smoke, and objects whose shape changes substantially.

Advantages:

- simple runtime selection;
- each frame remains easy to inspect in a voxel editor;
- no skeleton or skinning data is necessary.

Costs:

- repeated geometry increases package and memory size;
- interpolation between frames is not automatic;
- careless frames can wobble because their pivots or bounds differ.

Keep a common grid, pivot, scale, palette, and forward direction across the
clip. Use discrete playback first. Add interpolation only when it improves the
real camera view.

### Rigid parts

Split a model into named solid parts. Animate each part with translation,
rotation, or scale. This route fits doors, winches, tools, robots, and simple
characters with block-like limbs.

Advantages:

- one copy of each part can serve many poses;
- movement stays crisp and mechanical;
- collision can remain on a stable independent shape.

Costs:

- the format needs named parts, pivots, and a hierarchy;
- gaps and intersections can appear at joints;
- the runtime must define transform order.

### Skeleton and weighted geometry

Use a skeleton only when articulated motion needs joints that frame models or
rigid parts cannot express at an acceptable cost. This route fits a mature 3D
character pipeline, not the first animated voxel tracer.

Advantages:

- many clips can share one model;
- animation blending can be smooth;
- common character tools can edit the motion.

Costs:

- skinning, weights, bind poses, blending, and export rules add substantial
  engine and authoring complexity;
- a cube grid can deform poorly without a deliberate visual style;
- collision and gameplay state still need separate authority.

## Define the clip contract

Each reloadable clip needs:

- a stable name;
- an ordered frame or key list;
- positive frame durations or a documented sample rate;
- loop, hold, or one-shot behavior;
- a start and completion policy;
- a common pivot, bounds, scale, and forward direction;
- pause, reload, and missing-asset behavior;
- event markers only when gameplay needs them.

Keep visual playback separate from simulation. A sword hit, door unlock, or
enemy attack must use authoritative game state. Animation can show that state,
but it must not create hidden gameplay rules.

## Build one tracer first

Select one visible motion with a clear success condition. For example, animate
a relay crystal pulse, a winch crank, or one enemy idle clip. Load its assets,
play it in the real renderer, pause it, reload its content, and release its
resources. Expand to other clip types only after that path is coherent.

## Review the motion

Inspect the clip at its normal camera distance. Make sure that:

- its silhouette changes intentionally;
- its pivot does not jump;
- its feet or base do not slide;
- its frame rate fits the art style;
- its loop has no accidental pause;
- it remains readable against real lighting and terrain;
- it does not depend on a fixed camera-facing sprite plane.

Classic voxel replacements can inspire crisp frame-based motion. Do not copy
their assets, characters, palettes, or animation frames.
