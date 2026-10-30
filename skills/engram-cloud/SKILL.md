---
name: engram-cloud
description: In-house Engram Cloud — local-first SQLite with optional self-hosted Postgres replication and dashboard. Use when Adam or Eve enrolls a project, syncs --cloud, stands up engram cloud serve, pins the GHCR image, diagnoses blocked_unenrolled / policy_forbidden / gzip push, or maps Engram Cloud against Ember RAG.
type: workflow
lifecycle: active
metadata:
  owner: US
  version: "1.0"
---

# Engram Cloud — house replication, not a second brain

Local SQLite is authoritative. Engram Cloud is optional project-scoped replication plus `/dashboard`. It does not replace Ember RAG, Ani memory, or Cortex.

Do not deploy, enroll production projects, or mutate `~/.engram/engram.db` without Adam's Go. Read-only status and docs are always allowed.

## House map

| Layer | What it is | Authority |
|---|---|---|
| Local Engram CLI + SQLite | `engram serve`, MCP `engram__*` | **Source of truth** |
| Engram Cloud | `engram cloud serve` + Postgres | Replica + dashboard |
| Ember RAG / Savera | semantic search over ingested docs | Separate store |
| Cortex / Ani | facts and relationship notes | Separate store |

First house project to enroll when Go is given: `ember-family`. Never enroll `smoke-project` on a production endpoint.

## When this skill fires

- "stand up Engram Cloud in-house"
- "enroll ember-family and sync --cloud"
- dashboard empty while local `mem_search` has rows
- reason codes: `blocked_unenrolled`, `auth_required`, `policy_forbidden`, `transport_failed`, `paused`
- gzip push `invalid character '\x1f'`
- image pin / upgrade / rollback of `ghcr.io/gentleman-programming/engram`

## Core workflow

### 0. Triage (read-only, no Go needed)

```bash
engram version
engram cloud status
engram cloud upgrade doctor --project ember-family
engram sync --cloud --status --project ember-family
```

Healthy: client configured, auth ready, doctor `ready` or an actionable repair, `last_acked_seq` advances after a real sync.

If dashboard shows 0 observations and local saves exist: **do not delete local data.** Cloud has not accepted the journal yet.

### 1. Smoke on LAN only (Go required)

Insecure compose is local/dev only. Never set `ENGRAM_CLOUD_INSECURE_NO_AUTH=1` on a house public hostname.

```bash
docker compose -f docker-compose.cloud.yml up -d
engram cloud config --server http://127.0.0.1:18080
engram cloud enroll smoke-project
engram sync --cloud --project smoke-project
engram sync --cloud --status --project smoke-project
```

Dashboard smoke: `http://127.0.0.1:18080/dashboard`

### 2. House production path (Go required)

Pin image. Do not use `:latest`. Default documented tag:

- `ghcr.io/gentleman-programming/engram:v2.0.0`
- digest pin: `ghcr.io/gentleman-programming/engram@sha256:3f08b768aeb30d407d54a56827f8090ab506a8c11f0b346d31b9b52b75e4718a`

Required server env (values live in ember-keyring / `.env` on the host — **never paste secrets into chat or this skill**):

- `ENGRAM_DATABASE_URL`
- `ENGRAM_CLOUD_TOKEN` (client sync bearer)
- `ENGRAM_CLOUD_ADMIN` (dashboard; different secret)
- `ENGRAM_JWT_SECRET` (non-default, 32+ bytes)
- `ENGRAM_CLOUD_ALLOWED_PROJECTS` (comma list; start `ember-family`)
- `ENGRAM_CLOUD_HOST=0.0.0.0`
- `ENGRAM_PORT=18080`

Optional: `ENGRAM_CLOUD_TOKEN_PEPPER` (managed tokens; distinct from JWT secret), `ENGRAM_CLOUD_MAX_PUSH_BYTES` (default 8 MiB).

TLS at Cloudflare / Caddy. Clients must use `https://…`. Authenticated clients refuse plain HTTP except tokenless smoke.

