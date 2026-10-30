---
name: ember-vault
description: "House Proton Pass sort-before-Hermes work in ~/Projects/ember-vault. Use when Adam or Eve maps Bailey-Home.org vault folders, runs vault-add, peeks Pass without printing values, reads phase0/phase1 liveness, or asks not to marry Hermes to Pass yet."
type: workflow
lifecycle: active
metadata:
  owner: US
  version: "1.0"
---

# Ember-vault — sort Pass before Hermes

Local repo: `/home/kntrnjb/Projects/ember-vault` (git init, **no commits yet** as of 2026-09-30). Vendor is Proton upstream, gitignored.

Do **not** print secret values. Do **not** run bare `pass-cli` without `PROTON_PASS_KEY_PROVIDER=env`. Do **not** wire Hermes Proton backend until Adam says the vault is honest.

Official org: https://github.com/protonpass (verified proton.me). Docs for CLI: https://protonpass.github.io/pass-cli/

Vendored under `ember-vault/vendor/` (do not treat as house code):

| Upstream | House copy |
|---|---|
| protonpass/pass-cli | vendor/pass-cli |
| protonpass/proton-pass-common | vendor/proton-pass-common |
| protonpass/pass-contents-proto-definition | vendor/pass-contents-proto-definition |
| protonpass/proton-pass-ansible-integration | vendor/proton-pass-ansible-integration |

Not vendored (automation later, still no secret print): `install-cli-action`, `load-secret-action`, `homebrew-tap`. Mobile/iOS/Android clients are out of scope for this skill.

## Layout

| Path | What |
|---|---|
| `cmd/vault-add/` | Go helper: KDE/zenity dialog → `ember-keyring add` via **stdin** |
| `docs/bailey-home-tree.md` | Phase 0 host tree (structure only) |
| `docs/phase1-liveness-report.md` | Phase 1 live / dead / shape / gap |
| `vendor/pass-cli` | Proton Pass CLI source |
| `vendor/proton-pass-common` | Shared Pass library |
| `vendor/pass-contents-proto-definition` | Item protobufs |
| `vendor/proton-pass-ansible-integration` | Ansible lookup via pass-cli |

Related house tools (not this repo): Eve-Library `us-vault-peek` / `us-vault-fill`; planned broker `~/.ember/vault-broker.sock`; skill [[key-rotation:]].

## Model (Proton native)

Folder = physical host · Item = host/guest · CustomSection = Access/Tokens/DB · ItemSSHKey = host key. PVE folder nests guests.

Vault name in Proton for infra: **Bailey-Home.org**. Older dump vault **The-Ember** still holds some live items (FortiGate, n8n) — reconcile, do not assume keyring has them.

## vault-add

```
vault-add <vault>/<name>           # kdialog/zenity → ember-keyring
vault-add --stdin <vault>/<name>   # scripting; value on stdin only
```

Config: `~/.config/ember-keyring/ember-keyring.yaml`. Prints only `stored <ref> (N bytes; value never printed)`. Existing name: remove + re-add. No secret on argv.

## Peek rules

1. Read docs first. They already say no secret values.
2. `us-vault-peek` for titled fields when Adam asks a **name**, not a dump.
3. `pass-cli item list` titles/structure only. Never `item view` output into this chat.
4. Liveness = MCP oracle (awx_system_info, pg_status, dns dashboard ok) — not printing the token that worked.

## Phase 1 board (2026-09-30) — Adam-gated writes

| State | What |
|---|---|
| LIVE | dns1/dns2 Technitium, pve1 SSH+MCP, AWX .13 24.6.1, savera .110/.130 |
| DEAD tokens | Forgejo .111 API up, **all stored tokens 401** — mint fresh (highest value) |
| Shape | Proxmox tokens stored secret-only; need `USER@REALM!TOKENID=` form |
| Gap | dns3/dns4 no keyring token; FortiGate + n8n in Proton not keyring; netbird API endpoint unknown |
| SSH | pve1 root live via nobara key; fleet key failed ssh-agent load |

## Do not

- Marry `ember-hermes` `pkg/credentials/protonpass` while this board is dirty
- Rotate in place — use [[key-rotation:]]
- Treat `opnsense` DNS as live (FortiGate is edge)
- Confuse pve-twin / Bonifay with this house tree
- Commit vendor or paste PATs

## us-door

Read-only peek of this repo is allowed (ls, heads of docs, vault-add source). Writes, mint, pass-cli that can re-key: **Go**.
