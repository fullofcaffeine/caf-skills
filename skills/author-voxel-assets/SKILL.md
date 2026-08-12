---
name: author-voxel-assets
description: Design, create, convert, review, and integrate voxel models such as MagicaVoxel `.vox` assets. Use when Codex must replace a flat world sprite with a real volume, author a voxel prop or character, preserve a 2D icon as reference or fallback, add deterministic model generation, improve voxel silhouettes or palettes, plan voxel animation, or review voxel provenance and runtime integration.
---

# Author voxel assets

Create a real volume that reads well during play. Do not treat voxel work as a
mechanical conversion of every source pixel into a cube.

## Establish the contract

Inspect the repository before you edit an asset. Identify:

- the model format and version;
- the editable source of truth;
- the runtime loader and coordinate system;
- the scale, pivot, forward direction, and world bounds;
- the palette and art direction;
- the asset manifest, license, and source record;
- the regeneration, validation, packaging, and visual-review commands;
- the static or animated behavior that the game claims.

Do not assume that `.vox` means MagicaVoxel or that one loader supports every
chunk in that format. Use the loader's admitted format as the exact boundary.

## Choose an authoring route

Use an existing repository route when it produces maintainable source and
reviewable output.

1. Use an editor-owned `.vox` file when artists edit that file directly.
2. Use a deterministic builder when code or structured data owns the shape.
3. Use a conversion tool only when the input and conversion rule are durable.

An LLM can propose geometry, palettes, or source edits. It is not part of a
deterministic build unless the repository explicitly pins model output as a
reviewed primary asset. Never require an online model to rebuild shipped data.

For a 2D reference, retain its identity and visual language. Re-author its
depth, side, back, underside, and contact with the ground. Keep the 2D image
for an icon or fallback when that remains useful.

## Author the model

Start with broad forms and inspect the silhouette from the expected camera
angles. Add details only after the volume reads correctly.

- Give the object a clear front, side, and back.
- Use material groups and color ramps instead of random surface noise.
- Keep thin parts thick enough for the camera distance and renderer.
- Put the pivot where placement, rotation, or animation needs it.
- Keep decorative geometry separate from collision authority.
- Use the smallest useful grid. More cells do not guarantee better art.

Do not extrude one cube for every opaque sprite pixel by default. That creates
a textured slab, preserves edge noise, and gives no authored side silhouette.

## Integrate without special cases

Put model selection, transform, scale, state, and clip names in reloadable data
when the product supports data-driven content. Keep the engine generic. Do not
add campaign, level, character, or prop names to a shared renderer.

Use one loader owner for each native model resource. Cache or share only with
an explicit lifetime. Release every loaded resource exactly once. Keep a clear
fallback for missing or rejected data when the product requires one.

## Validate the result

Use independent checks for different claims:

1. Regenerate the model twice and compare bytes when generation is deterministic.
2. Validate its signature, dimensions, palette, manifest hash, and package path.
3. Load it through the real runtime boundary.
4. Review it from several gameplay angles and normal interaction distances.
5. Check its scale, pivot, grounding, yaw, occlusion, lighting, and fallback.
6. Inspect its animation timing and pause behavior when it is animated.

Do not replace visual review with a screenshot checksum. Use semantic tests for
the loader, manifest, lifecycle, and animation state machine. Use gameplay
review for art quality and readability.

## Add animation only with a stated representation

Read [animation.md](references/animation.md) before you design an animated
prop, character, or enemy. A static `.vox` model does not contain animation by
itself. Select frame models, rigid parts, or a skeleton from the actual motion
contract. Start with one real clip before you expand the format.

## Record provenance

Record the editable source, generation command, reference inputs, license, and
intentional external inspiration. Borrow a technique, not another game's
model, palette, character identity, source, or animation frames. Review the
license before you adapt open-source code or data.

State what is deterministic. For example:

- Creative design: human-authored or LLM-assisted.
- Regeneration: deterministic and offline.
- Runtime result: reviewed in the real renderer.

Do not describe LLM-assisted authorship as deterministic regeneration.
