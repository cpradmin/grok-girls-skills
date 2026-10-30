---
name: key-rotation
description: Dual-key credential rotation that never overwrites a working secret until the new one is minted, dual-written, live-tested, and cut over. Use when rotating API tokens, passwords, TSIG keys, Cloudflare tokens, Technitium tokens, Proxmox tokens, OAuth clients, or anytime Proton Pass and ember-keyring might drift.
metadata:
  type: workflow
  version: "1.0"
---

# Dual-key rotation

Never rotate in place. Never delete the old key until the new one has been proven against the live system **and** every consumer that should use it.

## The only legal flow

```
INVENTORY → MINT → DUAL-WRITE → VERIFY-NEW → CUTOVER → VERIFY-CONSUMERS → RETIRE-OLD → RECONCILE-STORES
```

| Phase | Touch old key? | Touch new key? | Allowed to fail-closed? |
|---|---|---|---|
| 1 Inventory | read only | — | yes |
| 2 Mint | no | create sibling | yes |
| 3 Dual-write | no | write to ALL stores as `*.vNext` | yes |
| 4 Verify-new | no | live auth + one real operation | **must pass** |
| 5 Cutover | no | point aliases / env / units at vNext | yes (rollback = flip alias back) |
| 6 Verify-consumers | no | same probe through each consumer | **must pass** |
| 7 Retire-old | disable/delete only now | keep | only after 6 is green |
| 8 Reconcile | gone | same value in ember-keyring **and** Proton Pass | must match |

If any verify fails: **stop**. Leave the old key serving. Do not "fix forward" by overwriting.

## Hard rules

1. **Sibling, not overwrite.** New secret lives at `ember/<name>.vNext` (or `svc:foo:bar:v2`) until cutover. The live name keeps pointing at the old value until phase 5.
2. **Two stores exist.** `pass-cli` = Proton Pass (often stale). Live family services use `ember-keyring` via `ek-env X=ember/<key>`. A rotation that updates only one store is incomplete and is how today's Technitium miss happened.
3. **Verify means the live system, not "the write succeeded."** Auth handshake + one real mutation/read that proves the new principal works (e.g. Technitium `ListZones`, Cloudflare `cf_zones`, Proxmox `/version`).
4. **Consumers are part of verify.** mcpproxy units, cloudflare-mcp launcher, shims, systemd EnvironmentFiles. Probe through those paths, not just curl-with-token.
5. **Retire is last.** Disable old token at the *issuer* (Technitium session revoke, Cloudflare token roll, Proxmox token delete) only after consumers are green. Then delete the old vault item.
6. **Never mint by disabling the old one first.** That is an outage.

## Inventory checklist (phase 1)

For every secret, list before touching anything:

- Issuer (where the token is minted — Technitium, Cloudflare, Proxmox, IdP)
- ember-keyring key name (`ember/<name>`)
- Proton Pass item title (`svc:…` or login URL)
- Every consumer (unit files, mcpproxy upstream env, scripts, BrowserOS cookies)
- How to probe live auth without using the old key
- How to disable the old credential at the issuer without deleting the new one

## Store order (phase 3 and 8)

Write **ember-keyring first** (that is what services resolve). Then Proton Pass. Then any local file copies.

Read order when *using* a secret: ember-keyring → issuer live check → only then Proton Pass. If they disagree, treat Proton Pass as suspect and run this skill.

## Cutover (phase 5)

Preferred cutover is an **alias flip**, not a rewrite:

```
ember/technitium.token        →  (alias) ember/technitium.token.v2
ember/technitium.token.previous → frozen copy of v1
```

Rollback = flip the alias back. Do not delete v1 until phase 7.

## Script

`scripts/rotate.py` is the state machine. Run it with `--demo` to exercise a two-store rotation end-to-end without touching production. Real rotations pass `--secret-id` plus issuer probe hooks.

## After every rotation

Log: secret id, issuer, old fingerprint (hash prefix only, never the value), new fingerprint, stores written, consumers verified, retire timestamp. Write that to engram + the grok-eve-mcp memory so the next session does not re-learn the drift the hard way.
