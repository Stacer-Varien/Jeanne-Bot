from datetime import date, datetime, timedelta
from enum import Enum
from random import choice, randint, shuffle
import time
import aiohttp
from humanfriendly import parse_timespan
from discord import (
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
from discord.ext.commands import Bot
from requests import get
from config import db, BB_WEBHOOK
from typing import Optional, List

current_time = date.today()


class Botban:
    def __init__(self, user: User):
        self.user = user

    @property
    def check_botbanned_user(self):
        botbanned_data = db.execute(
            "SELECT * FROM botbannedData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        return botbanned_data is not None and self.user.id == botbanned_data[0]

    def add_botbanned_user(self, reason: str):
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
            description="They will no longer use Jeanne,permanently!",
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


class Currency:
    def __init__(self, user: User):
        self.user = user

    @property
    def get_balance(self) -> int:
        data = db.execute(
            "SELECT amount FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        return data[0] if data is not None else 0

    def add_qp(self, amount: int):
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (
                self.user.id,
                amount,
                (current_time - timedelta(days=1)),
            ),
        )

        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET amount = amount + ? WHERE user_id = ?",
                (
                    amount,
                    self.user.id,
                ),
            )

        db.commit()

    def remove_qp(self, amount: int):
        db.execute(
            "UPDATE bankData SET amount = amount - ? WHERE user_id = ?",
            (
                amount,
                self.user.id,
            ),
        )

        db.commit()

    def give_daily(self):
        current_time = datetime.now()
        next_claim = current_time + timedelta(days=1)
        data = db.execute(
            "SELECT * FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        qp = 200 if datetime.today().weekday() >= 5 else 100

        if data == None:
            cur = db.execute(
                "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
                (
                    self.user.id,
                    qp,
                    round(next_claim.timestamp()),
                ),
            )
            db.commit()
            if cur.rowcount == 0:
                db.execute(
                    "UPDATE bankData SET claimed_date = ?, amount = amount + ? WHERE user_id = ?",
                    (
                        round(next_claim.timestamp()),
                        qp,
                        self.user.id,
                    ),
                )
                db.commit()
            return True

        if data[2] < round(current_time.timestamp()):
            db.execute(
                "UPDATE bankData SET claimed_date = ?, amount = amount + ? WHERE user_id = ?",
                (
                    round(next_claim.timestamp()),
                    qp,
                    self.user.id,
                ),
            )
            db.commit()
            return True
        return False

    def get_next_daily(self):
        data = db.execute(
            "SELECT claimed_date FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        return data[0] if data else None


class Inventory:
    def __init__(self, user: Optional[User] = None) -> None:
        self.user = user

    @staticmethod
    def fetch_wallpapers() -> list:
        data = db.execute("SELECT * FROM wallpapers").fetchall()

        db.commit()
        return data

    @staticmethod
    def get_wallpaper(name: str):
        wallpaper = db.execute(
            "SELECT * FROM wallpapers WHERE name = ?", (name,)
        ).fetchone()
        db.commit()
        return str(wallpaper[1]), str(wallpaper[2]), str(wallpaper[3])

    def deselect_wallpaper(self):
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

    def add_user_wallpaper(self, name: str):
        self.deselect_wallpaper()

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

        Currency(self.user).remove_qp(1000)

    def add_user_custom_wallpaper(self, name: str, link: str):
        self.deselect_wallpaper()

        db.execute(
            "INSERT OR IGNORE INTO userWallpaperInventory (user_id, wallpaper, link, brightness, selected) VALUES (?,?,?,?,?)",
            (
                self.user.id,
                name,
                link,
                100,
                1,
            ),
        )
        db.commit()

        Currency(self.user).remove_qp(1000)

    def selected_wallpaper(self):
        wallpaper = db.execute(
            "SELECT * FROM userWallpaperInventory WHERE user_id = ? and selected = ?",
            (
                self.user.id,
                1,
            ),
        ).fetchone()
        db.commit()
        return (
            str(wallpaper[1]),
            str(wallpaper[2]),
            int(wallpaper[3]),
            int(wallpaper[4])
        )

    def use_wallpaper(self, name: str):
        if self.deselect_wallpaper() == None:
            db.execute(
                "UPDATE userWallpaperInventory SET selected = ? WHERE wallpaper = ? AND user_id = ?",
                (
                    1,
                    name,
                    self.user.id,
                ),
            )
            db.commit()
            return
        
        self.deselect_wallpaper()
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
    def fetch_user_inventory(self) -> list | None:
        wallpapers = db.execute(
            "SELECT * FROM userWallpaperInventory WHERE user_id = ?", (self.user.id,)
        ).fetchall()

        return wallpapers if wallpapers else None

    def set_brightness(self, brightness: int):
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

    def set_bio(self, bio: str):
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

    def set_color(self, color: str):
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
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()
        return int(xp[0]) if xp else 0

    @property
    def get_user_xp(self) -> int:
        xp = db.execute(
            "SELECT exp FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()
        return int(xp[0]) if xp else 0

    @property
    def get_member_cumulated_xp(self) -> int:
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()
        return int(cumulated_exp[0]) if cumulated_exp else 0

    @property
    def get_user_cumulated_xp(self)->int:
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM globalxpData WHERE user_id = ?",
            (self.member.id,),
        ).fetchone()
        db.commit()
        return int(cumulated_exp[0]) if cumulated_exp else 0

    @property
    def get_next_time_server(self) -> int:
        next_time = db.execute(
            "SELECT next_time FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()

        return next_time[0] if next_time else round(datetime.now().timestamp)

    @property
    def get_next_time_global(self) -> int:
        next_time = db.execute(
            "SELECT next_time FROM globalxpData WHERE user_id = ?",
            (self.member.id,),
        ).fetchone()
        db.commit()
        return next_time[0] if next_time else round(datetime.now().timestamp)

    @property
    def get_member_level(self) -> int:
        level = db.execute(
            "SELECT lvl FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()
        return level[0] if level else 0

    @property
    def get_user_level(self) -> int:
        level = db.execute(
            "SELECT lvl FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()
        return level[0] if level else 0

    def add_xp(self):
        now_time = round(datetime.now().timestamp())
        next_time = round((datetime.now() + timedelta(minutes=2)).timestamp())
        if datetime.today().weekday() > 4:
            xp = 10
        else:
            xp = 5
        cursor1 = db.execute(
            "INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, cumulative_exp, next_time) VALUES (?,?,?,?,?,?)",
            (
                self.server.id,
                self.member.id,
                0,
                xp,
                xp,
                next_time,
            ),
        )
        db.commit()

        cursor2 = db.execute(
            "INSERT OR IGNORE INTO globalxpData (user_id, lvl, exp, cumulative_exp, next_time) VALUES (?,?,?,?,?)",
            (
                self.member.id,
                0,
                xp,
                xp,
                next_time,
            ),
        )
        db.commit()

        if cursor1.rowcount == 0 and now_time >= self.get_next_time_server:
            server_exp = self.get_member_xp
            cumulated_exp = self.get_member_cumulated_xp

            server_updated_exp = server_exp + xp
            server_updated_cumulative_exp = cumulated_exp + xp

            db.execute(
                "UPDATE serverxpData SET exp = ?, cumulative_exp = ?, next_time = ? WHERE guild_id = ? AND user_id = ?",
                (
                    server_updated_exp,
                    server_updated_cumulative_exp,
                    next_time,
                    self.server.id,
                    self.member.id,
                ),
            )

            db.commit()

        if cursor2.rowcount == 0 and now_time >= self.get_next_time_global:
            global_exp = self.get_user_xp
            global_cumulated_exp = self.get_user_cumulated_xp

            global_updated_exp = global_exp + xp
            global_updated_cumulated_exp = global_cumulated_exp + xp

            db.execute(
                "UPDATE globalxpDATA SET exp = ?, cumulative_exp = ?, next_time = ? WHERE user_id = ?",
                (
                    global_updated_exp,
                    global_updated_cumulated_exp,
                    next_time,
                    self.member.id,
                ),
            )

            db.commit()

        global_cumulated_exp = self.get_user_cumulated_xp
        global_level = self.get_user_level
        global_next_lvl_exp = (global_level * 50) + ((global_level - 1) * 25) + 50

        if global_cumulated_exp >= global_next_lvl_exp:
            global_updated_exp = global_cumulated_exp - global_next_lvl_exp
            db.execute(
                "UPDATE globalxpData SET lvl = lvl + ?, exp = ? WHERE user_id = ?",
                (
                    1,
                    global_updated_exp,
                    self.member.id,
                ),
            )
            db.commit()

        server_cumulated_exp = self.get_member_cumulated_xp
        server_level = self.get_member_level
        server_next_lvl_exp = (server_level * 50) + ((server_level - 1) * 25) + 50

        if server_cumulated_exp >= server_next_lvl_exp:
            server_updated_exp = server_cumulated_exp - server_next_lvl_exp
            db.execute(
                "UPDATE serverxpData SET lvl = lvl + ?, exp = ? WHERE guild_id = ? AND user_id = ?",
                (
                    1,
                    server_updated_exp,
                    self.server.id,
                    self.member.id,
                ),
            )
            db.commit()

            return self.get_level_channel()

    def get_level_channel(self):
        data = db.execute(
            "SELECT * FROM levelNotifierData WHERE server_id = ?", (self.server.id,)
        ).fetchone()
        db.commit()

        return data if data else None

    async def get_role_reward(self):
        data = db.execute(
            "SELECT * FROM levelRewardData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()
        if data == None:
            return
        if self.get_member_level() == int(data[2]):
            role = self.server.get_role(int(data[1]))
            await self.member.add_roles(role)
            return ""  # still working on that

    def get_server_rank(self):
        leaders_query = db.execute(
            "SELECT user_id FROM serverxpData WHERE guild_id = ? ORDER BY lvl DESC LIMIT 15;",
            (self.server.id,),
        )
        db.commit()
        return leaders_query.fetchall()

    def get_global_rank(self):
        leaders_query = db.execute(
            "SELECT * FROM globalxpData ORDER BY lvl DESC LIMIT 15;"
        )
        db.commit()
        return leaders_query.fetchall()

    def check_xpblacklist_channel(self, channel: TextChannel):
        data = db.execute(
            "SELECT * FROM xpChannelData WHERE server = ? AND channel = ?",
            (
                self.server.id,
                channel.id,
            ),
        ).fetchone()
        db.commit()
        return data if data else None


    def get_member_server_rank(self):
        result = db.execute(
            "SELECT user_id FROM serverxpData WHERE guild_id = ? ORDER BY cumulative_exp DESC",
            (self.member.guild.id,),
        ).fetchall()
        all_ids = [m_id[0] for m_id in result]
        try:
            rank = all_ids.index(self.member.id) + 1
            return rank
        except ValueError:
            return None

    def get_member_global_rank(self):
        result = db.execute(
            "SELECT user_id FROM globalxpData ORDER BY cumulative_exp DESC"
        ).fetchall()
        all_ids = [m_id[0] for m_id in result]

        try:
            rank = all_ids.index(self.member.id) + 1
            return rank
        except ValueError:
            return None

    @property
    def get_blacklisted_channels(self) -> list[int] | None:
        data = db.execute(
            "SELECT channel FROM xpChannelData WHERE server = ?", (self.server.id,)
        ).fetchall()
        db.commit()

        return [int(i[0]) for i in data] if data else None

    @property
    def list_all_roles(self) -> list:
        data = db.execute(
            "SELECT * FROM levelRewardData WHERE server = ?ORDER BY level ASC",
            (self.server.id,),
        ).fetchall()
        db.commit()

        return [i for i in data] if data else None


class Manage:
    def __init__(self, server: Guild) -> None:
        self.server = server

    def remove_blacklist(self, channel: TextChannel):
        db.execute(
            "DELETE FROM xpChannelData WHERE server = ? AND channel = ?",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

    def add_level_channel(
        self, channel: TextChannel, message: Optional[str] = None
    ) -> None:
        message = message if message else 0

        cur = db.execute(
            "INSERT OR IGNORE INTO levelNotifierData (server_id, channel_id, message) VALUES (?,?,?)",
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
                    "UPDATE levelNotifierData SET channel_id = ? WHERE server_id =?",
                    (
                        channel.id,
                        self.server.id,
                    ),
                )
                db.commit()
            if message:
                db.execute(
                    "UPDATE levelNotifierData SET message = ? WHERE server_id =?",
                    (
                        message,
                        self.server.id,
                    ),
                )
                db.commit()

    def add_xpblacklist(self, channel: TextChannel):
        db.execute(
            "INSERT OR IGNORE INTO xpChannelData (server, channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

    def add_role_reward(self, role: Role, level: int):
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

    def remove_role_reward(self, role: Role):
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

    def set_welcomer_msg(self, json_script: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO welcomerMsgData (server, welcoming, leaving) VALUES (?,?,?)",
            (
                self.server.id,
                json_script,
                0,
            ),
        )
        db.commit()

        if cur.rowcount == 0:
            db.execute(
                "UPDATE welcomerMsgData SET welcoming = ? WHERE server = ?",
                (
                    json_script,
                    self.server.id,
                ),
            )
            db.commit()

    def set_leaving_msg(self, json_script: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO welcomerMsgData (server, welcoming, leaving) VALUES (?,?,?)",
            (
                self.server.id,
                0,
                json_script,
            ),
        )
        db.commit()

        if cur.rowcount == 0:
            db.execute(
                "UPDATE welcomerMsgData SET leaving = ? WHERE server = ?",
                (
                    json_script,
                    self.server.id,
                ),
            )
            db.commit()

    def set_message_logger(self, channel: TextChannel):
        cur = db.execute(
            "INSERT OR IGNORE INTO messageLogData (server, channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

        if cur.rowcount == 0:
            db.execute(
                "UPDATE messageLogData SET channel = ? WHERE server = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
        db.commit()

    def set_welcomer(self, channel:TextChannel):
        cursor = db.execute(
            "INSERT OR IGNORE INTO welcomerData (guild_id, channel_id) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()
        if cursor.rowcount == 0:
            db.execute(
                f"UPDATE welcomerData SET channel_id = ? WHERE guild_id = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
            db.commit()

    def set_leaver(self, channel:TextChannel):
        cursor = db.execute(
            "INSERT OR IGNORE INTO leaverData (guild_id, channel_id) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()
        if cursor.rowcount == 0:
            db.execute(
                f"UPDATE leaverData SET channel_id = ? WHERE guild_id = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
        db.commit()

    def set_modloger(self, channel: TextChannel):
        cursor = db.execute(
            "INSERT OR IGNORE INTO modlogData (guild_id, channel_id) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

        if cursor.rowcount == 0:
            db.execute(
                f"UPDATE modlogData SET channel_id = ? WHERE guild_id = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
            db.commit()

    def remove_welcomer(self):
        db.execute("DELETE FROM welcomerData WHERE guild_id = ?", (self.server.id,))
        db.commit()

    def remove_leaver(self):
        db.execute("DELETE FROM leaverData WHERE guild_id = ?", (self.server.id,))
        db.commit()

    def remove_modloger(self):
        db.execute("DELETE FROM modlogData WHERE guild_id = ?", (self.server.id,))
        db.commit()

    def remove_levelup(self):
        db.execute(
            "DELETE FROM levelNotifierData WHERE server_id = ?", (self.server.id,)
        )

        db.commit()

    def remove_welcomemsg(self):
        db.execute(
            "UPDATE welcomerMsgData SET welcoming = ? WHERE server = ?",
            (
                0,
                self.server.id,
            ),
        )
        db.commit()

    def remove_leavingmsg(self):
        db.execute(
            "UPDATE welcomerMsgData SET leaving = ? WHERE server = ?",
            (
                0,
                self.server.id,
            ),
        )
        db.commit()

    def remove_messagelog(self):
        db.execute("DELETE FROM messageLogData WHERE server = ?", (self.server.id,))
        db.commit()


class Command:
    def __init__(self, server: Guild) -> None:
        self.server = server

    def check_disabled(self, command: str):
        data = db.execute(
            "SELECT command FROM disabledCommandsData WHERE server = ? AND command = ?",
            (
                self.server.id,
                command,
            ),
        ).fetchone()
        db.commit()

        return str(data[0]) if data else None

    def disable(self, command: str):
        db.execute(
            "INSERT OR IGNORE INTO disabledCommandsData (server, command) VALUES (?,?)",
            (
                self.server.id,
                command,
            ),
        )
        db.commit()

    def enable(self, command: str):
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
    def __init__(
        self, server: Optional[Guild] = None, member: Optional[Member] = None
    ) -> None:
        self.server = server
        self.member = member

    def warn_user(self, moderator: int, reason: str, warn_id: int, date: int):
        db.execute(
            "INSERT OR IGNORE INTO warnData (guild_id, user_id, moderator_id, reason, warn_id, date) VALUES (?,?,?,?,?,?)",
            (
                self.server.id,
                self.member.id,
                moderator,
                reason,
                warn_id,
                date,
            ),
        )
        db.commit()

        cur = db.execute(
            "INSERT OR IGNORE INTO warnDatav2 (guild_id, user_id, warn_points) VALUES (?,?,?)",
            (self.server.id, self.member.id, 1),
        )
        db.commit()

        if cur.rowcount == 0:
            db.execute(
                "UPDATE warnDatav2 SET warn_points = warn_points + ? WHERE guild_id = ? and user_id = ?",
                (1, self.server.id, self.member.id),
            )
            db.commit()

    def fetch_warnings_server(self):
        cur = db.cursor()
        warnings = cur.execute(
            "SELECT * FROM warnDATAv2 WHERE guild_id = ?", (self.server.id,)
        ).fetchall()
        db.commit()
        if len(warnings) == 0 or warnings == None:
            return None

        return warnings

    def fetch_warnings_user(self):
        cur = db.cursor()
        warnings = cur.execute(
            "SELECT * FROM warnDATA user WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchall()
        db.commit()

        if len(warnings) == 0 or warnings == None:
            return None

        return warnings

    def check_warn_id(self, warn_id: int):
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM warnData WHERE guild_id = ? AND warn_id = ?",
            (
                self.server.id,
                warn_id,
            ),
        )
        result = cur.fetchone()
        db.commit()

        return result if result else None

    def revoke_warn(self, warn_id: int):
        cur = db.cursor()
        cur.execute("DELETE FROM warnData WHERE warn_id = ?", (warn_id,))
        db.commit()

        cur.execute(
            "UPDATE warnDatav2 SET warn_points = warn_points - ? WHERE user_id = ? AND guild_id = ?",
            (
                1,
                self.member.id,
                self.server.id,
            ),
        )
        db.commit()

        wp_query = cur.execute(
            f"SELECT warn_points FROM warnDatav2 WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        )
        warnpoints = wp_query.fetchone()[0]
        db.commit()

        if warnpoints == 0:
            cur.execute(
                f"DELETE FROM warnDatav2 WHERE user_id = ? AND guild_id = ?",
                (
                    self.member.id,
                    self.server.id,
                ),
            )

            db.commit()

    def get_softban_data(self):
        data = db.execute("SELECT * FROM softbannedMembers").fetchall()
        db.commit()
        return data

    def softban_member(self, ends: str = None):
        if ends == None:
            ends = 99999999999  # infinite value for now
        else:
            seconds = parse_timespan(ends)
            ends = round((datetime.now() + timedelta(seconds=seconds)).timestamp())

        db.execute(
            "INSERT OR IGNORE INTO softbannedMembers (user_id, guild_id, ends) VALUES (?,?,?)",
            (
                self.member.id,
                self.server.id,
                ends,
            ),
        )

        db.commit()

    def remove_softban(self):
        db.execute(
            "DELETE FROM softbannedMembers WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        )
        db.commit()


class Logger:
    def __init__(self, server: Optional[Guild] = None) -> None:
        self.server = server

    def get_modlog_channel(self):
        data = db.execute(
            "SELECT channel_id FROM modlogData WHERE guild_id = ?", (self.server.id,)
        ).fetchone()
        db.commit()

        return data[0] if data else None

    def get_message_logger(self):
        channel = db.execute(
            "SELECT channel FROM messageLogData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return channel[0] if channel else None


class Welcomer:
    def __init__(self, server: Guild) -> None:
        self.server = server

    def get_welcomer(self):
        data = db.execute(
            "SELECT * FROM welcomerData where guild_id = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return data if data else None

    def get_leaver(self):
        data = db.execute(
            "SELECT * FROM leaverData where guild_id = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return data if data else None

    def get_welcoming_msg(self):
        data = db.execute(
            "SELECT welcoming FROM welcomerMsgData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return data[0] if data else None

    def get_leaving_msg(self):
        data = db.execute(
            "SELECT leaving FROM welcomerMsgData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        return data[0] if data else None


def get_cached_users():
    data = db.execute("SELECT * FROM globalxpData").fetchall()
    return len(data)


def get_true_members():
    data = db.execute("SELECT * FROM bankData").fetchall()
    return len(data)


def get_richest(member: Member):
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
    KonachanApi = (
        "https://konachan.com/post.json?s=post&q=index&limit=100&tags=score:>10+rating:"
    )
    YandereApi = "https://yande.re/post.json?limit=100&tags=score:>10+rating:"
    GelbooruApi = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=score:>10+rating:"


class Hentai:
    def __init__(self, plus: Optional[bool] = None):
        self.plus = plus
        self.blacklisted_tags = {"loli", "shota", "cub", "gore", "vore"}

    def format_tags(self, tags: str = None):
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

    def remove_data_from_json_list(
        self, json_list: List[dict], key_to_check: str, values_to_remove: List[str]
    ):
        try:
            data_list = [
                item
                for item in json_list
                if item.get(key_to_check) not in values_to_remove
            ]
            return data_list
        except Exception as e:
            print(f"Error in remove_data_from_json_list: {e}")
            return None

    async def get_nsfw_image(
        self, provider: NsfwApis, rating: Optional[str] = None, tags: str = None
    ):
        bl = self.get_blacklisted_links()
        tags = tags.lower() if tags else None

        url = provider.value + rating + "+" + self.format_tags(tags)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                nsfw_images = await resp.json()

        if not nsfw_images:
            return None

        if provider.value == provider.GelbooruApi.value:
            nsfw_images_list = list(nsfw_images.get("post", []))
        else:
            nsfw_images_list = list(nsfw_images)

        shuffle(nsfw_images_list)

        if not tags:
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
            tags = image["tags"].lower().split(" ")
            urls = image["file_url"]
            if any(tag in self.blacklisted_tags for tag in tags):
                continue
            if any(url in set(bl) for url in urls):
                continue
            filtered_images.append(image)
        return filtered_images

    def add_blacklisted_link(self, link: str):
        db.execute("INSERT OR IGNORE INTO hentaiBlacklist (links) VALUES (?)", (link,))
        db.commit()

    def get_blacklisted_links(self) -> List[str]:
        data = db.execute("SELECT links FROM hentaiBlacklist").fetchall()
        db.commit()
        return [link[0] for link in data]

    async def gelbooru(
        self, rating: Optional[str] = None, tag: Optional[str] = None
    ) -> Optional[str]:
        if rating is None:
            rating = choice(["questionable", "explicit"])
        if not tag or tag is None:
            tag = None
        images = await self.get_nsfw_image(NsfwApis.GelbooruApi, rating, tag)

        if self.plus:
            return images
        else:
            return choice(images)["file_url"]

    async def yandere(self, rating: Optional[str] = None, tag: Optional[str] = None):
        if rating is None:
            rating = choice(["questionable", "explicit"])

        images = await self.get_nsfw_image(NsfwApis.YandereApi, rating, tag)

        if self.plus:
            return images
        else:
            return choice(images)["file_url"]

    async def konachan(self, rating: Optional[str] = None, tag: Optional[str] = None):
        if rating is None:
            rating = choice(["questionable", "explicit"])

        images = await self.get_nsfw_image(NsfwApis.KonachanApi, rating, tag)

        if self.plus:
            return images
        else:
            return choice(images)["file_url"]

    async def hentai(self, rating: Optional[str] = None):
        if rating == None:
            rating = ["questionable", "explicit"]
            rating = choice(rating)

        gelbooru_image = await self.gelbooru(rating)

        yandere_image = await self.yandere(rating)

        konachan_image = await self.konachan(rating)

        h = [gelbooru_image, yandere_image, konachan_image]

        hentai: str = choice(h)

        if hentai == gelbooru_image:
            source = "Gelbooru"

        elif hentai == yandere_image:
            source = "Yande.re"

        elif hentai == konachan_image:
            source = "Konachan"

        return hentai, source

def shorten_url(url: str):
    api_url = "http://tinyurl.com/api-create.php"

    params = {"url": url}

    response = get(api_url, params=params)
    if response.status_code == 200:
        short_url = response.text
        time.sleep(1)
        return short_url
    else:
        return None


class Reminder:
    def __init__(self, user: Optional[User] = None):
        self.user = user

    def add(self, reason: str, time: int):
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

    def get_all_reminders(self):
        data = db.execute("SELECT * FROM reminderData").fetchall()
        db.commit()
        return data

    def get_all_user_reminders(self):
        data = db.execute(
            "SELECT * FROM reminderData WHERE userid = ?", (self.user.id,)
        ).fetchall()
        db.commit()
        return data if data is not None else None

    def remove(self, id: int):
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
        else:
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
        ]

    async def disabled_commands(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Jeanne.Choice[str]]:
        commands = Command(ctx.guild).list_all_disabled()
        return [
            Jeanne.Choice(name=command, value=command)
            for command in commands
            if current.lower() in command.lower()
        ]
    
    async def list_all_user_inventory(self, ctx:Interaction, current:str)->List[Jeanne.Choice[str]]:
        inventory=Inventory(ctx.user).fetch_user_inventory
        return [
            Jeanne.Choice(name=image[1], value=image[1])
            for image in inventory
            if current.lower() in str(image[1]).lower()
        ]
    
    
    async def get_all_wallpapers(self, ctx:Interaction, current:str)->List[Jeanne.Choice[str]]:
        wallpapers=Inventory.fetch_wallpapers()
        return [
            Jeanne.Choice(name=image[1], value=image[1])
            for image in wallpapers
            if current.lower() in str(image[1]).lower()
        ]



