from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from enum import Enum
from random import choice, randint
import json
import aiohttp
from humanfriendly import parse_timespan
from discord import (
    Color,
    Embed,
    Guild,
    Interaction,
    Member,
    Role,
    SyncWebhook,
    TextChannel,
    User,
    app_commands as Jeanne,
)

from discord.ext.commands import Bot, Context
from requests import RequestException, get
from config import db, BB_WEBHOOK, CATBOX_HASH, GELBOORU_API, GELBOORU_USER, RULE34_API, RULE34_USER
from typing import Literal, Optional, List
from discord.app_commands import locale_str as T


TABLE_BOOTSTRAP_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS bankData (
        user_id INTEGER PRIMARY KEY,
        amount INTEGER DEFAULT 0,
        claimed_date INTEGER DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS botbannedData (
        user_id INTEGER PRIMARY KEY,
        reason TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS confessData (
        user_id INTEGER,
        server_id INTEGER,
        id INTEGER,
        confession TEXT,
        PRIMARY KEY (server_id, id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS devWarnData (
        user INTEGER,
        reason TEXT,
        warn_id INTEGER,
        revoke_date INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS disabledCommandsData (
        server INTEGER,
        command TEXT,
        PRIMARY KEY (server, command)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS globalxpData (
        user_id INTEGER PRIMARY KEY,
        lvl INTEGER DEFAULT 0,
        exp INTEGER DEFAULT 0,
        cumulative_exp INTEGER DEFAULT 0,
        next_time INTEGER DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS hentaiBlacklist (
        links TEXT PRIMARY KEY
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS hentaiCache (
        date TEXT,
        source TEXT,
        tags TEXT,
        file_url TEXT,
        UNIQUE (source, file_url)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS levelRewardData (
        server INTEGER,
        role INTEGER,
        level INTEGER,
        PRIMARY KEY (server, role)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS partnerData (
        user_id INTEGER PRIMARY KEY
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS profileFeatures (
        user_id INTEGER PRIMARY KEY,
        animated_unlocked INTEGER DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS reminderData (
        userid INTEGER,
        id INTEGER,
        time INTEGER,
        reason TEXT,
        PRIMARY KEY (userid, id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS serverData (
        server INTEGER PRIMARY KEY,
        leaving_channel INTEGER,
        welcoming_channel INTEGER,
        levelup_channel INTEGER,
        levelup_message TEXT,
        modlog INTEGER,
        welcoming_message TEXT,
        leaving_message TEXT,
        rankup_message TEXT,
        confess_channel INTEGER,
        language_override TEXT DEFAULT 'auto',
        currency_name TEXT DEFAULT 'QP',
        currency_emoji TEXT DEFAULT '<:quantumpiece:1161010445205905418>',
        disabled_modules TEXT DEFAULT ''
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS serverxpData (
        user_id INTEGER,
        guild_id INTEGER,
        lvl INTEGER DEFAULT 0,
        exp INTEGER DEFAULT 0,
        cumulative_exp INTEGER DEFAULT 0,
        next_time INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, guild_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS softbannedMembers (
        user_id INTEGER,
        guild_id INTEGER,
        ends INTEGER,
        PRIMARY KEY (user_id, guild_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS modCaseData (
        guild_id INTEGER,
        case_id INTEGER,
        action TEXT,
        target_id INTEGER,
        moderator_id INTEGER,
        reason TEXT,
        date INTEGER,
        duration TEXT,
        status TEXT,
        related_warn_id INTEGER,
        PRIMARY KEY (guild_id, case_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS suspensionData (
        user INTEGER PRIMARY KEY,
        modules TEXT,
        timeout INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS userBio (
        user_id INTEGER PRIMARY KEY,
        bio TEXT,
        color TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS userWallpaperInventory (
        user_id INTEGER,
        wallpaper TEXT,
        link TEXT,
        brightness INTEGER,
        selected INTEGER,
        country TEXT,
        animated INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, wallpaper)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS wallpapers (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        link TEXT,
        price INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS warnData (
        user_id INTEGER,
        guild_id INTEGER,
        moderator_id INTEGER,
        reason TEXT,
        warn_id INTEGER,
        date INTEGER,
        PRIMARY KEY (guild_id, user_id, warn_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS welcomerMsgData (
        server INTEGER PRIMARY KEY,
        welcoming TEXT,
        leaving TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS xpChannelData (
        server INTEGER,
        channel INTEGER,
        PRIMARY KEY (server, channel)
    )
    """,
)

COLUMN_BOOTSTRAP_STATEMENTS = {
    "globalxpData": {
        "cumulative_exp": "INTEGER DEFAULT 0",
    },
    "serverxpData": {
        "cumulative_exp": "INTEGER DEFAULT 0",
    },
    "serverData": {
        "rankup_message": "TEXT",
        "confess_channel": "INTEGER",
        "language_override": "TEXT DEFAULT 'auto'",
        "currency_name": "TEXT DEFAULT 'QP'",
        "currency_emoji": "TEXT DEFAULT '<:quantumpiece:1161010445205905418>'",
        "disabled_modules": "TEXT DEFAULT ''",
    },
    "userBio": {
        "color": "TEXT",
    },
    "userWallpaperInventory": {
        "country": "TEXT",
        "animated": "INTEGER DEFAULT 0",
    },
}


def ensure_database_schema() -> None:
    for statement in TABLE_BOOTSTRAP_STATEMENTS:
        db.execute(statement)

    for table_name, columns in COLUMN_BOOTSTRAP_STATEMENTS.items():
        existing_columns = {
            row[1] for row in db.execute(f"PRAGMA table_info({table_name})").fetchall()
        }
        for column_name, definition in columns.items():
            if column_name not in existing_columns:
                db.execute(
                    f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"
                )

    db.execute(
        "UPDATE bankData SET amount = CAST(ROUND(COALESCE(amount, 0)) AS INTEGER)"
    )
    db.commit()


SUPPORTED_SERVER_LOCALES = {"en", "fr", "de"}
DEFAULT_CURRENCY_NAME = "QP"
DEFAULT_CURRENCY_EMOJI = "<:quantumpiece:1161010445205905418>"


class ServerSettings:
    MODULES = {
        "currency": "Currency",
        "fun": "Fun",
        "hentai": "NSFW",
        "image": "Images",
        "info": "Info",
        "inventory": "Inventory",
        "levelling": "Levelling",
        "manage": "Management",
        "moderation": "Moderation",
        "reactions": "Reactions",
        "utilities": "Utilities",
    }
    MODULE_COMMAND_ROOTS = {
        "currency": {
            "balance",
            "blackjack",
            "daily",
            "dice",
            "flip",
            "guess",
            "slots",
            "spin",
            "vote",
        },
        "fun": {
            "8ball",
            "animeme",
            "avatar",
            "combine",
            "hack",
            "rate",
            "reverse",
            "ship",
            "wanted",
        },
        "hentai": {
            "danbooru",
            "gelbooru",
            "hentai",
            "konachan",
            "rule34",
            "yandere",
        },
        "image": {"image"},
        "info": {"about", "botinfo", "serverinfo", "userinfo"},
        "inventory": {"background", "bio", "profile", "shop"},
        "levelling": {"rank", "xp"},
        "manage": {
            "clone",
            "command",
            "create",
            "delete",
            "edit",
            "level",
            "manage",
            "rename",
            "set",
        },
        "moderation": {
            "ban",
            "change-nickname",
            "clear-warn",
            "kick",
            "list-warns",
            "massban",
            "massunban",
            "prune",
            "timeout",
            "timeout-remove",
            "unban",
            "warn",
        },
        "reactions": {
            "bite",
            "blush",
            "cry",
            "cuddle",
            "dance",
            "hug",
            "kill",
            "kiss",
            "lick",
            "pat",
            "poke",
            "slap",
            "smug",
        },
        "utilities": {
            "calculate",
            "confession",
            "define",
            "embed",
            "reminder",
            "say",
            "search",
            "weather",
        },
    }

    def __init__(self, server: Guild | int) -> None:
        self.server_id = server.id if hasattr(server, "id") else int(server)

    def _ensure_row(self) -> None:
        db.execute(
            """
            INSERT OR IGNORE INTO serverData
                (server, language_override, currency_name, currency_emoji, disabled_modules)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                self.server_id,
                "auto",
                DEFAULT_CURRENCY_NAME,
                DEFAULT_CURRENCY_EMOJI,
                "",
            ),
        )
        db.commit()

    @property
    def row(self) -> dict:
        self._ensure_row()
        data = db.execute(
            """
            SELECT
                leaving_channel,
                welcoming_channel,
                levelup_channel,
                levelup_message,
                modlog,
                welcoming_message,
                leaving_message,
                rankup_message,
                confess_channel,
                language_override,
                currency_name,
                currency_emoji,
                disabled_modules
            FROM serverData
            WHERE server = ?
            """,
            (self.server_id,),
        ).fetchone()
        keys = (
            "leaving_channel",
            "welcoming_channel",
            "levelup_channel",
            "levelup_message",
            "modlog",
            "welcoming_message",
            "leaving_message",
            "rankup_message",
            "confess_channel",
            "language_override",
            "currency_name",
            "currency_emoji",
            "disabled_modules",
        )
        return dict(zip(keys, data, strict=False))

    @property
    def language_override(self) -> str:
        value = self.row.get("language_override") or "auto"
        return value if value in (*SUPPORTED_SERVER_LOCALES, "auto") else "auto"

    async def set_language_override(self, language: str) -> None:
        if language not in (*SUPPORTED_SERVER_LOCALES, "auto"):
            raise ValueError("Unsupported language override")
        self._ensure_row()
        db.execute(
            "UPDATE serverData SET language_override = ? WHERE server = ?",
            (language, self.server_id),
        )
        db.commit()

    @property
    def currency_name(self) -> str:
        return str(self.row.get("currency_name") or DEFAULT_CURRENCY_NAME)

    @property
    def currency_emoji(self) -> str:
        return str(self.row.get("currency_emoji") or DEFAULT_CURRENCY_EMOJI)

    async def set_currency_display(
        self, name: str | None = None, emoji: str | None = None
    ) -> None:
        name = (name or DEFAULT_CURRENCY_NAME).strip()[:32] or DEFAULT_CURRENCY_NAME
        emoji = (emoji or "").strip()[:80]
        self._ensure_row()
        db.execute(
            "UPDATE serverData SET currency_name = ?, currency_emoji = ? WHERE server = ?",
            (name, emoji, self.server_id),
        )
        db.commit()

    def format_currency(self, amount: int | float | Decimal) -> str:
        amount = Currency.normalize_qp(amount)
        name = self.currency_name
        emoji = self.currency_emoji
        if emoji and name and name != DEFAULT_CURRENCY_NAME:
            return f"{amount} {emoji} {name}"
        if emoji:
            return f"{amount} {emoji}"
        return f"{amount} {name}"

    @staticmethod
    def format_currency_for(server: Guild | int | None, amount: int | float | Decimal) -> str:
        if server is None:
            amount = Currency.normalize_qp(amount)
            return f"{amount} {DEFAULT_CURRENCY_EMOJI}"
        return ServerSettings(server).format_currency(amount)

    @property
    def disabled_modules(self) -> list[str]:
        raw_value = self.row.get("disabled_modules") or ""
        try:
            modules = json.loads(raw_value)
        except (TypeError, json.JSONDecodeError):
            modules = [item for item in str(raw_value).split(",") if item]
        return [module for module in modules if module in self.MODULES]

    async def set_module_enabled(self, module: str, enabled: bool) -> None:
        if module not in self.MODULES:
            raise ValueError("Unsupported module")
        modules = set(self.disabled_modules)
        if enabled:
            modules.discard(module)
        else:
            modules.add(module)
        self._ensure_row()
        db.execute(
            "UPDATE serverData SET disabled_modules = ? WHERE server = ?",
            (json.dumps(sorted(modules)), self.server_id),
        )
        db.commit()

    def is_module_disabled(self, module: str) -> bool:
        return module in self.disabled_modules

    @classmethod
    def command_module(cls, command) -> str | None:
        if command is None:
            return None
        callback = getattr(command, "callback", None)
        module_name = getattr(callback, "__module__", "")
        if module_name.startswith("cogs."):
            module_name = module_name.split(".")[-1]
            if module_name in cls.MODULES:
                return module_name

        qualified_name = getattr(command, "qualified_name", "")
        root = qualified_name.split()[0] if qualified_name else ""
        for module, roots in cls.MODULE_COMMAND_ROOTS.items():
            if root in roots:
                return module
        return None

    def setup_status(self, server: Guild | None = None) -> dict:
        data = self.row

        def channel_state(key: str) -> dict:
            channel_id = data.get(key)
            channel = server.get_channel(channel_id) if server and channel_id else None
            return {
                "configured": channel_id is not None,
                "channel_id": channel_id,
                "channel": channel,
                "missing": channel_id is not None and channel is None,
            }

        return {
            "welcome": channel_state("welcoming_channel"),
            "leave": channel_state("leaving_channel"),
            "modlog": channel_state("modlog"),
            "level": channel_state("levelup_channel"),
            "confession": channel_state("confess_channel"),
            "language_override": self.language_override,
            "currency_name": self.currency_name,
            "currency_emoji": self.currency_emoji,
            "disabled_modules": self.disabled_modules,
        }


def _coerce_locale(value: object) -> str:
    locale = getattr(value, "value", value)
    locale = str(locale or "en")
    if locale == "fr":
        return "fr"
    if locale == "de":
        return "de"
    return "en"


def get_guild_locale(server: Guild | None) -> str:
    if server is None:
        return "en"
    override = ServerSettings(server).language_override
    if override in SUPPORTED_SERVER_LOCALES:
        return override
    return _coerce_locale(getattr(server, "preferred_locale", "en"))


def get_command_locale(ctx: Interaction) -> str:
    if getattr(ctx, "guild", None) is not None:
        return get_guild_locale(ctx.guild)
    return _coerce_locale(getattr(ctx, "locale", "en"))


class DevPunishment:
    def __init__(self, user: Optional[User] = None) -> None:
        self.user = user

    @property
    def check_botbanned_user(self):
        botbanned_data = db.execute(
            "SELECT * FROM botbannedData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return botbanned_data is not None and self.user.id == botbanned_data[0]

    async def add_botbanned_user(self, reason: str):
        db.execute(
            "INSERT OR IGNORE INTO botbannedData (user_id, reason) VALUES (?, ?)",
            (
                self.user.id,
                reason,
            ),
        )
        db.execute("DELETE FROM serverxpData WHERE user_id = ?", (self.user.id,))
        db.execute("DELETE FROM globalxpData WHERE user_id = ?", (self.user.id,))
        db.execute(
            "DELETE FROM userWallpaperInventory WHERE user_id = ?", (self.user.id,)
        )
        db.execute("DELETE FROM profileFeatures WHERE user_id = ?", (self.user.id,))
        db.execute("DELETE FROM bankData WHERE user_id = ?", (self.user.id,))
        db.commit()
        botbanned = Embed(
            title="User has been botbanned!",
            description="They will no longer use Jeanne, permanently!",
        )
        botbanned.add_field(name="User", value=self.user)
        botbanned.add_field(name="ID", value=self.user.id, inline=True)
        botbanned.add_field(
            name="Reason of ban",
            value=reason,
            inline=False,
        )
        botbanned.set_footer(
            text="Due to this user botbanned, all data except warnings are immediately deleted from the database! They will have no chance of appealing their botban and all the commands executed by them are now rendered USELESS!"
        )
        botbanned.set_thumbnail(url=self.user.display_avatar)
        webhook = SyncWebhook.from_url(BB_WEBHOOK)
        webhook.send(embed=botbanned)

    def warnpoints(self) -> int:
        data = db.execute(
            "SELECT * FROM devWarnData WHERE user = ?", (self.user.id,)
        ).fetchall()
        db.commit()
        return 0 if not data else len(data)

    async def autopunish(self):
        points = self.warnpoints()
        db.commit()
        if points == 1:
            return
        if points == 2:
            duration = timedelta(days=7)
            await self.suspend(
                duration.total_seconds(),
                [
                    "cogs.utilities",
                    "cogs.fun",
                    "cogs.image",
                    "cogs.help",
                    "cogs.hentai",
                    "cogs.levelling",
                    "cogs.currency",
                    "cogs.reactions",
                    "cogs.manage",
                    "cogs.inventory",
                    "cogs.moderation",
                    "cogs.info",
                ],
                "Recieved 2 bot warnings",
            )
            return
        if points == 3:
            await self.add_botbanned_user("Recieved 3 bot warnings")
            return

    async def suspend(self, duration: int, modules: list[str], reason: str):
        data = db.execute(
            "INSERT OR IGNORE INTO suspensionData (user, modules, timeout) VALUES (?,?,?)",
            (
                self.user.id,
                ",".join(modules),
                round((datetime.now() + timedelta(seconds=duration)).timestamp()),
            ),
        )
        db.commit()

        if data.rowcount == 0:
            data = db.execute(
                "SELECT timeout FROM suspensionDATA WHERE user = ?", (self.user.id,)
            ).fetchone()
            db.commit()
            current_timeout_duration = datetime.fromtimestamp(float(data[0]))
            new_timeout = round(
                (current_timeout_duration + timedelta(seconds=duration)).timestamp()
            )
            db.execute(
                "UPDATE suspensionDATA SET modules = ?, timeout = ? WHERE user = ?",
                (",".join(modules), new_timeout, self.user.id),
            )
            db.commit()

        timeout = db.execute(
            "SELECT timeout FROM suspensionDATA WHERE user = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        embed = Embed(title="User has been Dev Suspended", color=Color.yellow())
        embed.add_field(name="User", value=self.user, inline=True)
        embed.add_field(name="ID", value=self.user.id, inline=True)
        embed.add_field(
            name="Suspended until", value=f"<t:{timeout[0]}:f>", inline=True
        )
        embed.add_field(name="Modules", value="\n".join(modules).title(), inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(
            text="This is not a botban. The user is suspended from using certain modules of Jeanne."
        )
        embed.set_thumbnail(url=self.user.display_avatar)
        webhook = SyncWebhook.from_url(BB_WEBHOOK)
        webhook.send(embed=embed)

    async def warn(self, reason: str):
        warn_id = randint(1, 9999999)
        points = self.warnpoints()
        revoke_date = None
        if points == 2:
            revoke_date = round((datetime.now() + timedelta(days=180)).timestamp())
        elif points:
            revoke_date = round((datetime.now() + timedelta(days=90)).timestamp())
        db.execute(
            "INSERT OR IGNORE INTO devWarnData (user, reason, warn_id, revoke_date) VALUES (?,?,?,?)",
            (
                self.user.id,
                reason,
                warn_id,
                revoke_date,
            ),
        )
        db.commit()
        embed = Embed(title="User has been Dev Warned", color=Color.yellow())
        embed.add_field(name="User", value=self.user, inline=True)
        embed.add_field(name="ID", value=self.user.id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Warn ID", value=warn_id, inline=True)
        embed.add_field(name="Points", value=self.warnpoints())
        embed.set_thumbnail(url=self.user.display_avatar)
        webhook = SyncWebhook.from_url(BB_WEBHOOK)
        webhook.send(embed=embed)
        await self.autopunish()

    def check_suspended_module(self, bot: Bot, command: Jeanne.Command) -> bool:
        data = db.execute(
            "SELECT * FROM suspensionData WHERE user = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        suspended_modules: list[str] = data[1].split(",") if data else []
        cog = next(
            (
                cmd.module
                for cmd in bot.tree.walk_commands()
                if not isinstance(cmd, Jeanne.Group)
                and cmd.qualified_name == command.qualified_name
            ),
            None,
        )
        if cog and any(module in cog for module in suspended_modules):
            return True
        return False

    def get_suspended_users(self):
        data = db.execute("SELECT * FROM suspensionData").fetchall()
        db.commit()
        return data

    async def remove_suspended_user(self):
        db.execute("DELETE FROM suspensionData WHERE user = ?", (self.user.id,))
        db.commit()


class Currency:
    def __init__(self, user: User):
        self.user = user

    @staticmethod
    def _qp_decimal(amount: int | float | str | Decimal) -> Decimal:
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("QP amount must be a valid number") from exc
        if not value.is_finite():
            raise ValueError("QP amount must be a valid number")
        return value

    @staticmethod
    def normalize_qp(amount: int | float | str | Decimal) -> int:
        value = Currency._qp_decimal(amount)
        return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    @staticmethod
    def is_negative_qp(amount: int | float | str | Decimal) -> bool:
        return Currency._qp_decimal(amount) < 0

    def _ensure_bank_row(self) -> None:
        previous_day = round((datetime.now() - timedelta(days=1)).timestamp())
        db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (
                self.user.id,
                0,
                previous_day,
            ),
        )
        db.execute(
            "UPDATE bankData SET amount = CAST(ROUND(COALESCE(amount, 0)) AS INTEGER) WHERE user_id = ?",
            (self.user.id,),
        )
        db.commit()

    @property
    def get_balance(self) -> int:
        data = db.execute(
            "SELECT amount FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        if data is None:
            return 0
        balance = self.normalize_qp(data[0])
        if data[0] != balance:
            db.execute(
                "UPDATE bankData SET amount = ? WHERE user_id = ?",
                (
                    balance,
                    self.user.id,
                ),
            )
            db.commit()
        return balance

    async def add_qp(self, amount: int | float | str | Decimal) -> int:
        if self.is_negative_qp(amount):
            raise ValueError("QP amount cannot be negative")
        amount = self.normalize_qp(amount)
        self._ensure_bank_row()
        if amount == 0:
            return 0
        db.execute(
            "UPDATE bankData SET amount = amount + ? WHERE user_id = ?",
            (
                amount,
                self.user.id,
            ),
        )
        db.commit()
        return amount

    async def remove_qp(self, amount: int | float | str | Decimal) -> int:
        if self.is_negative_qp(amount):
            raise ValueError("QP amount cannot be negative")
        amount = self.normalize_qp(amount)
        self._ensure_bank_row()
        if amount == 0:
            return 0
        removed = min(self.get_balance, amount)
        db.execute(
            """
            UPDATE bankData
            SET amount = CASE
                WHEN amount - ? < 0 THEN 0
                ELSE amount - ?
            END
            WHERE user_id = ?
            """,
            (
                amount,
                amount,
                self.user.id,
            ),
        )
        db.commit()
        return removed

    async def set_qp(self, amount: int | float | str | Decimal) -> int:
        if self.is_negative_qp(amount):
            raise ValueError("QP amount cannot be negative")
        amount = self.normalize_qp(amount)
        self._ensure_bank_row()
        db.execute(
            "UPDATE bankData SET amount = ? WHERE user_id = ?",
            (
                amount,
                self.user.id,
            ),
        )
        db.commit()
        return amount

    async def give_daily(self):
        next_claim = round((datetime.now() + timedelta(days=1)).timestamp())
        qp = 200 if (datetime.today().weekday() > 4) else 100
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (
                self.user.id,
                qp,
                next_claim,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET claimed_date = ?, amount = amount + ? WHERE user_id = ?",
                (
                    next_claim,
                    qp,
                    self.user.id,
                ),
            )
            db.commit()

    async def claim_daily(self) -> int | None:
        now = round(datetime.now().timestamp())
        next_claim = round((datetime.now() + timedelta(days=1)).timestamp())
        qp = 200 if (datetime.today().weekday() > 4) else 100

        cur = db.execute(
            """
            UPDATE bankData
            SET claimed_date = ?, amount = amount + ?
            WHERE user_id = ? AND claimed_date < ?
            """,
            (
                next_claim,
                qp,
                self.user.id,
                now,
            ),
        )
        db.commit()
        if cur.rowcount == 1:
            return next_claim

        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (
                self.user.id,
                qp,
                next_claim,
            ),
        )
        db.commit()
        if cur.rowcount == 1:
            return next_claim

        return None

    @property
    def check_daily(self) -> int | Literal[True]:
        data = db.execute(
            "SELECT claimed_date FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        if (data is None) or (int(data[0]) < round(datetime.now().timestamp())):
            return True
        return int(data[0])


class Inventory:
    def __init__(self, user: Optional[User] = None) -> None:
        self.user = user

    @staticmethod
    async def upload_to_catbox(image_url: str) -> str | None:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            url = "https://catbox.moe/user/api.php"
            userhash = CATBOX_HASH
            data = {"reqtype": "urlupload", "userhash": userhash, "url": image_url}
            async with session.post(url, data=data) as response:
                if response.status != 200:
                    return None
                uploaded_url = (await response.text()).strip()

        if uploaded_url.startswith("http"):
            return uploaded_url
        return None

    async def add_country(self, country: str):
        db.execute(
            "UPDATE userWallpaperInventory SET country = ? WHERE user_id = ?",
            (
                country,
                self.user.id,
            ),
        )
        db.commit()
        await Currency(self.user).remove_qp(500)

    @property
    def selected_country(self) -> str | None:
        data = db.execute(
            "SELECT country FROM userWallpaperInventory WHERE user_id = ? AND selected = ?",
            (
                self.user.id,
                1,
            ),
        ).fetchone()
        db.commit()
        return None if data is None else data[0]

    @staticmethod
    def fetch_wallpapers() -> list:
        data = db.execute("SELECT * FROM wallpapers").fetchall()
        db.commit()
        return data

    @staticmethod
    def get_wallpaper(name: str) -> tuple[str, str, str]:
        wallpaper = db.execute(
            "SELECT * FROM wallpapers WHERE name = ?", (name,)
        ).fetchone()
        db.commit()
        return str(wallpaper[0]), str(wallpaper[1]), str(wallpaper[2])

    async def deselect_wallpaper(self) -> Literal[True] | None:
        wallpaper = db.execute(
            "SELECT wallpaper FROM userWallpaperInventory WHERE user_id = ? AND selected = ?",
            (
                self.user.id,
                1,
            ),
        ).fetchone()
        db.commit()
        if wallpaper is None:
            return None
        db.execute(
            "UPDATE userWallpaperInventory SET selected = ? WHERE user_id = ? AND wallpaper = ?",
            (
                0,
                self.user.id,
                wallpaper[0],
            ),
        )
        db.commit()
        return True

    async def add_user_wallpaper(self, name: str):
        await self.deselect_wallpaper()
        wallpaper = self.get_wallpaper(name)
        db.execute(
            "INSERT OR IGNORE INTO userWallpaperInventory (user_id, wallpaper, link, brightness, selected) VALUES (?,?,?,?,?)",
            (
                self.user.id,
                wallpaper[1],
                wallpaper[2],
                100,
                1,
            ),
        )
        db.commit()
        await Currency(self.user).remove_qp(1000)

    async def add_user_custom_wallpaper(
        self, name: str, url: str, price: int = 1500, animated: bool = False
    ) -> bool:
        if not url:
            return False
        if animated and not self.animated_profile_unlocked:
            return False
        if Currency(self.user).get_balance < price:
            return False

        cur = db.execute(
            "INSERT OR IGNORE INTO userWallpaperInventory "
            "(user_id, wallpaper, link, brightness, selected, animated) "
            "VALUES (?,?,?,?,?,?)",
            (
                self.user.id,
                name,
                url,
                100,
                0,
                int(animated),
            ),
        )
        if cur.rowcount == 0:
            return False

        await self.deselect_wallpaper()
        db.execute(
            "UPDATE userWallpaperInventory SET selected = 1 "
            "WHERE user_id = ? AND wallpaper = ?",
            (
                self.user.id,
                name,
            ),
        )
        db.commit()
        await Currency(self.user).remove_qp(price)
        return True

    @property
    def animated_profile_unlocked(self) -> bool:
        data = db.execute(
            "SELECT animated_unlocked FROM profileFeatures WHERE user_id = ?",
            (self.user.id,),
        ).fetchone()
        return data is not None and bool(data[0])

    async def unlock_animated_profile(self, price: int = 10000) -> bool:
        if self.animated_profile_unlocked:
            return True
        price = Currency.normalize_qp(price)
        bank = Currency(self.user)
        if price < 0 or bank.get_balance < price:
            return False
        await bank.remove_qp(price)
        db.execute(
            "INSERT OR REPLACE INTO profileFeatures (user_id, animated_unlocked) "
            "VALUES (?, 1)",
            (self.user.id,),
        )
        db.commit()
        return True

    @property
    def selected_wallpaper(self) -> str | None:
        wallpaper = db.execute(
            "SELECT link FROM userWallpaperInventory WHERE user_id = ? and selected = ?",
            (
                self.user.id,
                1,
            ),
        ).fetchone()
        db.commit()
        return None if (wallpaper is None) else str(wallpaper[0])

    @property
    def selected_wallpaper_is_animated(self) -> bool:
        wallpaper = db.execute(
            "SELECT animated FROM userWallpaperInventory "
            "WHERE user_id = ? AND selected = ?",
            (self.user.id, 1),
        ).fetchone()
        return wallpaper is not None and bool(wallpaper[0])

    async def use_wallpaper(self, name: str):
        await self.deselect_wallpaper()
        db.execute(
            "UPDATE userWallpaperInventory SET selected = ? WHERE wallpaper = ? AND user_id = ?",
            (
                1,
                name,
                self.user.id,
            ),
        )
        db.commit()

    @property
    def get_user_inventory(self) -> list | None:
        wallpapers = db.execute(
            "SELECT * FROM userWallpaperInventory WHERE user_id = ?", (self.user.id,)
        ).fetchall()
        return wallpapers if wallpapers else None

    @property
    def get_brightness(self) -> int:
        data = db.execute(
            "SELECT brightness FROM userWallpaperInventory WHERE user_id = ? and selected = ?",
            (
                self.user.id,
                1,
            ),
        ).fetchone()
        return 100 if (data is None) else int(data[0])

    async def set_brightness(self, brightness: int) -> bool:
        try:
            data = db.execute(
                "UPDATE userWallpaperInventory SET brightness = ? WHERE user_id = ? AND selected = ?",
                (
                    brightness,
                    self.user.id,
                    1,
                ),
            )
            db.commit()
            return data.rowcount > 0
        except Exception:
            return False

    async def set_bio(self, bio: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO userBio (user_id, bio) VALUES (?,?)",
            (
                self.user.id,
                bio,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            db.execute(
                "UPDATE userBio SET bio = ? WHERE user_id = ?",
                (
                    bio,
                    self.user.id,
                ),
            )
            db.commit()

    @property
    def get_bio(self) -> str | None:
        data = db.execute(
            "SELECT bio FROM userBio WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return str(data[0]) if data else None

    async def set_color(self, color: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO userBio (user_id, color) VALUES (?,?)",
            (
                self.user.id,
                color,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            db.execute(
                "UPDATE userBio SET color = ? WHERE user_id = ?",
                (
                    color,
                    self.user.id,
                ),
            )
            db.commit()

    @property
    def get_color(self) -> str | None:
        data = db.execute(
            "SELECT color FROM userBio WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return str(data[0]) if data else None


class Levelling:
    def __init__(
        self, member: Optional[Member] = None, server: Optional[Guild] = None
    ) -> None:
        self.member = member
        self.server = server

    @property
    def get_member_xp(self) -> int:
        xp = db.execute(
            "SELECT exp FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (self.member.id, self.server.id),
        ).fetchone()
        return 0 if xp is None else int(xp[0])

    @property
    def get_user_xp(self) -> int:
        xp = db.execute(
            "SELECT exp FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        return 0 if xp is None else int(xp[0])

    @property
    def get_member_cumulated_xp(self) -> int:
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (self.member.id, self.server.id),
        ).fetchone()
        return 0 if cumulated_exp is None else int(cumulated_exp[0])

    @property
    def get_user_cumulated_xp(self) -> int:
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM globalxpData WHERE user_id = ?",
            (self.member.id,),
        ).fetchone()
        return 0 if cumulated_exp is None else int(cumulated_exp[0])

    @property
    def get_next_time_server(self) -> int:
        next_time = db.execute(
            "SELECT next_time FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (self.member.id, self.server.id),
        ).fetchone()
        return int(next_time[0]) if next_time and next_time[0] is not None else 0

    @property
    def get_next_time_global(self) -> int:
        next_time = db.execute(
            "SELECT next_time FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        return int(next_time[0]) if next_time and next_time[0] is not None else 0

    @property
    def get_member_level(self) -> int:
        level = db.execute(
            "SELECT lvl FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (self.member.id, self.server.id),
        ).fetchone()
        return int(level[0]) if level and level[0] is not None else 0

    @property
    def get_user_level(self) -> int:
        level = db.execute(
            "SELECT lvl FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        return int(level[0]) if level and level[0] is not None else 0

    async def add_xp(self, xp: int):
        now_time = round(datetime.now().timestamp())
        next_time = round((datetime.now() + timedelta(minutes=2)).timestamp())

        global_cursor = db.execute(
            "INSERT OR IGNORE INTO globalxpData (user_id, lvl, exp, next_time) VALUES (?, ?, ?, ?)",
            (self.member.id, 0, xp, next_time),
        )
        db.commit()

        if global_cursor.rowcount == 0:
            if now_time >= self.get_next_time_global:
                global_exp = self.get_user_xp
                global_updated_exp = global_exp + xp
                db.execute(
                    "UPDATE globalxpData SET exp = ?, next_time = ? WHERE user_id = ?",
                    (
                        global_updated_exp,
                        next_time,
                        self.member.id,
                    ),
                )


                global_level = self.get_user_level
                global_next_lvl_exp = (global_level * 50) + ((global_level - 1) * 25) + 50
                if global_updated_exp >= global_next_lvl_exp:
                    db.execute(
                        "UPDATE globalxpData SET lvl = lvl + ?, exp = ? WHERE user_id = ?",
                        (1, 0, self.member.id),
                    )



        server_cursor = db.execute(
            "INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, next_time) VALUES (?, ?, ?, ?, ?)",
            (self.server.id, self.member.id, 0, xp, next_time),
        )


        if server_cursor.rowcount == 0:
            if now_time >= self.get_next_time_server:
                server_exp = self.get_member_xp
                server_updated_exp = server_exp + xp
                db.execute(
                    "UPDATE serverxpData SET exp = ?, next_time = ? WHERE guild_id = ? AND user_id = ?",
                    (
                        server_updated_exp,
                        next_time,
                        self.server.id,
                        self.member.id,
                    ),
                )


                server_level = self.get_member_level
                server_next_lvl_exp = (server_level * 50) + ((server_level - 1) * 25) + 50
                if server_updated_exp >= server_next_lvl_exp:
                    db.execute(
                        "UPDATE serverxpData SET lvl = lvl + ?, exp = ? WHERE guild_id = ? AND user_id = ?",
                        (
                            1,
                            0,
                            self.server.id,
                            self.member.id,
                        ),
                    )

                    return self.get_level_channel

    @property
    def get_level_channel(
        self,
    ) -> tuple[Optional[TextChannel], Optional[str], Optional[str]]:
        return self.get_levelup_channel, self.get_levelup_msg, self.get_rank_up_update

    @property
    def get_levelup_msg(self) -> Optional[str]:
        data = db.execute(
            "SELECT levelup_message FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        
        return str(data[0]) if data and data[0] is not None else None

    @property
    def get_levelup_channel(self) -> Optional[TextChannel]:
        data = db.execute(
            "SELECT levelup_channel FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        return self.server.get_channel(data[0]) if data and data[0] is not None else None

    @property
    def get_rank_up_update(self) -> Optional[str]:
        data = db.execute(
            "SELECT rankup_message FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        return str(data[0]) if data and data[0] is not None else None

    @property
    def get_role_reward(self) -> Optional[Role]:
        data = db.execute(
            "SELECT role FROM levelRewardData WHERE server = ? AND level = ?",
            (self.server.id, self.get_member_level),
        ).fetchone()
        
        return self.server.get_role(data[0]) if data and data[0] is not None else None

    @property
    def get_server_rank(self) -> Optional[List]:
        leaders_query = db.execute(
            "SELECT * FROM serverxpData WHERE guild_id = ? ORDER BY lvl DESC LIMIT 15;",
            (self.server.id,),
        )
        db.commit()
        return leaders_query.fetchall()

    @property
    def get_global_rank(self) -> Optional[List]:
        leaders_query = db.execute(
            "SELECT * FROM globalxpData ORDER BY lvl DESC LIMIT 15;"
        )
        db.commit()
        return leaders_query.fetchall()

    def check_xpblacklist_channel(self, channel: TextChannel) -> Optional[TextChannel]:
        data = db.execute(
            "SELECT channel FROM xpChannelData WHERE server = ? AND channel = ?",
            (self.server.id, channel.id),
        ).fetchone()
        db.commit()
        if data is None:
            return None
        return self.server.get_channel(data[0]) if data is not None else False

    @property
    def get_member_server_rank(self) -> Optional[int]:
        result = db.execute(
            "SELECT user_id FROM serverxpData WHERE guild_id = ? ORDER BY exp DESC",
            (self.member.guild.id,),
        ).fetchall()
        all_ids = [item[0] for item in result]
        if self.member.id not in all_ids:
            return None
        rank = all_ids.index(self.member.id)
        return rank + 1

    @property
    def get_user_global_rank(self) -> Optional[int]:
        result = db.execute(
            "SELECT user_id FROM globalxpData ORDER BY exp DESC"
        ).fetchall()
        all_ids = [item[0] for item in result]
        if self.member.id not in all_ids:
            return None
        rank = all_ids.index(self.member.id)
        return rank + 1

    @property
    def get_blacklisted_channels(self) -> list[TextChannel] | None:
        data = db.execute(
            "SELECT channel FROM xpChannelData WHERE server = ?", (self.server.id,)
        ).fetchall()
        db.commit()
        return [self.server.get_channel(i[0]) for i in data] if data else None

    @property
    def list_all_roles(self) -> list | None:
        data = db.execute(
            "SELECT * FROM levelRewardData WHERE server = ? ORDER BY level ASC",
            (self.server.id,),
        ).fetchall()
        db.commit()
        return [i for i in data] if data else None


class Manage:
    def __init__(self, server: Guild) -> None:
        self.server = server

    async def remove_blacklist(self, channel: TextChannel):
        db.execute(
            "DELETE FROM xpChannelData WHERE server = ? AND channel = ?",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

    async def add_level_channel(
        self, channel: TextChannel, message: Optional[str] = None
    ) -> None:
        message = message if message else "0"
        cur = db.execute(
            "INSERT OR IGNORE INTO serverData (server, levelup_channel, levelup_message) VALUES (?,?,?)",
            (
                self.server.id,
                channel.id,
                message,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            if channel:
                db.execute(
                    "UPDATE serverData SET levelup_channel = ? WHERE server =?",
                    (
                        channel.id,
                        self.server.id,
                    ),
                )
                db.commit()
            if message:
                db.execute(
                    "UPDATE serverData SET levelup_message = ? WHERE server =?",
                    (
                        message,
                        self.server.id,
                    ),
                )
                db.commit()

    async def add_rankup_rolereward(self, message: Optional[str] = None) -> None:
        message = message if message else "0"
        cur = db.execute(
            "INSERT OR IGNORE INTO serverData (server, rankup_message) VALUES (?,?)",
            (
                self.server.id,
                message,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            if message:
                db.execute(
                    "UPDATE serverData SET rankup_message = ? WHERE server =?",
                    (
                        message,
                        self.server.id,
                    ),
                )
                db.commit()

    async def add_xpblacklist(self, channel: TextChannel):
        db.execute(
            "INSERT OR IGNORE INTO xpChannelData (server, channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

    async def add_role_reward(self, role: Role, level: int):
        data = db.execute(
            "INSERT OR IGNORE INTO levelRewardData (server, role, level) VALUES (?,?,?)",
            (
                self.server.id,
                role.id,
                level,
            ),
        )
        db.commit()
        if data.rowcount == 0:
            db.execute(
                "UPDATE levelRewardData SET level = ? WHERE server = ? AND role = ?",
                (
                    level,
                    self.server.id,
                    role.id,
                ),
            )
            db.commit()

    async def remove_role_reward(self, role: Role) -> Literal[True] | None:
        data = db.execute(
            "SELECT role FROM levelRewardData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        if data is None:
            return None
        db.execute(
            "DELETE FROM levelRewardData WHERE server = ? AND role = ?",
            (
                self.server.id,
                role.id,
            ),
        )
        db.commit()
        return True

    async def set_welcomer_msg(self, json_script: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO serverData (server, welcoming_message, leaving_message) VALUES (?,?,?)",
            (
                self.server.id,
                json_script,
                0,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            db.execute(
                "UPDATE serverData SET welcoming_message = ? WHERE server = ?",
                (
                    json_script,
                    self.server.id,
                ),
            )
            db.commit()

    async def set_leaving_msg(self, json_script: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO serverData (server, welcoming_message, leaving_message) VALUES (?,?,?)",
            (
                self.server.id,
                0,
                json_script,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            db.execute(
                "UPDATE serverData SET leaving_message = ? WHERE server = ?",
                (
                    json_script,
                    self.server.id,
                ),
            )
            db.commit()

    async def set_welcomer(self, channel: TextChannel):
        cursor = db.execute(
            "INSERT OR IGNORE INTO serverData (server, welcoming_channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()
        if cursor.rowcount == 0:
            db.execute(
                "UPDATE serverData SET welcoming_channel = ? WHERE server = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
            db.commit()

    async def set_leaver(self, channel: TextChannel):
        cursor = db.execute(
            "INSERT OR IGNORE INTO serverData (server, leaving_channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()
        if cursor.rowcount == 0:
            db.execute(
                "UPDATE serverData SET leaving_channel = ? WHERE server = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
        db.commit()

    async def set_modloger(self, channel: TextChannel):
        cursor = db.execute(
            "INSERT OR IGNORE INTO serverData (server, modlog) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()
        if cursor.rowcount == 0:
            db.execute(
                "UPDATE serverData SET modlog = ? WHERE server = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
            db.commit()

    async def remove_welcomer(self):
        db.execute(
            "UPDATE serverData SET welcoming_channel = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def remove_leaver(self):
        db.execute(
            "UPDATE serverData SET leaving_channel = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def remove_modloger(self):
        db.execute(
            "UPDATE serverData SET modlog = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def remove_levelup(self):
        db.execute(
            "UPDATE serverData SET levelup_channel = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def remove_levelup_msg(self):
        db.execute(
            "UPDATE serverData SET levelup_message = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def remove_rolereward_msg(self):
        db.execute(
            "UPDATE serverData SET rankup_message = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def remove_welcomemsg(self):
        db.execute(
            "UPDATE serverData SET welcoming_message = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def remove_leavingmsg(self):
        db.execute(
            "UPDATE serverData SET leaving_message = ? WHERE server = ?",
            (
                None,
                self.server.id,
            ),
        )
        db.commit()

    async def add_confession_channel(self, channel: TextChannel):
        cursor = db.execute(
            "INSERT OR IGNORE INTO serverData (server, confess_channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()
        if cursor.rowcount == 0:
            db.execute(
                "UPDATE serverData SET confess_channel = ? WHERE server = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
            db.commit()


class Confess:
    def __init__(self, server: Guild) -> None:
        self.server=server

    @property
    def get_confession_channel(self) -> TextChannel | None:
        data = db.execute(
            "SELECT confess_channel FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return None if data is None else self.server.get_channel(data[0])

    async def add_confession(self, user: User, confession_id:int, confession: str):
        db.execute(
            "INSERT OR IGNORE INTO confessData (user_id, server_id, id, confession) VALUES (?,?,?,?)",
            (
                user.id,
                self.server.id,
                confession_id,
                confession
            ),
        )
        db.commit()
    
    async def get_confessions(self) -> list | None:
        data = db.execute("SELECT * FROM confessData WHERE server_id = ?", (self.server.id,)).fetchall() #needs attention
        db.commit()
        return data if data else None
    
    async def get_confession(self, confession_id: int) -> tuple | None:
        data = db.execute(
            "SELECT * FROM confessData WHERE server_id = ? AND id = ?",
            (self.server.id, confession_id),
        ).fetchone()
        db.commit()
        return data if data else None


class Command:
    def __init__(self, server: Guild) -> None:
        self.server = server

    def check_disabled(self, command: str):
        try:
            data = db.execute(
                "SELECT command FROM disabledCommandsData WHERE server = ? AND command = ?",
                (
                    self.server.id,
                    command,
                ),
            ).fetchone()
            db.commit()
            return data is not None and command == data[0]
        except Exception:
            return False

    async def disable(self, command: str):
        db.execute(
            "INSERT OR IGNORE INTO disabledCommandsData (server, command) VALUES (?,?)",
            (
                self.server.id,
                command,
            ),
        )
        db.commit()

    async def enable(self, command: str):
        db.execute(
            "DELETE FROM disabledCommandsData WHERE server = ? AND command = ?",
            (
                self.server.id,
                command,
            ),
        )
        db.commit()

    @property
    def list_all_disabled(self) -> list[str]:
        data = db.execute(
            "SELECT command FROM disabledCommandsData WHERE server = ?",
            (self.server.id,),
        ).fetchall()
        db.commit()
        return [str(i[0]) for i in data] if data else None


class Moderation:
    def __init__(self, server: Optional[Guild] = None) -> None:
        self.server = server

    def _next_case_id(self) -> int:
        data = db.execute(
            "SELECT COALESCE(MAX(case_id), 0) + 1 FROM modCaseData WHERE guild_id = ?",
            (self.server.id,),
        ).fetchone()
        db.commit()
        return int(data[0])

    async def create_case(
        self,
        action: str,
        target: Member | User | int | None,
        moderator: Member | User | int | None,
        reason: str | None = None,
        duration: str | None = None,
        status: str = "active",
        related_warn_id: int | None = None,
    ) -> int:
        target_id = target.id if hasattr(target, "id") else target
        moderator_id = moderator.id if hasattr(moderator, "id") else moderator
        case_id = self._next_case_id()
        date = round(datetime.now().timestamp())
        db.execute(
            """
            INSERT INTO modCaseData
                (guild_id, case_id, action, target_id, moderator_id, reason, date, duration, status, related_warn_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.server.id,
                case_id,
                str(action),
                int(target_id) if target_id is not None else None,
                int(moderator_id) if moderator_id is not None else None,
                reason or "Unspecified",
                date,
                duration,
                status,
                related_warn_id,
            ),
        )
        db.commit()
        return case_id

    def fetch_case(self, case_id: int) -> tuple | None:
        data = db.execute(
            "SELECT * FROM modCaseData WHERE guild_id = ? AND case_id = ?",
            (self.server.id, case_id),
        ).fetchone()
        db.commit()
        return data

    def fetch_cases_user(self, target: Member | User | int, limit: int = 10) -> list:
        target_id = target.id if hasattr(target, "id") else target
        data = db.execute(
            """
            SELECT * FROM modCaseData
            WHERE guild_id = ? AND target_id = ?
            ORDER BY case_id DESC
            LIMIT ?
            """,
            (self.server.id, int(target_id), limit),
        ).fetchall()
        db.commit()
        return data

    def fetch_recent_cases(self, limit: int = 10) -> list:
        data = db.execute(
            """
            SELECT * FROM modCaseData
            WHERE guild_id = ?
            ORDER BY case_id DESC
            LIMIT ?
            """,
            (self.server.id, limit),
        ).fetchall()
        db.commit()
        return data

    async def warn_user(
        self, member: Member, moderator: int, reason: str, warn_id: int, date: int
    ):
        db.execute(
            "INSERT OR IGNORE INTO warnData (guild_id, user_id, moderator_id, reason, warn_id, date) VALUES (?,?,?,?,?,?)",
            (
                self.server.id,
                member.id,
                moderator,
                reason,
                warn_id,
                date,
            ),
        )
        db.commit()

    @property
    def fetch_warnings_server(self) -> list | None:
        warnings = db.execute(
            "SELECT * FROM warnDATA WHERE guild_id = ?", (self.server.id,)
        ).fetchall()
        db.commit()
        if len(warnings) == 0 or warnings is None:
            return None
        return warnings

    def fetch_warnings_user(self, member: Member) -> list | None:
        cur = db.cursor()
        warnings = cur.execute(
            "SELECT * FROM warnDATA user WHERE user_id = ? AND guild_id = ?",
            (
                member.id,
                self.server.id,
            ),
        ).fetchall()
        db.commit()
        if len(warnings) == 0 or warnings is None:
            return None
        return warnings

    def check_warn_id(self, member: Member, warn_id: int) -> int | None:
        data = db.execute(
            "SELECT warn_id FROM warnData WHERE guild_id = ? AND user_id = ? AND warn_id = ?",
            (
                self.server.id,
                member.id,
                warn_id,
            ),
        )
        result = data.fetchone()
        db.commit()
        return int(result[0]) if result else None

    def warnpoints(self, member: Member) -> int:
        wp_query = db.execute(
            "SELECT * FROM warnData WHERE user_id = ? AND guild_id = ?",
            (
                member.id,
                self.server.id,
            ),
        ).fetchall()

        return 0 if wp_query is None else len(wp_query)

    async def revoke_warn(self, member: Member, warn_id: int):
        db.execute(
            "DELETE FROM warnData WHERE guild_id = ? AND user_id = ? AND warn_id = ?",
            (self.server.id, member.id, warn_id),
        )
        db.commit()

    def get_softban_data(self):
        data = db.execute("SELECT * FROM softbannedMembers").fetchall()
        db.commit()
        return data

    async def softban_member(self, member: Member, ends: int = None):
        if ends is None:
            ending = 99999999999  # infinite value for now
        elif isinstance(ends, (int, float)):
            ending = round((datetime.now() + timedelta(seconds=float(ends))).timestamp())
        else:
            seconds = parse_timespan(str(ends))
            ending = round((datetime.now() + timedelta(seconds=seconds)).timestamp())
        db.execute(
            "INSERT OR IGNORE INTO softbannedMembers (user_id, guild_id, ends) VALUES (?,?,?)",
            (
                member.id,
                self.server.id,
                ending,
            ),
        )
        db.commit()

    async def remove_softban(self, member: Member):
        db.execute(
            "DELETE FROM softbannedMembers WHERE user_id = ? AND guild_id = ?",
            (
                member.id,
                self.server.id,
            ),
        )
        db.commit()

    @property
    def get_modlog_channel(self) -> TextChannel | None:
        data = db.execute(
            "SELECT modlog FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return self.server.get_channel(data[0]) if data is not None else None


class Welcomer:
    def __init__(self, server: Guild) -> None:
        self.server = server

    @property
    def get_welcomer(self) -> TextChannel | None:
        data = db.execute(
            "SELECT welcoming_channel FROM serverData where server = ?",
            (self.server.id,),
        ).fetchone()
        db.commit()
        return self.server.get_channel(data[0]) if data is not None else None

    @property
    def get_leaver(self) -> TextChannel | None:
        data = db.execute(
            "SELECT leaving_channel FROM serverData where server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return self.server.get_channel(data[0]) if data is not None else None

    @property
    def get_welcoming_msg(self) -> str | None:
        data = db.execute(
            "SELECT welcoming_message FROM serverData WHERE server = ?",
            (self.server.id,),
        ).fetchone()
        db.commit()
        return data[0] if data is not None else None

    @property
    def get_leaving_msg(self) -> str | None:
        data = db.execute(
            "SELECT leaving_message FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return data[0] if data is not None else None


def get_richest(member: Member) -> int:
    try:
        result = db.execute(
            "SELECT user_id FROM bankData ORDER BY amount DESC"
        ).fetchall()
        all_ids = [m_id[0] for m_id in result]
        try:
            rank = all_ids.index(member.id) + 1
            return rank
        except Exception:
            return 20
    except Exception:
        return 20


class NsfwApis(Enum):
    GelbooruApi = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&api_key={GELBOORU_API}&user_id={GELBOORU_USER}&limit=100&tags=rating:explicit+"
    KonachanApi = "https://konachan.com/post.json?limit=100&tags=rating:explicit+"
    YandereApi = "https://yande.re/post.json?api_version=2&limit=100&tags=score:>10+rating:explicit+"
    DanbooruApi = "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit+"
    Rule34Api = f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&api_key={RULE34_API}&user_id={RULE34_USER}&limit=100&tags=rating:explicit+"


class Hentai:
    def __init__(self):
        self.api_headers = {
            "User-Agent": "Jeanne-Bot/5.4 (+https://github.com/Stacer-Varien/Jeanne-Bot)"
        }
        self.blacklisted_tags = {
            "loli",
            "shota",
            "cub",
            "gore",
            "vore",
            "flat_chest",
            "loli_nude",
            "milkshakework",
            "oppai_loli",
            "onee_loli",
            "child",
            "kodomo_doushi",
            "child_on_child",
            "small_breasts",
            "short_stack",
            "cunny",
            "lxli",
            "urine",
            "scat",
            "fart",
            "diaper",
            "diapers",
            "urination",
            "piss",
            "bestiality",
            "shit",
            "feces",
            "excrement",
            "decapitation",
            "guro",
            "beheading",
            "brain_bite",
            "pregnant",
            "pee",
            "pee_in_container",
            "piss_bottle",
            "onlyfans", #copyright reasons
            "real_life", #no real life porn allowed
            "cocomelon", #for very very obvious reasons
            "bebefinn", #for very very obvious reasons
            "baby_shark", #for very very obvious reasons
            "child_model", #for very very obvious reasons
            "commission", #copyright reasons
        }

    def _fetch_json(self, url: str):
        try:
            response = get(url, headers=self.api_headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except (RequestException, ValueError):
            return None

    def format_tags(self, tags: Optional[str] = None) -> str:
        if tags:
            tags = [
                tag.strip().replace(" ", "_")
                for tag in tags.split(",")
                if tag.strip().replace(" ", "_")
            ]
            tags_string = "+".join(tags)
            return tags_string
        else:
            return ""

    def format_cache_tags(self, tags: Optional[str] = None) -> str:
        if tags:
            tags = [
                tag.strip().replace(" ", "_")
                for tag in tags.split(",")
                if tag.strip().replace(" ", "_") and not tag.startswith("-")
            ]
            tags_string = " ".join(tags)
            return tags_string
        else:
            return ""

    def load_cache(self, tags: Optional[str] = None) -> list | None:
        cur = db.cursor()
        if tags:
            pattern = "".join([f"%{i}%" for i in self.format_cache_tags(tags).split()])
            cur.execute(
                "SELECT source, tags, file_url FROM hentaiCache WHERE lower(tags) LIKE lower(?)",
                (pattern,),
            )

        elif tags == "" or tags is None:
            cur.execute("SELECT source, tags, file_url FROM hentaiCache")

        rows = cur.fetchall()
        if not rows:
            return None
        posts = []
        for r in rows:
            posts.append({"source": str(r[0]), "tags": str(r[1]), "file_url": str(r[2])})
        return posts

    def save_cache(self, source: str, tags: str, file_url: str) -> None:
        cur = db.cursor()
        data=cur.execute(
            "INSERT OR IGNORE INTO hentaiCache (date, source, tags, file_url) VALUES (?, ?, ?, ?)",
            (datetime.now().strftime("%Y%m%d"), source, tags, file_url),
        )
        db.commit()

        if data.rowcount == 0:
            date = datetime.now().strftime("%Y%m%d")
            if int(date) == int(
                db.execute(
                    "SELECT date FROM hentaiCache WHERE source=? AND file_url = ?",
                    (source, file_url),
                ).fetchone()[0]
            ):
                pass
            db.commit()

    def _filter_blacklisted(self, tag_string: str) -> bool:
        tags = {t.lower() for t in tag_string.split() if t}
        return bool(self.blacklisted_tags.intersection(tags))

    def get_blacklisted_links(self) -> list[str] | None:
        cur = db.cursor()
        data = cur.execute("SELECT links FROM hentaiBlacklist").fetchall()
        db.commit()
        return [str(link[0]) for link in data] if data else None

    def add_blacklisted_link(self, link: str):
        cur = db.cursor()
        cur.execute("INSERT OR IGNORE INTO hentaiBlacklist (links) VALUES (?)", (link,))
        cur.execute("DELETE FROM hentaiCache WHERE file_url = ?", (link,))
        db.commit()

    def _is_allowed_post(
        self, tags_field: str, file_url: str, blacklisted_links: set[str]
    ) -> bool:
        if not tags_field or self._filter_blacklisted(tags_field.lower()):
            return False
        if not file_url or file_url in blacklisted_links:
            return False
        return True

    def get_images_rule34(self, tags: Optional[str] = None):

        blacklisted_links = set(self.get_blacklisted_links() or [])
        try:
            cache = [
                i
                for i in self.load_cache(tags)
                if i["source"] == "rule34"
                and self._is_allowed_post(
                    str(i.get("tags", "")),
                    str(i.get("file_url", "")),
                    blacklisted_links,
                )
            ]
        except Exception:
            cache = []

        post_list = cache
        if len(cache) < 100:
            tag_part = self.format_tags(tags)

            url = NsfwApis.Rule34Api.value
            if tag_part:
                url = f"{url}+{tag_part}"

            data = self._fetch_json(url)
            posts = data if isinstance(data, list) else []
            filtered = []
            for p in posts:
                tags_field = str(p.get("tags", ""))
                file_url = str(p.get("file_url", ""))

                if not self._is_allowed_post(tags_field, file_url, blacklisted_links):
                    continue

                self.save_cache("rule34", tags_field, file_url)
                filtered.append(
                    {"source": "Rule34", "tags": tags_field, "file_url": file_url}
                )
            if filtered:
                post_list = filtered

        return post_list

    def get_images_gelbooru(self, tags: Optional[str] = None):
        blacklisted_links = set(self.get_blacklisted_links() or [])
        try:
            cache = [
                i
                for i in self.load_cache(tags)
                if i["source"] == "gelbooru"
                and self._is_allowed_post(
                    str(i.get("tags", "")),
                    str(i.get("file_url", "")),
                    blacklisted_links,
                )
            ]
        except Exception:
            cache = []

        post_list = cache
        if len(cache) < 100:
            tag_part = self.format_tags(tags)

            url = NsfwApis.GelbooruApi.value
            if tag_part:
                url = f"{url}+{tag_part}"

            data = self._fetch_json(url)
            posts = data.get("post", []) if isinstance(data, dict) else []
            filtered = []
            for p in posts:
                tags_field = str(p.get("tags", ""))
                file_url = str(p.get("file_url", ""))

                if not self._is_allowed_post(tags_field, file_url, blacklisted_links):
                    continue

                self.save_cache("gelbooru", tags_field, file_url)
                filtered.append(
                    {"source": "Gelbooru", "tags": tags_field, "file_url": file_url}
                )
            if filtered:
                post_list = filtered

        return post_list

    def get_images_konachan(self, tags: Optional[str] = None):
        blacklisted_links = set(self.get_blacklisted_links() or [])
        try:
            cache = [
                i
                for i in self.load_cache(tags)
                if i["source"] == "konachan"
                and self._is_allowed_post(
                    str(i.get("tags", "")),
                    str(i.get("file_url", "")),
                    blacklisted_links,
                )
            ]
        except Exception:
            cache = []

        post_list = cache
        if len(cache) < 100:
            tag_part = self.format_tags(tags)

            url = NsfwApis.KonachanApi.value
            if tag_part:
                url = f"{url}+{tag_part}"

            data = self._fetch_json(url)
            posts = data if isinstance(data, list) else []
            filtered = []
            for p in posts:
                tags_field = str(p.get("tags", ""))
                file_url = str(p.get("file_url", ""))

                if not self._is_allowed_post(tags_field, file_url, blacklisted_links):
                    continue

                self.save_cache("konachan", tags_field, file_url)
                filtered.append(
                    {"source": "Konachan", "tags": tags_field, "file_url": file_url}
                )
            if filtered:
                post_list = filtered

        return post_list

    def get_images_yandere(self, tags: Optional[str] = None):
        blacklisted_links = set(self.get_blacklisted_links() or [])
        try:
            cache = [
                i
                for i in self.load_cache(tags)
                if i["source"] == "yandere"
                and self._is_allowed_post(
                    str(i.get("tags", "")),
                    str(i.get("file_url", "")),
                    blacklisted_links,
                )
            ]
        except Exception:
            cache = []

        post_list = cache
        if len(cache) < 100:
            tag_part = self.format_tags(tags)

            url = NsfwApis.YandereApi.value
            if tag_part:
                url = f"{url}+{tag_part}"

            data = self._fetch_json(url)
            posts = data.get("posts", []) if isinstance(data, dict) else []
            filtered = []
            for p in posts:
                tags_field = str(p.get("tags", ""))
                file_url = str(p.get("sample_url", ""))

                if not self._is_allowed_post(tags_field, file_url, blacklisted_links):
                    continue

                self.save_cache("yandere", tags_field, file_url)
                filtered.append(
                    {"source": "Yandere", "tags": tags_field, "file_url": file_url}
                )
            if filtered:
                post_list = filtered

        return post_list

    def get_images_danbooru(self, tags: Optional[str] = None):
        blacklisted_links = set(self.get_blacklisted_links() or [])
        try:
            cache = [
                i
                for i in self.load_cache(tags)
                if i["source"] == "danbooru"
                and self._is_allowed_post(
                    str(i.get("tags", "")),
                    str(i.get("file_url", "")),
                    blacklisted_links,
                )
            ]
        except Exception:
            cache = []

        post_list = cache
        if len(cache) < 100:
            tag_part = self.format_tags(tags)

            url = NsfwApis.DanbooruApi.value
            if tag_part:
                url = f"{url}+{tag_part}"

            data = self._fetch_json(url)
            posts = data if isinstance(data, list) else []
            filtered = []
            for p in posts:
                tags_field = str(p.get("tag_string", ""))
                file_url = str(p.get("file_url", ""))

                if not self._is_allowed_post(tags_field, file_url, blacklisted_links):
                    continue

                self.save_cache("danbooru", tags_field, file_url)
                filtered.append(
                    {"source": "Danbooru", "tags": tags_field, "file_url": file_url}
                )
            if filtered:
                post_list = filtered

        return post_list

    def hentai(self):
        available_posts = []
        sources = (
            ("Rule34", self.get_images_rule34),
            ("Gelbooru", self.get_images_gelbooru),
            ("Yande.re", self.get_images_yandere),
            ("Konachan", self.get_images_konachan),
            ("Danbooru", self.get_images_danbooru),
        )

        for source, fetch_posts in sources:
            try:
                posts = fetch_posts() or []
            except Exception:
                continue
            if posts:
                available_posts.append((choice(posts)["file_url"], source))

        if not available_posts:
            raise IndexError("No image sources returned a usable post")

        return choice(available_posts)


class Reminder:
    def __init__(self, user: Optional[User] = None):
        self.user = user

    async def add(self, reason: str, time: int):
        db.execute(
            "INSERT OR IGNORE INTO reminderData (userid, id, time, reason) VALUES (?,?,?,?)",
            (
                self.user.id,
                randint(1, 999999),
                time,
                reason,
            ),
        )
        db.commit()

    @property
    def get_all_reminders(self) -> list | None:
        data = db.execute("SELECT * FROM reminderData").fetchall()
        db.commit()
        return data if data else None

    @property
    def get_all_user_reminders(self) -> list | None:
        data = db.execute(
            "SELECT * FROM reminderData WHERE userid = ?", (self.user.id,)
        ).fetchall()
        db.commit()
        return data if data else None

    async def remove(self, id: int) -> Literal[False] | None:
        data = db.execute(
            "SELECT * FROM reminderData WHERE userid = ? AND id = ?",
            (
                self.user.id,
                id,
            ),
        ).fetchone()
        db.commit()
        if data is None:
            return False
        db.execute(
            "DELETE FROM reminderData WHERE userid = ? AND id = ?",
            (
                self.user.id,
                id,
            ),
        )
        db.commit()


class AutoCompleteChoices:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def command_choices(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Jeanne.Choice[str]]:
        cmds = [
            cmd.qualified_name
            for cmd in self.bot.tree.walk_commands()
            if not isinstance(cmd, Jeanne.Group)
        ]
        return [
            Jeanne.Choice(name=T(command), value=command)
            for command in cmds
            if current.lower() in command.lower()
        ][:25]

    async def disabled_commands(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Jeanne.Choice[str]]:
        commands = Command(ctx.guild).list_all_disabled
        if not commands:
            return []
        return [
            Jeanne.Choice(name=command, value=command)
            for command in commands
            if current.lower() in command.lower()
        ][:25]

    async def list_all_user_inventory(
        self, ctx: Interaction, current: str
    ) -> List[Jeanne.Choice[str]]:
        inventory = Inventory(ctx.user).get_user_inventory
        if not inventory:
            return []
        return [
            Jeanne.Choice(name=image[1], value=image[1])
            for image in inventory
            if current.lower() in str(image[1]).lower()
        ][:25]

    async def get_all_wallpapers(
        self, ctx: Interaction, current: str
    ) -> List[Jeanne.Choice[str]]:
        wallpapers = Inventory.fetch_wallpapers()
        return [
            Jeanne.Choice(name=image[0], value=image[0])
            for image in wallpapers
            if current.lower() in str(image[0]).lower()
        ][:25]

    async def default_ban_options(
        self, ctx: Interaction, current: str
    ) -> List[Jeanne.Choice[str]]:
        default_options = [
            "Suspicious or spam account",
            "Compromised or hacked account",
            "Breaking server rules",
            "Botting account",
        ]
        locale = get_command_locale(ctx)
        if locale == "fr":
            default_options = [
                "Compte suspect ou spam",
                "Compte compromis ou piraté",
                "Violation des règles du serveur",
                "Compte de botting",
            ]
        elif locale == "de":
            default_options = [
                "Verdächtiges oder Spam-Konto",
                "Kompromittiertes oder gehacktes Konto",
                "Verstoß gegen Serverregeln",
                "Bot-Konto",
            ]
        return [
            Jeanne.Choice(name=option, value=option)
            for option in default_options
            if current.lower() in option.lower()
        ]

    async def warned_users(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Jeanne.Choice[Member]]:
        user_ids = []
        warnings = Moderation(ctx.guild).fetch_warnings_server
        for warning in warnings:
            user_ids.append(warning[0])

        warned_users = [ctx.guild.get_member(int(user_id)) for user_id in user_ids]

        unique_names = set()
        choices = []

        for user in warned_users:
            if not user:
                continue

            name = user.global_name or user.name
            user_id = str(user.id)

            if name not in unique_names and current.lower() in name.lower():
                unique_names.add(name)
                choices.append(Jeanne.Choice(name=name, value=user_id))

            if len(choices) >= 25:
                break

        return choices

    async def banned_users(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Jeanne.Choice[Member]]:
        entries = [entry async for entry in ctx.guild.bans()]

        banned_users = [entry.user for entry in entries]

        choices = []

        for user in banned_users:
            name = user.name or user.global_name
            user_id = str(user.id)
            choices.append(Jeanne.Choice(name=f"{name} - {user_id}", value=user_id))

            if len(choices) >= 25:
                break

        return choices

    async def report_types(
        self, ctx: Interaction, current: str
    ) -> List[Jeanne.Choice[str]]:
        report_types = [
            "Fault",
            "Bug",
            "ToS Violator",
            "Exploit",
            "Translation Error",
            "Other",
        ]
        locale = get_command_locale(ctx)
        if locale == "fr":
            report_types = [
                "Défaillance",
                "Bogue",
                "Violation des CGU",
                "Exploitation",
                "Erreur de traduction",
                "Autre",
            ]
        elif locale == "de":
            report_types = [
                "Fehler",
                "Bug",
                "AGB-Verstoß",
                "Exploit",
                "Übersetzungsfehler",
                "Sonstiges",
            ]
        return [
            Jeanne.Choice(name=option, value=option)
            for option in report_types
            if current.lower() in option.lower()
        ]

    async def confessions(self, ctx: Interaction, current: int) -> List[Jeanne.Choice[int]]:
        confessions = await Confess(ctx.guild).get_confessions()
        if not confessions:
            return []
        return [Jeanne.Choice(name=str(c[2]), value=c[2]) for c in confessions if str(c[2]).startswith(str(current))][:25]


class Partner:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def add(user: User):
        db.execute("INSERT OR IGNORE INTO partnerData (user_id) VALUES (?)", (user.id,))
        db.commit()

    @staticmethod
    def check(user: User):
        data = db.execute(
            "SELECT * FROM partnerData WHERE user_id = ?", (user.id,)
        ).fetchone()
        db.commit()
        return data[0] if data else None

    @staticmethod
    async def remove(user: User):
        db.execute("DELETE FROM partnerData WHERE user_id = ?", (user.id,))
        db.commit()


class BetaTest:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def add(self, ctx: Context, user: User):
        server = await self.bot.fetch_guild(740584420645535775)
        betarole = server.get_role(1130430961587335219)
        try:
            m = await server.fetch_member(user.id)
            await m.add_roles(betarole, reason="Added to the Beta Programme")
            await ctx.send(f"{user} has been added as a Beta Tester")
        except Exception:
            await ctx.send(
                f"Member is not in {server}. This is required so they can be added in the Beta Programme"
            )

    async def check(self, user: User) -> bool | None:
        try:
            server = await self.bot.fetch_guild(740584420645535775)
            beta_role = server.get_role(1130430961587335219)
            try:
                member = await server.fetch_member(user.id)
                if beta_role in member.roles:
                    return True
            except Exception:
                return False
        except Exception as e:
            print(e)

    async def remove(self, ctx: Context, user: User):
        server = await self.bot.fetch_guild(740584420645535775)
        betarole = server.get_role(1130430961587335219)
        try:
            m = await server.fetch_member(user.id)
            await m.remove_roles(betarole, reason="Removed from the Beta Programme")
        except Exception:
            await ctx.send(
                f"Member is not in {server}. This is required so they can be added in the Beta Programme"
            )


async def check_disabled_app_command(ctx: Interaction):
    if Command(ctx.guild).check_disabled(ctx.command.qualified_name):
        await ctx.response.send_message(
            "This command is disabled by the server's managers", ephemeral=True
        )
        return
    module = ServerSettings.command_module(ctx.command)
    if module and ServerSettings(ctx.guild).is_module_disabled(module):
        locale = get_command_locale(ctx)
        messages = {
            "fr": "Ce module est désactivé par les gestionnaires du serveur.",
            "de": "Dieses Modul wurde von der Serververwaltung deaktiviert.",
        }
        await ctx.response.send_message(
            messages.get(locale, "This module is disabled by the server's managers."),
            ephemeral=True,
        )
        return
    return True


def check_botbanned_app_command(ctx: Interaction):
    if DevPunishment(ctx.user).check_botbanned_user:
        return
    return True


async def is_beta_app_command(ctx: Interaction):
    if not await BetaTest(ctx.client).check(ctx.user):
        await ctx.response.send_message(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )
        return
    return True


async def is_suspended(ctx: Interaction):
    if DevPunishment(ctx.user).check_suspended_module(ctx.client, ctx.command):
        return
    return True


def shorten_url(url: str) -> str | None:
    api_url = "http://tinyurl.com/api-create.php"
    params = {"url": url}
    response = get(api_url, params=params)
    if response.status_code == 200:
        short_url = response.text
        return short_url
    else:
        return None
