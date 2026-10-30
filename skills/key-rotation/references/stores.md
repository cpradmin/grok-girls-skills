# Credential stores — read/write order

## Two stores, one truth

| Store | How agents read it | What it actually is | Trust |
|---|---|---|---|
| ember-keyring | `ek-env X=ember/<name>` | age-encrypted family vault the services use | **source of truth** |
| Proton Pass / pass-cli | `pass-cli item get …` | human password manager, Syncthing replica on the box | suspect if they disagree |

Today's miss: Technitium was rotated in ember-keyring (Aug 2, Aug 19). Proton Pass still held the old admin password. Agents that "checked the vault" via pass-cli kept authenticating with a dead secret.

## Read order

1. ember-keyring
2. live issuer probe with that value
3. Proton Pass only as a human-facing copy

If 1 and 3 disagree, run `key-rotation`. Do not "fix" by writing the Proton value over ember.

## Write order (dual-write and reconcile)

1. ember-keyring sibling key (`<name>.v2`)
2. Proton Pass sibling item
3. Flip live alias in ember-keyring
4. Flip live alias in Proton Pass
5. Confirm fingerprints match

## Known family secrets that must stay dual-written

- Technitium API token (`ember/technitium` / `svc:$KEY_STORE_HOST:technitium`)
- Cloudflare DNS token (`svc:eve:cloudflare:api-token`)
- Cloudflare Access:Edit token (`svc:eve:cloudflare:access-edit`)
- Proxmox tokens (`root@pam!mcp`, `root@pam!eve`)
