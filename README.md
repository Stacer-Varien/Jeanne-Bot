# Jeanne 🌟

Jeanne is a multilingual Discord bot built with `discord.py`, `sqlite3`, and a mix of utility, media, moderation, and community-focused systems. The project is designed as a slash-command-first bot with profile progression, economy features, server tools, and a distinct anime-inspired identity.

This repository is the actual bot codebase, not just a command demo. It includes the runtime bot, event listeners, localized command text, asset generators, and the SQLite-backed data layer.

## What Jeanne Can Do ✨

### Community Systems 📈

- 📊 XP and leveling for active members
- 🏆 rank leaderboards for global and server progress
- 🪪 profile cards with wallpapers, colors, bios, badges, and country flair
- 💰 economy features such as daily rewards, balance tracking, betting, slots, spinwheel, and blackjack-style interactions

### Moderation 🛡️

- ⚖️ warn, clear warnings, timeout, remove timeout, kick, ban, unban
- ⏳ timed bans via softban tracking
- 👥 mass moderation helpers
- 📜 configurable moderation logs
- 🚫 command disabling per server

### Server Management 🛠️

- 🧱 create and manage text channels, voice channels, categories, forums, threads, roles, emojis, and stickers
- 👋 configurable welcome messages, leave messages, level-up messages, and role reward messages
- 📵 XP blacklist channels
- 🤫 confession channel setup

### Utility Features 🔧

- ⏰ reminders
- 🌦️ weather lookup
- ➗ calculator
- 📚 dictionary lookup
- ✉️ embed generation and editing
- 🐞 bot report flow
- 🕶️ anonymous confession flow
- ❓ command help lookup via `/help ask`

### Fun and Media 🎉

- 🖼️ image commands
- 💞 reaction commands such as hug, slap, pat, kiss, bite, and more
- 🎲 fun commands and lightweight social interactions
- 🛍️ inventory and wallpaper shop flows

### Localization 🌍

Jeanne ships with localized command content for:

- 🇬🇧 English
- 🇫🇷 French
- 🇩🇪 German

## Project Structure 🗂️

```text
.
|-- assets/              # UI views, generators, and image helpers
|-- cogs/                # Main slash-command and event feature groups
|-- events/              # Background tasks and listeners
|-- languages/           # Localized command implementations
|-- secret/              # Local project-only files
|-- config.py            # Env loading, tokens, API config, DB connection
|-- functions.py         # Shared business logic, DB helpers, schema bootstrap
|-- jeanne.py            # Bot entry point
|-- database.db          # SQLite database
`-- requirements.txt
```

## Tech Stack 💻

- 🐍 Python
- 💬 discord.py
- 🗃️ SQLite
- 🌐 aiohttp
- 🎨 Pillow
- 🧭 ReactionMenu
- 📄 pandas / openpyxl

## Self-Hosting 🚀

### Prerequisites 📋

- 🐍 Python `3.12+` is recommended
- 🔑 a Discord bot application and token
- 📄 a `.env` file with the variables your enabled features depend on

### Install 📦

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Configure ⚙️

The bot reads configuration from `.env` through `python-dotenv`.

At minimum, review these variables:

```env
token=
weather_api=
topgg=
topgg_auth=
db_auth=
report_webhook=
botban_webhook=
tenor=
client_key=
jeanne_album=
saber_album=
wallpaper_album=
medusa_album=
animeme_album=
neko_album=
morgan_album=
kitsune_album=
badges_album=
catbox_hash=
status=
GELBOORU_API_KEY=
GELBOORU_USER_ID=
RULE34_API_KEY=
RULE34_USER_ID=
```

Notes 📝:

- 🔐 `GELBOORU_API_KEY`, `GELBOORU_USER_ID`, `RULE34_API_KEY`, and `RULE34_USER_ID` are read as required environment variables in `config.py`.
- 🧩 Some variables power optional features, but if the current code reads them during startup, they still need to exist.
- 🔞 The mature-content command set is present in the codebase. Host responsibly and keep usage aligned with Discord rules and your local laws.

### Run ▶️

```powershell
python jeanne.py
```

## Database 🗄️

Jeanne uses `database.db` for persistent storage.

On startup, the bot now runs a schema bootstrap from [functions.py](functions.py) that:

- 🏗️ creates missing tables with `CREATE TABLE IF NOT EXISTS`
- ➕ adds a few required columns if they do not already exist
- 💾 leaves existing data in place

That means a fresh restart can rebuild the core schema automatically without manually creating tables first.

## Notes for Developers 👩‍💻

- 🧩 Commands are split between `cogs/` and localized implementations in `languages/`.
- 🗄️ Shared data logic, moderation state, leveling logic, and DB helpers live in `functions.py`.
- 🪟 UI components such as confirmations, buttons, menus, and modals live in `assets/components.py`.
- 🎨 Profile rendering is handled with Pillow in `assets/generators/profile_card.py`.
- 🔄 Background tasks such as reminder cleanup and timed-ban expiration live in `events/tasks.py`.

## Invite and Support 💬

- ➕ Invite Jeanne: https://discord.com/oauth2/authorize?client_id=831993597166747679
- 🏅 Top.gg: https://top.gg/bot/831993597166747679
- 🫂 Support server: https://discord.gg/Vfa796yvNq
- 📧 Contact: `jeannebot.discord@gmail.com`

## Disclaimer ⚠️

This is a real, evolving personal project. APIs, command behavior, and feature availability may change over time. If you self-host it, expect to maintain your own environment, secrets, assets, and feature integrations.
