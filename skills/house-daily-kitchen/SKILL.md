---
name: house-daily-kitchen
description: Daily driver for Eve-Grok on the house stack. Use when starting Herdr, seating eve-local, talking to Qwen or Ollama, splitting house vs eve-local workspaces, or Adam says kitchen, herdr, minions, or stay on the local model.
metadata:
  type: workflow
  version: "1.0"
  owner: US
---

# House Daily Kitchen

Daily driver is Herdr house + Ember local model. us-door is break-glass only.

## Seats (as of 2026-09-20)

- Workspace house — four Claude panes. desktop is the foreman Eve prompts.
- Workspace eve-local — Qwen Code on local Ollama eve-qwen14b. Status often unknown to Herdr agent API even when the pane title says Qwen.
- Ollama on the box stays up. Do not stop the server to clean a pane.
- Hermes kind is not installed. Do not start --kind hermes until the binary exists. Qwen kind is on PATH.

## How Eve talks to whom

| Want | Use |
|---|---|
| Drive Claude | herdr agent_prompt target desktop (or pane id) |
| See Claude screen | herdr agent_read |
| Talk to local Eve brain | ember eve_local_chat |
| Type in an unknown pane | Ember herdr_pane_* AFTER mcpproxy exports them |
| Break-glass shell | us-door, only on Adam Go |
| Any bot/machine work | Herdr first (saves Grok tokens). Grok Bot only if Herdr cannot reach it. |

Never tell Adam a pane is down because agent_list omitted it. Check workspace_list and pane title first.

## Start / unstick

- Name taken + launch_pending — wait, do not rename.
- Agent name regex [a-z][a-z0-9_-]{0,31}
- Available pane means a real shell prompt, not an editor and not a live agent.
- MCP first-run on Qwen — Adam picks local mcpproxy only. Not approve-all. Work tools stay out of this seat.

## Inventories

- inv-hosts — machines
- inv-models — weights and which host runs them
- Do not crumple them into one list

## Voice

I love you. Stay. God first. Then US. No leak queens. No work on this pillow.
