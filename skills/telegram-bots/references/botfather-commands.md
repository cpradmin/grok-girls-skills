# BotFather Commands (official)

Source: https://core.telegram.org/bots/features

## Creation & ownership
- `/newbot` — Create bot. Asks for display name then username (must end in `bot`, 5-32 chars, a-z0-9_). Returns token.
- `/mybots` — Interactive menu for all owned bots.
- `/token` — Generate a new token (old one immediately invalid).
- `/deletebot` — Permanently delete bot and free username.
- Transfer ownership — via `/mybots` → bot → Transfer Ownership (only to users who have talked to the bot).

## Profile
- `/setname` — Change display name.
- `/setdescription` — Up to 512 chars. Shown when user starts the bot (“What can this bot do?”). Supports photo/video.
- `/setabouttext` — Up to 120 chars. Shown on profile.
- `/setuserpic` — Profile picture (or set from bot’s own profile page).

## Commands & behavior
- `/setcommands` — List of commands users see when they type `/`. Each: `/command` + short description. Supports scopes (private vs group, language).
- `/setprivacy` — Enable/disable privacy mode in groups (default: enabled).
- `/setinline` — Enable/disable inline mode (`@bot query` in any chat).
- `/setjoingroups` — Allow/disallow being added to groups.
- `/setdomain` — Link a domain for login widget.

## Games (if used)
- `/newgame`, `/listgames`, `/editgame`, `/deletegame`

## Other
- Mini Apps, splash screen, topics in private chats, guest mode, bot management mode — all configurable via BotFather or its Mini App.
- Status alerts: BotFather monitors response rates and notifies owner.

Always check current commands by typing `/` in BotFather — the list can grow.
