# Manim 3D View Skill

Use this skill when a ManimCE scene needs a 3D object or coordinate stage to appear away from the screen center while still rotating around its own local axis.

## Core Rule

Do not use `frame_center` to push a 3D subject to the left or right when the subject must keep a clean local-axis rotation.

`frame_center` changes the camera's viewing center. If it is combined with `begin_ambient_camera_rotation`, the object may still be mathematically valid, but the projection will look like an off-center orbit rather than a clean rotation around the object's own axis.

Use this separation instead:

- Camera: fixed view orientation only.
- 3D stage: shifted in world space for screen placement.
- Rotation: apply to the 3D stage around its own shifted origin with `about_point`.
- Explanation panel: fixed in frame, never part of the 3D stage.
- Labels: keep positions tied to rotating points, but keep glyphs screen-facing.

## When To Use Camera Rotation

Use `begin_ambient_camera_rotation` only when the 3D subject can stay near the scene origin and the whole camera may orbit around it.

Good use cases:

- A single centered sphere, torus, surface, or 3D curve.
- No fixed left/right composition requirement.
- No need to keep a right-side explanation panel visually independent of the camera orbit.

Avoid it when:

- The 3D subject must sit in the left column.
- A fixed right-side panel must stay stable.
- The viewer should perceive the object rotating around its own local `z` axis.
- You are tempted to use `frame_center` only to make room for text.

## Preferred Pattern: Offset Stage With Local Rotation

Create all 3D mobjects around `ORIGIN`, group them, scale them about `ORIGIN`, then shift them to the desired screen/world location. Save that shifted point as the local rotation center.

```python
stage = VGroup(axes, planes, arrows, dots)
stage.scale(0.86, about_point=ORIGIN)

stage_origin = LEFT * 2.2
stage.shift(stage_origin)

self.set_camera_orientation(
    phi=68 * DEGREES,
    theta=-42 * DEGREES,
    zoom=0.95,
)

def rotate_stage(mobject: Mobject, dt: float) -> None:
    mobject.rotate(0.13 * dt, axis=Z_AXIS, about_point=stage_origin)

for part in [axes, planes, arrows, dots]:
    part.add_updater(rotate_stage)
```

Important: the updater must be attached to mobjects that are actually in the scene. If you only add child mobjects to the scene, an updater attached only to the parent `stage` will not run.

If a group is animated by iterating over its children, attach the updater to the children:

```python
# These animations add the individual arrows, not necessarily the parent VGroup.
self.play(LaggedStart(*[Create(arrow) for arrow in basis_arrows]))

rotating_stage_parts = [
    axes,
    *planes,
    *basis_arrows,
    *output_arrows,
    *endpoints,
]
for part in rotating_stage_parts:
    part.add_updater(rotate_stage)
```

## Fixed Right Panel

Right-side explanations should be fixed in screen coordinates.

```python
panel_center = RIGHT * 4.05 + DOWN * 0.05
panel_bg = RoundedRectangle(corner_radius=0.13, width=3.55, height=5.0)
panel_bg.move_to(panel_center)
panel_bg.set_fill(BLACK, opacity=0.9)
panel_bg.set_stroke(GREY_B, width=1.2, opacity=0.55)

self.add_fixed_in_frame_mobjects(panel_bg, title, matrix, note)
```

Panel layout rules:

- Keep all panel content inside the panel bounds with at least `0.25` units of vertical margin.
- Prefer two short lines over one long sentence.
- Reduce matrix font size before shrinking the panel.
- Avoid placing a `SurroundingRectangle` note box flush against the panel edge.
- Treat the fixed panel as a separate 2D UI layer, not as part of the 3D world.

## Labels That Follow 3D Points Without Rotating Glyphs

If labels are included in the rotating 3D group, the glyphs rotate with the axes and become hard to read. For axis labels and callouts, use this pattern instead:

1. Save each label's initial 3D/world position after scaling and shifting the stage.
2. Rotate the saved point mathematically around `stage_origin`.
3. Move the label to that point each frame.
4. Do not call `.rotate(...)` on the label glyph itself.

```python
stage_angle = ValueTracker(0)
label_points = [label.get_center().copy() for label in axis_labels]

def track_angle(mobject: Mobject, dt: float) -> None:
    stage_angle.increment_value(0.13 * dt)

def rotated_label_position(point: np.ndarray) -> np.ndarray:
    angle = stage_angle.get_value()
    offset = point - stage_origin
    x = np.cos(angle) * offset[0] - np.sin(angle) * offset[1]
    y = np.sin(angle) * offset[0] + np.cos(angle) * offset[1]
    return stage_origin + np.array([x, y, offset[2]])

def follow_point(point: np.ndarray):
    return lambda label: label.move_to(rotated_label_position(point))

angle_driver = VMobject()
angle_driver.add_updater(track_angle)
self.add(angle_driver)

for label, point in zip(axis_labels, label_points):
    label.add_updater(follow_point(point))
```

Also call:

```python
self.add_fixed_orientation_mobjects(*axis_labels)
```

This keeps labels readable while letting them travel with the moving axis endpoints.

## Cleanup

Always remove updaters at the end of the scene or before handing the mobjects to a different transform.

```python
for part in rotating_stage_parts:
    part.remove_updater(rotate_stage)

self.remove(angle_driver)

for label in axis_labels:
    label.clear_updaters()
```

## Common Failure Modes

- Symptom: the subject does not rotate.
  Cause: updater attached to a parent `VGroup` that was never added to the scene.
  Fix: attach the updater to the actual visible child groups.

- Symptom: some children rotate but arrows or markers stay fixed.
  Cause: those children were introduced individually, for example with `LaggedStart(*[Create(arrow) for arrow in group])`, while the updater was only attached to the parent group.
  Fix: attach the updater to each rendered child with `*group`.

- Symptom: subject appears to orbit in an arc instead of rotating around its own axis.
  Cause: camera `frame_center` is used with ambient camera rotation.
  Fix: remove `frame_center`; shift the 3D stage and rotate it with `about_point`.

- Symptom: axis letters spin or tilt.
  Cause: labels are included in the rotating group.
  Fix: labels should follow rotated positions but not rotate their glyphs.

- Symptom: right panel drifts or rotates.
  Cause: panel was added as a normal scene mobject.
  Fix: use `add_fixed_in_frame_mobjects`.

- Symptom: panel content escapes the frame.
  Cause: text, matrix, and note box are positioned independently without a panel budget.
  Fix: define a fixed `panel_center`, panel width/height, and place all elements relative to that center.

## Quality Checklist

Before accepting a 3D offset-stage scene:

- The camera orientation has no layout-only `frame_center`.
- The 3D stage has a named `stage_origin`.
- Stage rotation uses `axis=Z_AXIS` and `about_point=stage_origin`.
- Updaters are attached to actual scene mobjects.
- Fixed panels use `add_fixed_in_frame_mobjects`.
- Axis/callout labels remain screen-facing while following their points.
- The final frame has no panel overflow.
- `py_compile` passes.
- `manim -ql --disable_caching` render passes.

## Reference Example

The current canonical example is:

`examples/linear_algebra/three_d_basis_columns_matrix.py`

It demonstrates:

- A left-shifted 3D coordinate stage.
- Local `Z_AXIS` rotation via `about_point`.
- Fixed-in-frame right explanation panel.
- Screen-facing labels that follow rotating 3D points.