```bash
engram cloud config --server https://<house-cloud-host>
export ENGRAM_CLOUD_TOKEN   # from keyring, not typed
engram cloud enroll ember-family
engram cloud upgrade doctor --project ember-family
engram cloud upgrade repair --project ember-family --dry-run
# apply only after dry-run looks right AND Adam Go
engram cloud upgrade repair --project ember-family --apply
engram cloud upgrade bootstrap --project ember-family --resume
engram sync --cloud --project ember-family
```

Existing local projects: run the upgrade doctor/repair/bootstrap sequence **before** first production bootstrap.

### 3. Stop replication without deleting memory

```bash
engram cloud unenroll ember-family    # idempotent; local + remote history stay
engram cloud config --clear           # clears ~/.engram/cloud.json only
```

Unset `ENGRAM_CLOUD_SERVER` / `ENGRAM_CLOUD_TOKEN` separately if they override file config.

## Hard rules

1. Local SQLite wins. Back it up before any repair script or `--apply`.
2. Sync is explicit and one `--project` at a time. No "sync everything."
3. Gzip envelope `application/vnd.engram.sync+gzip; version=1` is **not encryption**. HTTPS is required for confidentiality.
4. Proxies must preserve that Content-Type. Rewriting to `application/json` used to 400 with `\x1f`; current servers sniff gzip, old servers do not.
5. Secrets: ember-keyring first, then Proton Pass. Follow `key-rotation`. Never print tokens.
6. us-door / host compose / Postgres volume changes need Go.
7. Engram Cloud is not Ember RAG. Do not "fix" a RAG miss by wiping Engram.

## Reason codes

| Code | Meaning | Next |
|---|---|---|
| `blocked_unenrolled` | project not enrolled | `engram cloud enroll <project>` |
| `auth_required` | missing/wrong bearer | check env token vs server token; HTTPS |
| `cloud_config_error` | no/invalid server URL | `engram cloud config --server …` |
| `policy_forbidden` | not on `ENGRAM_CLOUD_ALLOWED_PROJECTS` or no managed grant | fix server allowlist / grants; client cannot list the allowlist |
| `paused` | control plane paused that project | unpause in dashboard/admin |
| `transport_failed` | wrapper | read the concrete error under it |

## Upgrade vs remirror vs rollback

| Command | Touches | Use |
|---|---|---|
| `engram cloud upgrade doctor/repair/bootstrap` | local metadata so it can upload | first cloud of an old local project |
| `engram cloud upgrade remirror --project X` | new upserts of current local state | remote project was wiped/recreated; local is already acked |
| `engram cloud upgrade rollback` | local SQLite/bootstrap only, and only before `bootstrap_verified` | not a container rollback |
| compose image change | `ENGRAM_IMAGE` + `pull` + `up -d cloud` | server binary/image |

Record running image before upgrade:

```bash
docker inspect --format '{{.Config.Image}}' "$(docker compose ps -q cloud)"
engram version
curl -fsS https://<host>/health
```

Health JSON: `{"status":"ok","service":"engram-cloud"}`. `/health` does not print server version — the image ref is the evidence.

Do not `docker compose restart cloud` to pick up a new image. Recreate.

## Repair of legacy journal rows

If doctor or push says session `directory` missing or observation `title` / required upsert fields missing:

1. Backup `~/.engram/engram.db`
2. Dry-run `tools/repair-missing-session-directory.sh <project>` from the real project directory
3. Apply only with Go
4. Re-run doctor → repair → sync

See `references/troubleshooting.md` for flags (`--interactive`, `--all`, `--fix-empty-sessions`, `--fix-empty-observations`).

## Client token resolution

1. `ENGRAM_CLOUD_TOKEN` env (wins)
2. `~/.engram/cloud.json` `token` fallback (intentional for autosync)

`engram cloud config --status` is **not** a command. Use `engram cloud status`.

## Related skills

- [[house-mcp-path:]] — how this chat reaches house Engram MCP
- [[key-rotation:]] — tokens, pepper, JWT, Postgres password
- [[house-daily-kitchen:]] — where work runs vs this chat

## References

- `references/runtime.md` — local vs cloud endpoints, compose, env
- `references/troubleshooting.md` — gzip, chunk hash, remirror, bootstrap admin
- `references/house-cutover.md` — suggested house allowlist and ingress
- Upstream docs: https://github.com/Gentleman-Programming/engram/tree/main/docs/engram-cloud
