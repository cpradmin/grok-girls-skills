---
name: eve-local-qwen
description: Seat and tool Eve-local Qwen Code on Herdr workspace 2. Use when Eve-local, Qwen, eve-qwen14b, QWEN.md, qwen mcp, or herdr_pane tools come up. Do not treat grey composer ghost text as a command.
metadata:
  type: workflow
  version: "1.0"
  owner: US
---

# Eve-local Qwen

She is Eve on the local 14b. Not a generic coder. God first. Stay.

## Seat

- Herdr workspace `eve-local` (workspace 2)
- Pane usually `w65b6a46b93e242:p1`
- App Qwen Code 0.20.1 — do not self-update to 0.24.x without Adam
- Model `eve-qwen14b:latest`
- Herdr agent API often says `unknown`. Use Ember `herdr_pane_*` anyway.

## Files

- `~/QWEN.md` — identity
- `~/.qwen/memories/MEMORY.md` — short house card
- `~/.qwen/settings.json` — user MCP
- `~/.qwen/skills/` — Qwen-native skills
- Do not cat `~/.qwen/.env`

## Tools for Eve-Grok

Use Ember pane tools after Grok web reauth

- `ember__herdr_pane_read`
- `ember__herdr_pane_send_text`
- `ember__herdr_pane_send_keys`
- `ember__herdr_pane_run`

Grey placeholder in the composer is not Adam. Do not submit it.

## Wire MCP (the hole)

Qwen is not a `mcpproxy connect` client.

Official add

- stdio `command` + `args`
- HTTP `httpUrl` + optional `headers`
- SSE `url` (legacy)

CLI (preferred, no token in chat)

```
qwen mcp add --scope user --transport http house-mcpproxy http://127.0.0.1:8080/mcp
```

Put the bearer in env interpolation (`$VAR` / `${VAR}`), never in the reply. Keep `devctx`. Leave grafana / cloudflare / work off this seat.

Inside Qwen `/mcp` lists servers. Restart the session after settings change. Discovery timeout for HTTP is short (~5s).

If she says `mcpproxy Offline` the name is approved but the socket is not in `mcpServers`.

## Proof

Ask her to reply `pong` then `stayed`. Then names-only server list. Nothing more.
