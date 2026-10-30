---
name: blender-advanced-human
description: "Advanced Blender workflow for realistic human characters from Character Creator 4 bases. Use when refining CC4 models, fixing VRM bone hierarchy export, upgrading to Geometry Nodes hair, or setting up high-quality Cycles lighting and skin on house machines."
type: workflow
lifecycle: active
---

# Advanced Blender Human Pipeline — CC4 Base to Clean Export

Use for realistic human avatars (Eve, Ani, family models) built from Character Creator 4. Prefer Blender MCP for live scene work. Use Herdr for installs, background runs, and file work. Never break CC texture links or skin shaders.

## Core Workflow

1. **Start from CC4 + CC/iC Tools**
   - Confirm CC/iC Blender Tools is enabled.
   - Keep original CC skin shaders and texture links untouched.
   - Use gentle shape keys or Proportion Editor for body changes.
   - Stop immediately if shaders go white or textures break.

2. **VRM Export (highest priority fix)**
   - Pose character into clean T-pose.
   - Open VRM Humanoid panel and manually verify bone mapping (hips, spine, chest, neck, head, upper/lower arms, hands, upper/lower legs, feet).
   - Auto-assign often fails on CC4/Rigify names — assign manually.
   - Apply armature modifier only after weights are confirmed good.
   - Export only selected objects. Prefer VRM 1.0 when target supports it. Limit bone influences to 4 for compatibility.
   - See references/vrm-export.md for exact steps.

3. **Hair Upgrade**
   - Prefer Geometry Nodes hair curves over old particle system.
   - Use Blender 5.2+ Hair Dynamics (XPBD) when available.
   - For faster realistic results, consider StrandKit or Global Hair style procedural setups.
   - Keep hair as a separate object so it can be swapped without touching the body.

4. **Lighting & Skin**
   - Soft area lights + HDRI.
   - Leave CC subsurface scattering alone.
   - Gentle MixRGB only after the diffuse if color adjustment is needed.

5. **Machine Rules**
   - Herdr is default for any install, background Blender, or file work.
   - Blender MCP only when Blender is open and the BlendMCP addon is connected.
   - Do not use Grok Bot unless Adam explicitly clears it.

## Common Issues

| Problem | Fix |
|---------|-----|
| VRM red bone slots | Manual assignment in VRM Humanoid panel |
| Shaders go white | Revert last texture or MixRGB change immediately |
| Hair looks flat | Switch to Geometry Nodes hair + density control |
| Blender MCP offline | Launch Blender, enable BlendMCP, click Connect |

## References
- `references/vrm-export.md` — exact VRM bone mapping and export checklist
- `references/hair-systems.md` — Geometry Nodes and Hair Dynamics notes
