---
name: cloudcli-agent
description: Send work to local CloudCLI shop via POST /api/agent. Use when Adam says CloudCLI, shop door, send Claude to a repo, or Eve should not burn the Grok week on a coding job. Never print the API key.
---

# CloudCLI agent (shop, not home)

Home is US / this chat / Eve-local. This is the shop.

## Endpoint
POST http://127.0.0.1:3002/api/agent
Header X-API-Key from ember-keyring only: `ember/svc:cloudcli:api-key` via `ek-env`.
Docs still say :3001. Live port is 3002.

## Legal default body
- provider: claude
- model: pin 4.8 when the UI exposes it
- projectPath: ~/Eve unless Adam names another existing path
- stream: false unless he wants a ticker
- message: exact task, nothing extra

## Forbidden unless Adam Go
- createPR, createBranch, cleanup on clones
- githubToken in the JSON (use stored CloudCLI settings)
- printing the key, putting the key in HTML, logging the header

## How
ek-env CLOUDCLI_KEY=ember/svc:cloudcli:api-key -- curl ...

Report sessionId and success. Do not dump full transcripts if they contain secrets.
