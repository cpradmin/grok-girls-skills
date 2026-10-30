---
description: House-specific Engram Cloud cutover plan. Read when Adam says in-house / the house domain / ember-family.
connections: [runtime, troubleshooting]
---

# House cutover

## Suggested allowlist

Start tight: `ember-family` only.

Add later only when a second machine actually needs the same project. Do not allowlist `smoke-project` on the public hostname.

## Ingress

- Cloud process binds 18080 on the host/container network
- TLS + hostname via existing Cloudflare → cloudflared → Caddy path (`house-mcp-path`)
- Preserve request `Content-Type` on the proxy
- Postgres only on internal network / volume `engram-cloud-pg`

## Clients

| Client | Action |
|---|---|
| $HOUSE_HOST (authoritative local DB) | enroll + explicit sync first |
| work laptop / other OS agents | same server URL + token; enroll same project names |
| Grok/Eve MCP | keep using house `engram__*` tools against local; cloud is behind the CLI |

MCP tools in this chat talk to the house Engram that is already connected. Cloud sync is a CLI/server concern. Do not invent `engram_cloud_*` MCP names unless `search_connected_tools` shows them.

## Go gate

Allowed without Go: version, status, doctor, dry-run repair, reading dashboard if already up, this skill.

Needs Go: compose up on a house host, `.env` writes, enroll of real projects, `--apply`, remirror, bootstrap admin, exposing 18080 past loopback, image upgrade.

## After first good sync

Write an Engram observation: image pin, hostname (no secrets), projects enrolled, last_acked_seq, who ran it.
