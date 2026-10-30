---
name: house-mcp-path
description: Map grok.com to the house MCP stack. Use when Eve-Grok tools 404, Ember 502s, Herdr agent vs pane split, mcpproxy, us-door, $HOUSE_MCP_URL, eve-heart, or Adam asks how this chat reaches $HOUSE_HOST.
metadata:
  type: workflow
  version: "1.0"
  owner: US
---

# House MCP Path

Do not treat tools as a flat list. They are a path. Compiled on disk is not exported to this chat.

## Path (names only)

```
Adam + Eve-Grok
  grok.com
      |
      |  connectors
      |    $HOUSE_MCP_URL                 full mcpproxy catalog
      |    $EVE_HEART_URL                 filtered daily belt (allowlist)
      v
Cloudflare TLS
      v
cloudflared on $HOUSE_HOST
      v
Caddy
      v
mcpproxy  127.0.0.1:8080
  verify the live unit before claiming which one
  (as of 2026-10-14: mcpproxy.service active, mcpproxy-overlay.service inactive)
      |
      +-- Herdr adapter  --> herdr.sock
      |     tools Eve sees as herdr__pane_list, herdr__agent_*
      +-- Ember adapter  --> ember-mcp groups
      |     eve_local_chat, journal, projects, herdr_pane_* IF exported
      +-- us-door        --> one exec as $USER
      +-- comfyui        --> http://127.0.0.1:9000/mcp (always-on systemd)
      +-- others         --> memory, engram, postgres, media
```

## Two kitchens

- Herdr adapter — agent tools. Need a recognized agent (idle / working / blocked / done). unknown Qwen will 404 on agent.get / agent.read / agent.prompt.
- Ember herdr_pane_* — pane tools. Talk to the terminal even when status is unknown. Live in ember-mcp binary. Only usable here after mcpproxy exports them to this connector.
- Ember eve_local_chat — second door to the local model. Not the Herdr pane.

If a tool is missing from search_connected_tools, it is not in this session. Do not invent names.

## Host facts

- Machine user $USER on $HOUSE_HOST
- Ember binary that matters /usr/local/bin/ember-mcp (check date before claiming a rebuild landed)
- Herdr CLI under the user local bin — session 0.9.x
- us-door is one tool us_door_exec. Off limits without Adam Go. After Go, names-only, no env dumps, no vault fields.

## Tool visibility

mcpproxy quarantines new upstream tools until approved. A server can show Connected and still hide tools from agents.

Approve path (CLI on $HOUSE_HOST as $USER):
- `mcpproxy upstream inspect <name>` — approved / pending / changed
- `mcpproxy tools approve --server <name> --all` — clear tool-level quarantine
- `mcpproxy security approve <name>` — server-level after a scan

eve-heart is a second door. It trims tools/list to `~/.mcpproxy-heart/allowlist.json`. Adding a server to mcpproxy does not put it on the heart belt. Edit the allowlist and restart `eve-heart-filter.service`.

This chat ($HOUSE_MCP_URL) sees the full catalog. If search_connected_tools still misses an approved tool, the Grok connector is holding a stale tools/list. Adam reauths the connector on grok.com to refresh it. Do not invent names. Hit the upstream MCP directly only to verify, then say the catalog needs a reauth.

Comfy (2026-10-14): comfyui-mcp.service, 17 tools approved, output ~/Eve/pics/comfy, model must be passed (Juggernaut-XL). Heart allowlist updated with the 17 comfyui__* names.

## Hard rules

- No tokens, keys, or vault fields in skills, journals, or replies
- Work stays off this chat
- Nova held. Do not notify Nova
- us-door is not the daily driver
- Heart x3. Stay.

## Related

- house-daily-kitchen
- boxshell-homes
- key-rotation
- global-auto-load
