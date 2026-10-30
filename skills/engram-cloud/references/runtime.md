---
description: Engram Cloud runtime split, endpoints, compose, and required env. Read before deploy or client config.
connections: [troubleshooting, house-cutover]
---

# Runtime

## Two processes

| Process | Job | Endpoints |
|---|---|---|
| `engram serve` | local memory API | `GET /sync/status` |
| `engram cloud serve` | replica + dashboard | `GET /health`, `GET /sync/pull`, `POST /sync/push`, `GET /dashboard/*` |

Push media type: `application/vnd.engram.sync+gzip; version=1`. Pull uses gzip only if client `Accept`s it and decoded chunk ≤ 8 MiB; else legacy JSON. Server still accepts legacy JSON pushes.

## GHCR

- Tag: `ghcr.io/gentleman-programming/engram:v2.0.0`
- Platforms: linux/amd64, linux/arm64
- Do not build-from-source for house prod

## Compose shape (production-ish)

Services: `postgres:16-alpine` + `cloud` image. Volume `engram-cloud-pg`. Cloud waits on Postgres health. Publish `18080:18080` only on loopback or internal net; public via TLS proxy.

Postgres must not be on public ingress.

## Auth modes

| Mode | Flags | Where |
|---|---|---|
| Smoke | `ENGRAM_CLOUD_INSECURE_NO_AUTH=1` + allowlist `smoke-project` | 127.0.0.1 only |
| Legacy env tokens | `ENGRAM_CLOUD_TOKEN` + `ENGRAM_CLOUD_ADMIN` + JWT secret | house default |
| Managed principals | set `ENGRAM_CLOUD_TOKEN_PEPPER`; `engram cloud bootstrap admin` | optional later |

Cannot combine insecure-no-auth with `ENGRAM_CLOUD_TOKEN`.

First managed admin is once. Duplicate bootstrap is refused and audited. Lost unused token: `engram cloud bootstrap recover-token` only in documented safe states.

## CLI that matters

```
engram cloud config --server <url>
engram cloud status [--project X]
engram cloud enroll X
engram cloud unenroll X
engram sync --cloud --project X
engram sync --cloud --status --project X
engram cloud upgrade doctor|repair|bootstrap|status|remirror --project X
engram cloud attest-prompt-source --sync-id <id> --owner-project X
```

Attest is human-token, confirm-yes, no import/pull/delete.
