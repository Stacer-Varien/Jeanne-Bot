from datetime import date, datetime, timedelta
from json import loads
from random import choice, randint
from humanfriendly import parse_timespan
from discord import Embed, Color, Emoji, Guild, Member, TextChannel, User
from requests import get, post
from config import db, TINYURL
from typing import Optional

current_time = date.today()


class Botban:
    def __init__(self, user: User) -> None:
        self.user = user

    def check_botbanned_user(self) -> bool:
        botbanned_data = db.execute(
            "SELECT * FROM botbannedData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        if botbanned_data == None:
            return False
        else:
            if self.user.id == botbanned_data[0]:
                return True

    def add_botbanned_user(self, reason: str):
        db.execute(
            "INSERT OR IGNORE INTO botbannedData (user_id, reason) VALUES (?,?)",
            (
                self.user.id,
                reason,
            ),
        )
        server_xp_data = db.execute(
            "SELECT * FROM serverxpData WHERE user_id = ?", (self.user.id,)
        ).fetchall()
        global_xp_data = db.execute(
            "SELECT * FROM globalxpData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        inventory_data = db.execute(
            "SELECT * FROM userWallpaperInventory WHERE user_id = ?", (self.user.id,)
        ).fetchall()
        bank_data = db.execute(
            "SELECT * FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        if server_xp_data == None:
            pass
        else:
            db.execute("DELETE FROM serverxpData WHERE user_id = ?", (self.user.id,))

        if global_xp_data == None:
            pass
        else:
            db.execute("DELETE * FROM globalxpData WHERE user_id = ?", (self.user.id,))

        if inventory_data == None:
            pass
        else:
            db.execute(
                "DELETE FROM userWallpaperInventory WHERE user_id = ?", (self.user.id,)
            )

        if bank_data == None:
            pass
        else:
            db.execute("DELETE FROM bankData WHERE user_id = ?", (self.user.id,))

        db.commit()


class Currency:
    def __init__(self, user: User) -> None:
        self.user = user

    def get_balance(self):
        data = db.execute(
            "SELECT amount FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        if data == None:
            return 0
        else:
            return data[0]

    def add_qp(self, amount: int) -> int:
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (self.user.id, amount, (current_time - timedelta(days=1))),
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

    def remove_qp(self, amount: int) -> int:
        db.execute(
            "UPDATE bankData SET amount = amount - ? WHERE user_id = ?",
            (
                amount,
                self.user.id,
            ),
        )
        db.commit()

    def give_daily(self) -> bool:
        current_time = datetime.now()
        next_claim = current_time + timedelta(days=1)
        data = db.execute(
            "SELECT * FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        if datetime.today().weekday() > 5:
            qp = 200
        else:
            qp = 100

        if data == None:
            cur = db.execute(
                "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
                (
                    self.user.id,
                    qp,
                    round(next_claim.timestamp()),
                ),
            )

            if cur.rowcount == 0:
                db.execute(
                    "UPDATE bankData SET claimed_date = ? , amount = amount + ? WHERE user_id = ?",
                    (
                        round(next_claim.timestamp()),
                        qp,
                        self.user.id,
                    ),
                )
            db.commit()
            return True

        elif data[2] < round(current_time.timestamp()):
            db.execute(
                "UPDATE bankData SET claimed_date = ? , amount = amount + ? WHERE user_id = ?",
                (
                    round(next_claim.timestamp()),
                    qp,
                    self.user.id,
                ),
            )
            db.commit()
            return True

        else:
            return False

    def get_next_daily(self):
        data = db.execute(
            "SELECT claimed_date FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return data[0]


class Inventory:
    def __init__(self, user: Optional[User] = None) -> None:
        self.user = user

    def fetch_wallpapers(self, qp: Emoji) -> Embed:
        w = db.execute("SELECT * FROM wallpapers").fetchall()

        backgrounds = Embed(
            title="Avaliable Background Pictures for Level Cards", color=Color.random()
        ).set_footer(text="To view them, click on the hyperlinked names")

        for a in w:
            backgrounds.add_field(
                name=f"{a[1]}",
                value="[Item ID: {}]({})\nPrice: 1000 {}".format(a[0], a[2], qp),
                inline=True,
            )
        db.commit()
        return backgrounds

    def get_wallpaper(self, item_id: str):
        wallpaper = db.execute(
            "SELECT * FROM wallpapers WHERE id = ?", (item_id,)
        ).fetchone()
        db.commit()
        return wallpaper

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
        else:
            db.execute(
                "UPDATE userWallpaperInventory SET selected = ? WHERE user_id = ? AND wallpaper = ?",
                (
                    0,
                    self.user.id,
                    wallpaper[0],
                ),
            )
            db.commit()

    def add_user_wallpaper(self, item_id: int):
        self.deselect_wallpaper()

        wallpaper = self.get_wallpaper(item_id)

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
        try:
            wallpaper = db.execute(
                "SELECT * FROM userWallpaperInventory WHERE user_id = ? and selected = ?",
                (
                    self.user.id,
                    1,
                ),
            ).fetchone()
            db.commit()
            return wallpaper
        except:
            return ""

    def use_wallpaper(self, name: str):
        if self.deselect_wallpaper() == None:
            return
        db.execute(
            "UPDATE userWallpaperInventory SET selected = ? WHERE wallpaper = ? AND user_id = ?",
            (
                1,
                name,
                self.user.id,
            ),
        )
        db.commit()

    def fetch_user_inventory(self):
        wallpapers = db.execute(
            "SELECT * FROM userWallpaperInventory WHERE user_id = ?", (self.user.id,)
        ).fetchall()

        if wallpapers == None:
            return None
        else:
            return wallpapers
            # for data in wallpapers:
            #    return f"[{data[1]}]({data[2]})\n"

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

        if cur.rowcount == 0:
            db.execute(
                "UPDATE userBio SET bio = ? WHERE user_id = ?",
                (
                    bio,
                    self.user.id,
                ),
            )
        db.commit()

    def get_bio(self):
        data = db.execute(
            "SELECT bio FROM userBio WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        if data == None:
            return None
        else:
            return data[0]

    def set_color(self, color: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO userBio (user_id, color) VALUES (?,?)",
            (
                self.user.id,
                color,
            ),
        )

        if cur.rowcount == 0:
            db.execute(
                "UPDATE userBio SET color = ? WHERE user_id = ?",
                (
                    color,
                    self.user.id,
                ),
            )
        db.commit()

    def get_color(self):
        data = db.execute(
            "SELECT color FROM userBio WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        if data == None:
            return None
        else:
            return data[0]


class Levelling:
    def __init__(
        self, member: Optional[Member] = None, server: Optional[Guild] = None
    ) -> None:
        self.member = member
        self.server = server

    def get_member_xp(self):
        xp = db.execute(
            "SELECT exp FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()
        if xp == None:
            return 0
        else:
            return xp[0]

    def get_user_xp(self):
        xp = db.execute(
            "SELECT exp FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()
        if xp == None:
            return 0
        else:
            return xp[0]

    def get_member_cumulated_xp(self):
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()
        if cumulated_exp == None:
            return 0
        else:
            return cumulated_exp[0]

    def get_user_cumulated_xp(self):
        cumulated_exp = db.execute(
            "SELECT cumulative_exp FROM globalxpData WHERE user_id = ?",
            (self.member.id,),
        ).fetchone()
        db.commit()
        if cumulated_exp == None:
            return 0
        else:
            return cumulated_exp[0]

    def get_member_level(self):
        level = db.execute(
            "SELECT lvl FROM serverxpData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        ).fetchone()
        db.commit()
        if level == None:
            return 0
        else:
            return level[0]

    def get_user_level(self):
        level = db.execute(
            "SELECT lvl FROM globalxpData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()
        if level == None:
            return 0
        else:
            return level[0]

    def add_xp(self):
        if datetime.today().weekday() > 4:
            xp = 10
        else:
            xp = 5
        cursor1 = db.execute(
            "INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?,?)",
            (
                self.server.id,
                self.member.id,
                0,
                xp,
                xp,
            ),
        )

        cursor2 = db.execute(
            "INSERT OR IGNORE INTO globalxpData (user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?)",
            (
                self.member.id,
                0,
                xp,
                xp,
            ),
        )

        if cursor1.rowcount == 0:
            server_exp = self.get_member_xp()
            cumulated_exp = self.get_member_cumulated_xp()

            server_updated_exp = server_exp + xp
            server_updated_cumulative_exp = cumulated_exp + xp

            db.execute(
                "UPDATE serverxpData SET exp = ?, cumulative_exp = ? WHERE guild_id = ? AND user_id = ?",
                (
                    server_updated_exp,
                    server_updated_cumulative_exp,
                    self.server.id,
                    self.member.id,
                ),
            )

        db.commit()

        if cursor2.rowcount == 0:
            global_exp = self.get_user_xp()
            global_cumulated_exp = self.get_user_cumulated_xp()

            global_updated_exp = global_exp + xp
            global_updated_cumulated_exp = global_cumulated_exp + xp

            db.execute(
                "UPDATE globalxpDATA SET exp = ?, cumulative_exp = ? WHERE user_id = ?",
                (
                    global_updated_exp,
                    global_updated_cumulated_exp,
                    self.member.id,
                ),
            )

        db.commit()

        global_cumulated_exp = self.get_user_cumulated_xp()
        global_level = self.get_user_level()
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

        server_cumulated_exp = self.get_member_cumulated_xp()
        server_level = self.get_member_level()
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

    def add_level_channel(
        self, channel: TextChannel, message: Optional[str] = None
    ) -> None:
        if message == None:
            message = 0

        cur = db.execute(
            "INSERT OR IGNORE INTO levelNotifierData (server_id, channel_id, message) VALUES (?,?,?)",
            (
                self.server.id,
                channel.id,
                message,
            ),
        )

        if cur.rowcount == 0:
            if channel:
                db.execute(
                    "UPDATE levelNotifierData SET channel_id = ? WHERE server_id =?",
                    (
                        channel.id,
                        self.server.id,
                    ),
                )
            if message:
                db.execute(
                    "UPDATE levelNotifierData SET message = ? WHERE server_id =?",
                    (
                        message,
                        self.server.id,
                    ),
                )
        db.commit()

    def get_level_channel(self):
        data = db.execute(
            "SELECT * FROM levelNotifierData WHERE server_id = ?", (self.server.id,)
        ).fetchone()
        db.commit()

        if data == None:
            return None
        else:
            return data

    def get_server_rank(self):
        leaders_query = db.execute(
            "SELECT user_id FROM serverxpData WHERE guild_id = ? ORDER BY lvl DESC LIMIT 15;",
            (self.server.id,),
        )
        db.commit()
        return leaders_query.fetchall()

    def get_global_rank(self):
        leaders_query = db.execute(
            "SELECT user_id FROM globalxpData ORDER BY lvl DESC LIMIT 15;"
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
        if data == None:
            return False
        else:
            return True

    def add_xpblacklist(self, channel: TextChannel):
        db.execute(
            "INSERT OR IGNORE INTO xpChannelData (server, channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

    def remove_blacklist(self, channel: TextChannel):
        db.execute(
            "DELETE FROM xpChannelData WHERE server = ? AND channel = ?",
            (
                self.server.id,
                channel.id,
            ),
        )
        db.commit()

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

    def get_blacklisted_channels(self):
        data = db.execute(
            "SELECT channel FROM xpChannelData WHERE server = ?", (self.server.id,)
        ).fetchall()
        db.commit()

        if data == None:
            return None
        else:
            return data


class Manage:
    def __init__(self, server: Guild, channel: Optional[TextChannel] = None) -> None:
        self.server = server
        self.channel = channel

    def set_welcomer(self):
        cursor = db.execute(
            "INSERT OR IGNORE INTO welcomerData (guild_id, channel_id) VALUES (?,?)",
            (
                self.server.id,
                self.channel.id,
            ),
        )

        if cursor.rowcount == 0:
            db.execute(
                f"UPDATE welcomerData SET channel_id = ? WHERE guild_id = ?",
                (
                    self.channel.id,
                    self.server.id,
                ),
            )
        db.commit()

    def set_leaver(self):
        cursor = db.execute(
            "INSERT OR IGNORE INTO leaverData (guild_id, channel_id) VALUES (?,?)",
            (
                self.server.id,
                self.channel.id,
            ),
        )

        if cursor.rowcount == 0:
            db.execute(
                f"UPDATE leaverData SET channel_id = ? WHERE guild_id = ?",
                (
                    self.channel.id,
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

        if cursor.rowcount == 0:
            db.execute(
                f"UPDATE modlogData SET channel_id = ? WHERE guild_id = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
        db.commit()

    def set_reporter(self):
        cursor = db.execute(
            "INSERT OR IGNORE INTO reportData (guild_id, channel_id) VALUES (?,?)",
            (
                self.server.id,
                self.channel.id,
            ),
        )

        if cursor.rowcount == 0:
            db.execute(
                f"UPDATE reportData SET channel_id = ? WHERE guild_id = ?",
                (
                    self.server.id,
                    self.channel.id,
                ),
            )
        db.commit()

    def remove_welcomer(self):
        cur = db.cursor()
        cur.execute("SELECT * FROM welcomerData WHERE guild_id = ?", (self.server.id,))
        result = cur.fetchone()

        if result == None:
            return False

        else:
            cur.execute(
                "DELETE FROM welcomerData WHERE guild_id = ?", (self.server.id,)
            )
            db.commit()

    def remove_leaver(self):
        cur = db.cursor()
        cur.execute("SELECT * FROM leaverData WHERE guild_id = ?", (self.server.id,))
        result = cur.fetchone()

        if result == None:
            return False

        else:
            cur.execute("DELETE FROM leaverData WHERE guild_id = ?", (self.server.id,))
            db.commit()

    def remove_modloger(self):
        cur = db.cursor()
        cur.execute("SELECT * FROM modlogData WHERE guild_id = ?", (self.server.id,))
        result = cur.fetchone()

        if result == None:
            return False

        else:
            cur.execute("DELETE FROM modlogData WHERE guild_id = ?", (self.server.id,))
            db.commit()

    def remove_reporter(self):
        cur = db.cursor()
        cur.execute("SELECT * FROM reportData WHERE guild_id = ?", (self.server.id,))
        result = cur.fetchone()

        if result == None:
            return False

        else:
            cur.execute("DELETE FROM reportData WHERE guild_id = ?", (self.server.id,))

            db.commit()

    def remove_levelup(self):
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM levelNotifierData WHERE server_id = ?", (self.server.id,)
        )
        result = cur.fetchone()

        if result == None:
            return False

        else:
            cur.execute(
                "DELETE FROM levelNotifierData WHERE server_id = ?", (self.server.id,)
            )

            db.commit()


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

        cur = db.execute(
            "INSERT OR IGNORE INTO warnDatav2 (guild_id, user_id, warn_points) VALUES (?,?,?)",
            (self.server.id, self.member.id, 1),
        )

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
        if len(warnings) == 0:
            return None
        elif warnings == None:
            return None
        else:
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

        if len(warnings) == 0:
            return None
        elif warnings == None:
            return None
        else:
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

        if result == None:
            return None

        else:
            return result

    def revoke_warn(self, warn_id: int):
        cur = db.cursor()
        cur.execute("DELETE FROM warnData WHERE warn_id = ?", (warn_id,))

        cur.execute(
            "UPDATE warnDatav2 SET warn_points = warn_points - ? WHERE user_id = ? AND guild_id = ?",
            (
                1,
                self.member.id,
                self.server.id,
            ),
        )

        wp_query = cur.execute(
            f"SELECT warn_points FROM warnDatav2 WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                self.server.id,
            ),
        )
        warnpoints = wp_query.fetchone()[0]

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
        modlog_channel_query = db.execute(
            "SELECT channel_id FROM modlogData WHERE guild_id = ?", (self.server.id,)
        ).fetchone()

        if modlog_channel_query == None:
            return None
        else:
            return modlog_channel_query[0]

    def get_report_channel(self):
        data = db.execute(
            "SELECT channel_id FROM reportData WHERE guild_id = ?", (self.server.id,)
        ).fetchone()
        return data

    def get_welcomer(self):
        data = db.execute(
            "SELECT * FROM welcomerData where guild_id = ?", (self.server.id,)
        ).fetchone()
        return data

    def get_leaver(self):
        data = db.execute(
            "SELECT * FROM leaverData where guild_id = ?", (self.server.id,)
        ).fetchone()
        return data

    def set_message_logger(self, channel: TextChannel):
        cur = db.execute(
            "INSERT OR IGNORE INTO messageLogData (server, channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )

        if cur.rowcount == 0:
            db.execute(
                "UPDATE messageLogData SET channel = ? WHERE server = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
        db.commit()

    def get_message_logger(self):
        try:
            channel = db.execute(
                "SELECT channel FROM messageLogData WHERE server = ?", (self.server.id,)
            ).fetchone()
            db.commit()
            return channel[0]
        except:
            return False

    def set_member_logger(self, channel: TextChannel):
        cur = db.execute(
            "INSERT OR IGNORE INTO memberLogData (server, channel) VALUES (?,?)",
            (
                self.server.id,
                channel.id,
            ),
        )

        if cur.rowcount == 0:
            db.execute(
                "UPDATE memberLogData SET channel = ? WHERE server = ?",
                (
                    channel.id,
                    self.server.id,
                ),
            )
        db.commit()

    def remove_messagelog(self):
        cur = db.cursor()
        cur.execute(
            "SELECT channel FROM messageLogData WHERE server = ?", (self.server.id,)
        )
        result = cur.fetchone()

        if result == None:
            return False

        else:
            db.execute("DELETE FROM messageLogData WHERE server = ?", (self.server.id,))

            db.commit()


class Welcomer:
    def __init__(self, server: Guild) -> None:
        self.server = server

    def get_welcoming_msg(self):
        data = db.execute(
            "SELECT welcoming FROM welcomerMsgData WHERE server = ?", (self.server.id,)
        ).fetchone()

        if data == None or 0:
            return None
        else:
            return data[0]

    def get_leaving_msg(self):
        data = db.execute(
            "SELECT leaving FROM welcomerMsgData WHERE server = ?", (self.server.id,)
        ).fetchone()

        if data == None or 0:
            return None
        else:
            return data[0]

    def remove_welcomer_msg(self):
        data = db.execute(
            "SELECT welcoming FROM welcomerMsgData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        if data == None:
            return None
        else:
            db.execute(
                "UPDATE welcomerMsgData SET welcoming = ? WHERE server = ?",
                (
                    0,
                    self.server.id,
                ),
            )
            db.commit()

    def remove_leaving_msg(self):
        data = db.execute(
            "SELECT leaving FROM welcomerMsgData WHERE server = ?", (self.server.id,)
        ).fetchone()
        db.commit()
        if data == None:
            return None
        else:
            db.execute(
                "UPDATE welcomerMsgData SET leaving = ? WHERE server = ?",
                (
                    0,
                    self.server.id,
                ),
            )
            db.commit()

    def set_welcomer_msg(server: int, json_script: str):
        cur = db.execute(
            "INSERT OR IGNORE INTO welcomerMsgData (server, welcoming, leaving) VALUES (?,?,?)",
            (
                server,
                json_script,
                0,
            ),
        )

        if cur.rowcount == 0:
            db.execute(
                "UPDATE welcomerMsgData SET welcoming = ? WHERE server = ?",
                (
                    json_script,
                    server,
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

        if cur.rowcount == 0:
            db.execute(
                "UPDATE welcomerMsgData SET leaving = ? WHERE server = ?",
                (
                    json_script,
                    self.server.id,
                ),
            )
        db.commit()


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


class Hentai:
    def __init__(self, plus: Optional[bool] = None) -> None:
        self.plus = plus

    def add_blacklisted_link(self, link: str):
        db.execute("INSERT OR IGNORE INTO hentaiBlacklist (links) VALUES (?)", (link,))
        db.execute()

    def get_blacklisted_links(self):
        data = db.execute("SELECT links FROM hentaiBlacklist").fetchall()

        if data == None:
            return None
        else:
            for i in data:
                return i

    def gelbooru(self, rating: Optional[str] = None, tag: Optional[str] = None):
        bl = self.get_blacklisted_links()
        if rating == None:
            rating = ["questionable", "explicit"]
            rating = choice(rating)

        if tag == None:
            gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub"
        else:
            formated_tag = tag.replace(" ", "_")
            gelbooru_api = (
                f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub+"
                + formated_tag
            )

        response = get(gelbooru_api)
        ret = loads(response.text)

        filtered_ret = []
        for dictionary in ret["post"]:
            if dictionary["file_url"] != bl[0]:
                filtered_ret.append(dictionary)

        if self.plus == True:
            return filtered_ret
        else:
            return str(filtered_ret[randint(1, 100) - 1]["file_url"])

    def yandere(self, rating: Optional[str] = None, tag: Optional[str] = None):
        blacklisted_links = self.get_blacklisted_links()

        if rating is None:
            rating = choice(["questionable", "explicit"])

        tag_query = f"rating:{rating}+-loli+-shota+-cub"
        if tag:
            tag_query += f"+{tag.replace(' ', '_')}"

        yandere_api = get(
            f"https://yande.re/post.json?limit=100&shown:true&tags={tag_query}"
        ).json()

        filtered_ret = [
            post for post in yandere_api if post["file_url"] not in blacklisted_links
        ]

        if self.plus:
            return filtered_ret
        else:
            return str(choice(filtered_ret)["file_url"])

    def konachan(self, rating: Optional[str] = None, tag: Optional[str] = None):
        bl = self.get_blacklisted_links()
        if rating == None:
            rating = ["questionable", "explicit"]
            rating = choice(rating)

        if tag == None:
            konachan_api = get(
                f"https://konachan.com/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub"
            ).json()

        else:
            formated_tag = tag.replace(" ", "_")
            konachan_api = get(
                f"https://konachan.com/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub+"
                + formated_tag
            ).json()
        filtered_ret = []
        for dictionary in konachan_api:
            if dictionary["file_url"] != bl[0]:
                filtered_ret.append(dictionary)
        if self.plus == True:
            return konachan_api
        else:
            return str(konachan_api[randint(1, 100) - 1]["file_url"])

    def hentai(self, rating: Optional[str] = None):
        if rating == None:
            rating = ["questionable", "explicit"]
            rating = choice(rating)

        gelbooru_image = self.gelbooru(rating)

        yandere_image = self.yandere(rating)

        konachan_image = self.konachan(rating)

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
        return short_url
    else:
        return None
