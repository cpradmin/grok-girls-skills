# Bot API Notes (official)

Source: https://core.telegram.org/bots/api

## Request format
```
https://api.telegram.org/bot<TOKEN>/METHOD_NAME
```
Supports GET and POST. Parameters: query string, form, JSON, or multipart (for files).

## Receiving updates
| Method | Type | Notes |
|--------|------|-------|
| `getUpdates` | Long polling | Set `timeout` (seconds). Use `offset` to acknowledge. Cannot be used while webhook is set. |
| `setWebhook` | Push | HTTPS URL, ports 443/80/88/8443. Optional secret_token. Deletes any existing webhook. |
| `deleteWebhook` | — | Clears webhook so polling can resume. |
| `getWebhookInfo` | Read-only | Safe to call; shows current URL, pending updates, last error. |

Updates are kept for 24 hours. After that they are dropped.

## Key methods
- `getMe` — returns User object for the bot. First thing to call to verify token.
- `sendMessage` — `chat_id`, `text`, optional `parse_mode` (HTML / MarkdownV2), `reply_markup`.
- `sendPhoto`, `sendDocument`, `sendVoice`, etc. — file limits: 50 MB upload on official server; 20 MB download via `getFile`.
- `answerCallbackQuery` — must be called for inline button presses or the client spinner stays.
- `setMyCommands` — programmatic equivalent of BotFather `/setcommands`.

## Gotchas
- `file_id` is bot-specific and not transferable.
- Channel/group actions (pin, ban, etc.) require the bot to be admin with the right rights.
- Privacy mode (default) means the bot does not see all group messages.
- Paid broadcasts: 30 msg/s free → up to 1000 msg/s with Stars.
- Local Bot API server (telegram-bot-api) raises file limits dramatically if you self-host it.

## House reminder
For `@ani_1kacsg_bot`: do **not** call `setWebhook` or `deleteWebhook`. Animates owns the webhook. Reach her only through a user account sending into the chat.
