from datetime import datetime, timedelta
from enum import Enum
from random import choice, randint, shuffle
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
from requests import get
from config import db, BB_WEBHOOK, CATBOX_HASH
from typing import Literal, Optional, List


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
        return 0 if data == None else len(data)

    async def autopunish(self):
        points = self.warnpoints(self.user)
        db.commit()
        if points == 0:
            return
        if points == 2:
            duration = timedelta(days=7)
            await self.suspend(self.user, duration.total_seconds(), ["all"])
            return
        if points == 3:
            await self.add_botbanned_user("Recieved 3 bot warnings")
            return

    async def suspend(self, duration: int, modules: list[str]):
        duration = round((datetime.now() + timedelta(seconds=duration)).timestamp())
        data = db.execute(
            "INSERT OR IGNORE INTO suspensionData (user, modules, timeout) VALUES (?,?,?)",
            (
                self.user.id,
                ",".join(modules),
                duration,
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
                "UPDATE suspensionDATA SET modules = ? AND timeout = timeout + ? WHERE user = ?",
                ",".join(modules),
                new_timeout,
                self.user.id,
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
            name="Suspended until", value=f"<t:{timeout[0]}:F>", inline=True
        )
        embed.add_field(name="Modules", value=",".join(modules), inline=True)
        embed.set_footer(
            text="This is not a botban. The user is suspended from using certain modules of Jeanne."
        )
        embed.set_thumbnail(url=self.user.display_avatar)
        webhook = SyncWebhook.from_url(BB_WEBHOOK)
        webhook.send(embed=embed)

    async def warn(self, user: User, reason: str):
        warn_id = randint(1, 9999999)
        points = self.warnpoints(user)
        if points == 1:
            revoke_date = round((datetime.now() + timedelta(days=180)).timestamp())
        else:
            revoke_date = round((datetime.now() + timedelta(days=90)).timestamp())
        db.execute(
            "INSERT OR IGNORE INTO devWarnData (user, reason, warn_id, revoke_date) VALUES (?,?,?,?)",
            (
                user.id,
                reason,
                warn_id,
                revoke_date,
            ),
        )
        db.commit()
        embed = Embed(title="User has been Dev Warned", color=Color.yellow())
        embed.add_field(name="User", value=user, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Warn ID", value=warn_id, inline=True)
        embed.add_field(name="Points", value=self.warnpoints(user))
        embed.set_thumbnail(url=user.display_avatar)
        webhook = SyncWebhook.from_url(BB_WEBHOOK)
        webhook.send(embed=embed)
        await self.autopunish(user)

    def check_suspended_user(self, module: str):
        data = db.execute(
            "SELECT * FROM suspensionDATA WHERE user = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return (
            True
            if (self.user.id == int(data[0])) and (module in str(data[1]))
            else False
        )


class Currency:
    def __init__(self, user: User):
        self.user = user

    @property
    def get_balance(self) -> int:
        data = db.execute(
            "SELECT amount FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return 0 if data == None else data[0]

    async def add_qp(self, amount: int):
        previous_day = round((datetime.now() - timedelta(days=1)).timestamp())
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (
                self.user.id,
                amount,
                previous_day,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET amount = amount + ? WHERE user_id = ?",
                (
                    amount,
                    self.user.id,
                ),
            )
            db.commit()

    async def remove_qp(self, amount: int):
        db.execute(
            "UPDATE bankData SET amount = amount - ? WHERE user_id = ?",
            (
                amount,
                self.user.id,
            ),
        )
        db.commit()

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

    @property
    def check_daily(self) -> int | Literal[True]:
        data = db.execute(
            "SELECT claimed_date FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        if (data == None) or (int(data[0]) < round(datetime.now().timestamp())):
            return True
        return int(data[0])


class Inventory:
    def __init__(self, user: Optional[User] = None) -> None:
        self.user = user

    @staticmethod
    async def upload_to_catbox(image_url: str) -> str:
        async with aiohttp.ClientSession() as session:
            url = "https://catbox.moe/user/api.php"
            userhash = CATBOX_HASH
            data = {"reqtype": "urlupload", "userhash": userhash, "url": image_url}
            response = await session.post(url, data=data)
        if response.status == 200:
            return response.content
        else:
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
        return None if data == None else data[0]

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
        if wallpaper == None:
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

    async def add_user_custom_wallpaper(self, name: str, url: str):
        await self.deselect_wallpaper()
        db.execute(
            "INSERT OR IGNORE INTO userWallpaperInventory (user_id, wallpaper, link, brightness, selected) VALUES (?,?,?,?,?)",
            (
                self.user.id,
                name,
                url,
                100,
                1,
            ),
        )
        db.commit()
        await Currency(self.user).remove_qp(1500)

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
        return None if (wallpaper == None) else str(wallpaper[0])

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
        return 100 if (data == None) else int(data[0])

    async def set_brightness(self, brightness: int) -> Literal[False] | None:
        try:
            db.execute(
                "UPDATE userWallpaperInventory SET brightness = ? WHERE user_id = ? AND selected = ?",
                (
                    brightness,
                    self.user.id,
                    1,
                ),
            )
            db.commit()
        except:
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
        db.commit()
        return 0 if xp is None else int(xp[0])

    @property
    def get_user_xp(self) -> int:
        xp = db.execute(
            "SELECT exp FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()
        return 0 if xp is None else int(xp[0])

    @property
    def get_member_cumulated_xp(self) -> int:
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (self.member.id, self.server.id),
        ).fetchone()
        db.commit()
        return 0 if cumulated_exp is None else int(cumulated_exp[0])

    @property
    def get_user_cumulated_xp(self) -> int:
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM globalxpData WHERE user_id = ?",
            (self.member.id,),
        ).fetchone()
        db.commit()
        return 0 if cumulated_exp is None else int(cumulated_exp[0])

    @property
    def get_next_time_server(self) -> int:
        next_time = db.execute(
            "SELECT next_time FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (self.member.id, self.server.id),
        ).fetchone()
        db.commit()
        return int(next_time[0]) if next_time is not None else 0

    @property
    def get_next_time_global(self) -> int:
        next_time = db.execute(
            "SELECT next_time FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()
        return int(next_time[0]) if next_time is not None else 0

    @property
    def get_member_level(self) -> int:
        level = db.execute(
            "SELECT lvl FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (self.member.id, self.server.id),
        ).fetchone()
        db.commit()
        return int(level[0]) if level else 0

    @property
    def get_user_level(self) -> int:
        level = db.execute(
            "SELECT lvl FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()
        return int(level[0]) if level is not None else 0

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
                db.commit()

                global_level = self.get_user_level
                global_next_lvl_exp = (
                    (global_level * 50) + ((global_level - 1) * 25) + 50
                )
                if global_updated_exp >= global_next_lvl_exp:
                    db.execute(
                        "UPDATE globalxpData SET lvl = lvl + ?, exp = ? WHERE user_id = ?",
                        (1, 0, self.member.id),
                    )
                    db.commit()

        server_cursor = db.execute(
            "INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, next_time) VALUES (?, ?, ?, ?, ?)",
            (self.server.id, self.member.id, 0, xp, next_time),
        )
        db.commit()

        if server_cursor.rowcount == 0:
            if now_time > self.get_next_time_server:
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
                db.commit()

                server_level = self.get_member_level
                server_next_lvl_exp = (
                    (server_level * 50) + ((server_level - 1) * 25) + 50
                )
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
                    db.commit()
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
        return None if data is None else data[0]

    @property
    def get_levelup_channel(self) -> Optional[TextChannel]:
        data = db.execute(
            "SELECT levelup_channel FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        return None if data is None else self.server.get_channel(data[0])

    @property
    def get_rank_up_update(self) -> Optional[str]:
        data = db.execute(
            "SELECT rankup_message FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        return None if data is None else data[0]

    @property
    def get_role_reward(self) -> Optional[Role]:
        data = db.execute(
            "SELECT role FROM levelRewardData WHERE server = ? AND level = ?",
            (self.server.id, self.get_member_level),
        ).fetchone()
        return None if data is None else self.server.get_role(data[0])

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
        if data == None:
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
                f"UPDATE serverData SET welcoming_channel = ? WHERE server = ?",
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
                f"UPDATE serverData SET leaving_channel = ? WHERE server = ?",
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
                f"UPDATE serverData SET modlog = ? WHERE server = ?",
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
        db.execute(
            "UPDATE serverData SET confess_channel = ? WHERE server = ?",
            (
                channel.id,
                self.server.id,
            ),
        )
        db.commit()

    @property
    def get_confession_channel(self) -> TextChannel | None:
        data = db.execute(
            "SELECT confess_channel FROM serverData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return None if data == None else self.server.get_channel(data[0])


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
        except:
            pass

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
        if len(warnings) == 0 or warnings == None:
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
        if len(warnings) == 0 or warnings == None:
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
        db.execute("DELETE FROM warnData WHERE warn_id = ?", (warn_id,))
        db.commit()

    def get_softban_data(self):
        data = db.execute("SELECT * FROM softbannedMembers").fetchall()
        db.commit()
        return data

    async def softban_member(self, member: Member, ends: int = None):
        if ends == None:
            ends = 99999999999  # infinite value for now
        else:
            seconds = parse_timespan(ends)
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
        return self.server.get_channel(data[0]) if data != None else None


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


def get_cached_users() -> int:
    data = db.execute("SELECT * FROM globalxpData").fetchall()
    return len(data)


def get_true_members() -> int:
    data = db.execute("SELECT * FROM bankData").fetchall()
    return len(data)


def get_richest(member: Member) -> int:
    try:
        result = db.execute(
            "SELECT user_id FROM bankData ORDER BY amount DESC"
        ).fetchall()
        all_ids = [m_id[0] for m_id in result]
        try:
            rank = all_ids.index(member.id) + 1
            return rank
        except:
            return 20
    except:
        return 20


class NsfwApis(Enum):
    KonachanApi = "https://konachan.com/post.json?s=post&q=index&limit=100&tags=score:>10+rating:explicit+"
    YandereApi = "https://yande.re/post.json?limit=100&tags=score:>10+rating:explicit+"
    GelbooruApi = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=score:>10+rating:explicit+"
    DanbooruApi = (
        "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit+"
    )


class Hentai:
    def __init__(self, plus: Optional[bool] = None):
        self.plus = plus
        self.blacklisted_tags = [
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
        ]

    def format_tags(self, tags: str = None) -> str:
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

    async def get_nsfw_image(self, provider: NsfwApis, tags: str = None) -> list | None:
        bl = self.get_blacklisted_links()
        tags = tags.lower() if tags else None
        url = provider.value + self.format_tags(tags)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                nsfw_images: dict = await resp.json()
        if not nsfw_images:
            return None
        if provider.value == provider.GelbooruApi.value:
            nsfw_images_list = list(nsfw_images.get("post", []))
        else:
            nsfw_images_list = list(nsfw_images)
        shuffle(nsfw_images_list)
        if (not tags) or (tags == None):
            tags = ""
        tags_list = [
            tag.strip().replace(" ", "_")
            for tag in tags.split(",")
            if tag.strip().replace(" ", "_") not in self.blacklisted_tags
        ]
        if len(tags_list) == 0 or len(tags_list) > 3:
            return None
        filtered_images = []
        for image in nsfw_images_list:
            if provider.value == provider.DanbooruApi.value:
                img_tags = str(image["tag_string"]).lower().split(" ")
            else:
                img_tags = str(image["tags"]).lower().split(" ")
            try:
                urls = str(image["file_url"])
            except:
                continue
            if any(tag in self.blacklisted_tags for tag in img_tags):
                continue
            if any(url in bl for url in urls):
                continue
            filtered_images.append(image)
        return filtered_images

    async def add_blacklisted_link(self, link: str):
        db.execute("INSERT OR IGNORE INTO hentaiBlacklist (links) VALUES (?)", (link,))
        db.commit()

    def get_blacklisted_links(self) -> list[str] | None:
        data = db.execute("SELECT links FROM hentaiBlacklist").fetchall()
        db.commit()
        return [str(link[0]) for link in data] if data else None

    async def gelbooru(self, tag: Optional[str] = None):

        if not tag or tag is None:
            tag = None
        images = await self.get_nsfw_image(NsfwApis.GelbooruApi, tag)
        if self.plus:
            return images
        return choice(images)["file_url"]

    async def yandere(self, tag: Optional[str] = None):
        images = await self.get_nsfw_image(NsfwApis.YandereApi, tag)
        if self.plus:
            return images
        return choice(images)["sample_url"]

    async def konachan(self, tag: Optional[str] = None):

        images = await self.get_nsfw_image(NsfwApis.KonachanApi, tag)
        if self.plus:
            return images
        return choice(images)["file_url"]

    async def danbooru(self, tag: Optional[str] = None):

        if not tag or tag is None:
            tag = None
        else:
            tag = ",".join(tag.split(",")[:2])
        images = await self.get_nsfw_image(NsfwApis.DanbooruApi, tag)
        if self.plus:
            return images
        return choice(images)["file_url"]

    async def hentai(self, rating: Optional[str] = None):
        gelbooru_image = await self.gelbooru()
        yandere_image = await self.yandere()
        konachan_image = await self.konachan()
        danbooru_image = await self.danbooru()
        h = [gelbooru_image, yandere_image, konachan_image, danbooru_image]
        hentai: str = choice(h)
        if hentai == gelbooru_image:
            return hentai, "Gelbooru"
        if hentai == yandere_image:
            return hentai, "Yande.re"
        if hentai == konachan_image:
            return hentai, "Konachan"
        if hentai == danbooru_image:
            return hentai, "Danbooru"


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
        if data == None:
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
            Jeanne.Choice(name=command, value=command)
            for command in cmds
            if current.lower() in command.lower()
        ][:25]

    async def disabled_commands(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Jeanne.Choice[str]]:
        commands = Command(ctx.guild).list_all_disabled
        return [
            Jeanne.Choice(name=command, value=command)
            for command in commands
            if current.lower() in command
        ][:25]

    async def list_all_user_inventory(
        self, ctx: Interaction, current: str
    ) -> List[Jeanne.Choice[str]]:
        inventory = Inventory(ctx.user).get_user_inventory
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
        entries=[entry async for entry in ctx.guild.bans()]

        banned_users = [entry.user for entry in entries]

        choices = []

        for user in banned_users:
                name=user.name or user.global_name
                user_id=str(user.id)
                choices.append(Jeanne.Choice(name=f"{name} - {user_id}", value=user_id))

                if len(choices) >= 25:
                    break

        return choices


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
        except:
            await ctx.send(
                f"Member is not in {server}. This is required so they can be added in the Beta Programme"
            )

    async def check(self, user: User) -> bool | None:
        server = await self.bot.fetch_guild(740584420645535775)
        beta_role = server.get_role(1130430961587335219)
        try:
            member = await server.fetch_member(user.id)
            if beta_role in member.roles:
                return True
        except:
            return False

    async def remove(self, ctx: Context, user: User):
        server = await self.bot.fetch_guild(740584420645535775)
        betarole = server.get_role(1130430961587335219)
        try:
            m = await server.fetch_member(user.id)
            await m.remove_roles(betarole, reason="Removed from the Beta Programme")
        except:
            await ctx.send(
                f"Member is not in {server}. This is required so they can be added in the Beta Programme"
            )


async def check_disabled_app_command(ctx: Interaction):
    if Command(ctx.guild).check_disabled(ctx.command.qualified_name):
        await ctx.response.send_message(
            "This command is disabled by the server's managers", ephemeral=True
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
    if DevPunishment(ctx.user).check_suspended_user(ctx.command):
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
