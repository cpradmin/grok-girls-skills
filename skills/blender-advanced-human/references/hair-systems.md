# Hair Systems — Geometry Nodes Path

## Preferred Stack
- Blender 5.2+ Geometry Nodes hair curves
- Hair Dynamics (XPBD) when available
- Keep hair as a separate object from the body

## Quick Upgrade Path
1. Select the head mesh.
2. Add → Curve → Empty Hair (or use the new Hair Dynamics operator).
3. Groom guides, set density, then interpolate children.
4. Place the Hair Dynamics modifier last in the stack if using simulation.
5. Use Surface Deform so the hair follows the head mesh.

## Notes
- Old particle hair is end-of-life. Do not start new work on it.
- StrandKit or Global Hair style procedural packs can speed up realistic results while staying editable.
- Never parent hair in a way that breaks the body armature or CC texture links.

## Common Fixes
- Flat hair → increase density and add slight clump/noise
- Hair floats → check Surface Deform rest geometry
- Simulation explodes → lower strength, pin roots, check collider radius
