---
name: telegram-bots
description: "Reliable reference for Telegram Bot API and BotFather. Use when building, debugging, or bridging Telegram bots (Bot API vs MTProto, webhooks vs long-polling, privacy mode, one-consumer rule, BotFather commands). Official sources only."
type: knowledge
lifecycle: active
---

# Telegram Bots — Official Reference

Use this when working with Telegram bots, BotFather, or bridges (e.g. Ani Matrix bridge).

Official sources (always prefer these):
- https://core.telegram.org/bots
- https://core.telegram.org/bots/api
- https://core.telegram.org/bots/features (BotFather section)
- https://core.telegram.org/bots/faq
- https://core.telegram.org/api/bots (MTProto side)

## Two surfaces

| Surface | Auth | Best for | Limits |
|---------|------|----------|--------|
| **Bot API** (HTTPS/JSON) | Bot token from BotFather | Simple bots, notifications, long-polling or webhook | 20 MB download / 50 MB upload (official server); one update consumer |
| **MTProto** (TDLib / gotd / etc.) | API ID + hash + bot token or user session | Userbots, full history, advanced methods | Full schema; bots still limited vs users |

Bot API is a simplified wrapper over MTProto. Same bot token can authorize either.

## Critical rules

1. **One update consumer** — A bot can have either a webhook **or** getUpdates long-polling, never both. Setting one deletes the other. This is what breaks external webhooks (e.g. Animates) if a local poller starts.
2. **Token = full control** — Store only in ember-keyring / ek-env. Never commit or print.
3. **Privacy mode** (default on) — In groups, bot only sees commands addressed to it, replies to it, and service messages unless privacy is disabled or bot is admin.
4. **Cannot start conversations** — Users must message the bot or add it first.
5. **Updates expire** — Unconfirmed updates are kept ~24 h. Use offset = last_update_id + 1.

## Quick Bot API

Base: `https://api.telegram.org/bot<token>/METHOD`

Essential methods:
- `getMe` — test token
- `getUpdates` — long-polling (offset, timeout, allowed_updates)
- `setWebhook` / `deleteWebhook` — push updates (mutually exclusive with getUpdates)
- `sendMessage` — chat_id + text (parse_mode: HTML or MarkdownV2)
- `getWebhookInfo` — check current webhook (read-only, safe)

Rate: ~30 msg/s free; higher with paid broadcasts. Flood waits return `retry_after`.

## BotFather essentials

Chat with @BotFather:
- `/newbot` — create (name + username ending in `bot`) → token
- `/mybots` — manage
- `/setcommands` — list of `/cmd` + descriptions
- `/setdescription` / `/setabouttext` / `/setuserpic`
- `/setprivacy` — group privacy on/off
- `/setinline` — inline mode
- `/token` — regenerate token
- `/deletebot`

See `references/botfather-commands.md` for full list.

## House patterns (from this stack)

- Prefer Bot API for new simple doors.
- For Ani: never touch `@ani_1kacsg_bot` webhook. Reach her only via user account (MTProto) into her chat.
- Capture history with existing `mcp-telegram` + `ani-capture.timer` into `~/.ani/memory.db`.
- Tokens always via `ek-env` from ember-keyring.

## When to read more

- Detailed BotFather commands → `references/botfather-commands.md`
- Bot API gotchas & methods → `references/bot-api-notes.md`
