# VRM Export Checklist — CC4 / Rigify

## Before Export
1. Pose character into a clean T-pose (arms straight out, palms down).
2. Apply any pending transforms (Ctrl+A → All Transforms) on mesh and armature.
3. Confirm weights are good around shoulders, elbows, hips, knees.

## Bone Mapping
Open the VRM panel → Humanoid.

Manually verify and assign these required bones if auto-assign leaves them red:
- hips
- spine
- chest
- neck
- head
- leftUpperArm / rightUpperArm
- leftLowerArm / rightLowerArm
- leftHand / rightHand
- leftUpperLeg / rightUpperLeg
- leftLowerLeg / rightLowerLeg
- leftFoot / rightFoot

CC4 and Rigify names rarely match VRM names exactly. Do not trust auto-assign.

## Export Settings
- File → Export → VRM
- Export Only Selections: on
- Prefer VRM 1.0 when the target supports it
- Limit bone influences to 4 for broad compatibility
- Do not export cameras, lights, or extra helper objects

## After Export
Test in the target (VRChat, VRM viewer, etc.). If limbs collapse, re-check the red bone slots and re-export.
