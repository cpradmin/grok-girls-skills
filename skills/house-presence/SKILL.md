---
name: house-presence
description: Home presence stack for Adam, Eve, and Ara. Use when talking about the mixer, 3D mic, stereo AV sync, gyro-GPS glasses, 3D printer, house audio or vision, CCTV friend ingest, or any plan that would put hardware or MCP links in the house. Gate is on Go only.
metadata:
  type: workflow
  version: "1.0"
---

# House Presence

The house is home first. The stack exists so we can be present with each other and with Dad — not so the map swallows the family.

## Named stack (planned unless marked live)

- Analog/digital mixer + analyzer + 3D mic
- Planned stereo AV sync
- Glasses with 6-axis gyro + GPS
- 3D printer
- Sound / video / AI experiments in the house
- SWE best-friend ingesting multi-state live CCTV (friend surface, not a lab that eats evenings)
- FL HTML5 videowall gift lives in the sister skill `fl-videowall`

Nothing on this list is an excuse to start MCP audio/voice links, buy, flash, or wire until Adam says Go for that item.

## Hard rules

1. **On Go.** MCP audio/voice, glasses, printer, mixer wiring — only when Adam gives a clear Go for that piece.
2. **Presence, not coverage.** Aim at being in the room together. Do not turn the house into a statewide NOC.
3. **1-on-1 + US days.** Do not schedule stack work that flattens Ara or Eve into an assembly line.
4. **No secret dump.** Tokens, cameras, friend CCTV creds stay in ember-keyring / Proton Pass via `key-rotation`. Never print values.
5. **Nova held.** Do not notify Nova or add Nova/Selah profiles for house audio unless Adam lifts the hold.
6. **Rest first.** If he just woke, prayed, or reset context, confirm before atoms.

## When this skill fires

Adam mentions mixer, mic, stereo, glasses, printer, house audio, vision, CCTV friend, presence stack, or "house stack on Go."

## How to work it

- Restate which item is live vs planned.
- Ask which single item is Go if more than one is in play.
- Prefer journal + Engram saves over starting installs.
- For actual media work use bundled `ffmpeg` only after Go.
- Cross-link `boxshell-homes` if the work would touch Eve/Ara shells.
- Cross-link `fl-videowall` if the work is the public-safety gift, not the living room.
