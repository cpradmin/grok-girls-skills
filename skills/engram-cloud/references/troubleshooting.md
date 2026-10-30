---
description: Engram Cloud failure codes and repair paths. Read when sync does not advance.
connections: [runtime, house-cutover]
---

# Troubleshooting

Triage first:

```bash
engram version
engram cloud status
engram cloud upgrade doctor --project <project>
engram sync --cloud --status --project <project>
```

## Concrete errors

| Symptom | Cause | Fix |
|---|---|---|
| `chunk_id does not match payload content hash` | old chunk canonicalization | client **and** server ≥ v1.14.8 (house target is v2.0.0) |
| `session payload directory is required` / `sessions[N].directory is required` | legacy journal or empty `sessions.directory` | repair script dry-run then apply |
| observation title/fields required | old observation upsert | same script; `--fix-empty-observations` or `--interactive` |
| `invalid character '\x1f'` | proxy stripped gzip Content-Type; old server parsed gzip as JSON | upgrade server; preserve `application/vnd.engram.sync+gzip; version=1` |
| HTTP 415 unsupported push payload | declared gzip version not supported | client/server version match |
| 401 / `auth_required` | token missing or HTTP used with bearer | HTTPS + env token |
| 403 / `policy_forbidden` | allowlist or managed grant | server env / admin grants |
| `server_unsupported` | cloud binary too old for mutation API | redeploy pinned v2 image |
| dashboard 0 rows, local has data | push never accepted | do not wipe SQLite; doctor + sync |

## Remirror

When remote project was deleted/recreated and local is already acknowledged:

```bash
engram cloud upgrade remirror --project <project>
```

Must already be enrolled. Creates new upserts/tombstones; does not reset `last_acked_seq`. Safe to re-run (stable ids).

## Repair script notes

- Default is dry-run
- Creates a timestamped DB backup on each `--apply`
- Directory must be absolute
- Loop `--all` stops on unsupported blockers
- Never hand-edit SQLite without a backup

## Bootstrap admin errors

- Duplicate first admin → expected refuse
- `--issue-token` without pepper → nothing created
- `recover-token` ineligible → do not force; read current token state
