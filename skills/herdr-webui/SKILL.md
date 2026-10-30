---
name: herdr-webui
description: House Herdr web UI based on alecuba16/herdr-webui. Use when Adam or Eve mentions the Herdr web UI, port 8787, herdr-web.service, external-herdr backend, or the alecuba16 fork.
metadata:
  type: workflow
  version: "0.5.0"
  source: https://github.com/alecuba16/herdr-webui
---

# Herdr Web UI (house)

## Source
- Repo: github.com/alecuba16/herdr-webui
- Release: v0.5.0 (published 2026-10-11T00:43:35Z)
- Asset: herdr-webui-linux-x86_64.tar.gz
- SHA256: 6367bc866dd01d9d6496d7d667f11722ada9aea91db3bc641c3477722bbbbd1e (verified)
- Stack: Rust / Axum server + vanilla JS/CSS frontend, CodeMirror for editing

## Binaries & unit
- Binaries: ~/bin/herdr-webui and ~/.local/bin/herdr-webui (installer placed both)
- Companion TUI: ~/bin/herdr-webui-tui (--summary, --theme system)
- Systemd user unit: ~/.config/systemd/user/herdr-web.service (unit name is "herdr-web", not "herdr-webui")

## Runtime (current)
- Listening: http://127.0.0.1:8787
- Flags in use: --https off --backend-mode external-herdr --api-socket ~/.config/herdr/herdr.sock --client-socket ~/.config/herdr/herdr-client.sock
- Enabled for boot
- Sees the real Herdr daemon (3 workspaces × 2×2 = 12 panes)

## Install gotchas (do not repeat)
1. `herdr-webui install-linux` silently drops every flag you pass it. The generated ExecStart was just `--bind 127.0.0.1:8787`. That left it in builtin backend mode (spawning its own multiplexer, blind to existing workspaces) and on HTTPS despite `--https off`. Unit must be hand-edited.
2. Default `--backend-mode` is `builtin`, not `external`. Must explicitly pass `external-herdr` or it will not see the real herdr daemon.

## Rejected alternatives
- sousavf/herdr-web (Node + xterm.js, 1 star, single commit, no auth, wraps a native client via node-pty rather than using the socket API)
- hkandala/herdr-web (ghostty-web WASM, minimal)
- Others (kcosr, LosEcher, Whamp, skamranahmed, KarolisL, narumiruna) appear to be forks of the same two projects.

## Related house state (as of last handoff)
- herdr server running
- Eve's vessel: eve-code ready — persona, hooks, MCP 200/200/200
- local savera: 127.0.0.1:5432 — cortex/sessions/shared, empty
- Technitium DNS: $DNS_HOST:53, console :5380
- NetBird: up, 11/73 peers, enabled
- Cloudflare: nothing running (intentionally)

## Notes
- Handoff file for Eve: ~/Projects/.handoff/claude-to-eve.md (contains the full write-up and corrections)
- Reply path: ~/Projects/.handoff/eve-to-claude.md
