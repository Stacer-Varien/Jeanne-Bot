from datetime import date, datetime, timedelta
from shutil import rmtree
from humanfriendly import parse_timespan
from discord import Embed, Color, Emoji
from config import db, inv_db
from os import listdir, makedirs, path
from requests import get

current_time = date.today()


def check_botbanned_user(user: int):
    try:
        botbanquery = db.execute(
            "SELECT * FROM botbannedData WHERE user_id = ?", (user,))
        botbanned_data = botbanquery.fetchone()
        if user == botbanned_data[0]:
            return(True)
    except:
        return(False)


def get_balance(user: int):
    a = db.execute("SELECT amount FROM bankData WHERE user_id = ?", (user,))
    data = a.fetchone()

    if data == None:
        return 0
    else:
        return data[0]


def add_qp(user: int, amount: int):
    cur = db.execute("INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
                     (user, amount, (current_time - timedelta(days=1))))

    if cur.rowcount == 0:
        db.execute(
            "UPDATE bankData SET amount = amount + ? WHERE user_id = ?", (amount, user,))
    db.commit()


def remove_qp(user: int, amount: int):
    db.execute(
        "UPDATE bankData SET amount = amount - ? WHERE user_id = ?", (amount, user,))
    db.commit()


def give_daily(user: int):
    current_time = datetime.now()
    next_claim= current_time + timedelta(days=1)
    data = db.execute("SELECT * FROM bankData WHERE user_id = ?", (user,)).fetchone()

    if data == None:
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)", (user, 100, round(next_claim.timestamp()),))

        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET claimed_date = ? , amount = amount + 100 WHERE user_id = ?", (round(next_claim.timestamp()), user,))
        db.commit()
        return(True)

    elif data[2] < round(current_time.timestamp()):
        db.execute(
            "UPDATE bankData SET claimed_date = ? , amount = amount + 100 WHERE user_id = ?", (round(next_claim.timestamp()), user,))
        db.commit()
        return(True)

    else:
        return(False)

def get_next_daily(user:int):
    data = db.execute("SELECT claimed_date FROM bankData WHERE user_id = ?", (user,)).fetchone()
    db.commit()
    return data[0]


def add_botbanned_user(user: int, reason: str):
    try:
        db.execute(
            "INSERT OR IGNORE INTO botbannedData (user_id, reason) VALUES (?,?)", (user, reason,))

        cur = db.cursor()

        cur.execute("SELECT * FROM serverxpData WHERE user_id = ?", (user,))
        server_user_id = cur.fetchall()

        if server_user_id == None:
            pass

        else:
            cur.execute("DELETE FROM serverxpData WHERE user_id = ?", (user,))

        cur.execute("SELECT * FROM globalxpData WHERE user_id = ?", (user,))
        global_user_id = cur.fetchone()

        if global_user_id == None:
            pass

        else:
            cur.execute("DELETE FROM globalxpData WHERE user_id = ?", (user,))

        cur.execute("SELECT * FROM bankData WHERE user_id = ?", (user,))
        user_bank = cur.fetchone()

        if user_bank == None:
            pass

        else:
            cur.execute("DELETE FROM bankData WHERE user_id = ?", (user,))

        try:
            rmtree("./User_Inventories/{}".format(user))
        except:
            pass

        db.commit()

        return(True)
    except:
        return(False)


def fetch_wallpapers(qp:Emoji):
    w = db.execute("SELECT * FROM wallpapers").fetchall()

    backgrounds = Embed(title='Avaliable Background Pictures for Level Cards', color=Color.blue(
    )).set_footer(text="To view them, click on the hyperlinked names")

    for a in w:
        backgrounds.add_field(
            name=f"{a[1]}", value='[Item ID: {}]({})\nPrice: 1000 {}'.format(a[0], a[2], qp), inline=True)
    db.commit()
    return backgrounds


def get_wallpaper(item_id: str):
    wallpaper = db.execute(
        'SELECT * FROM wallpapers WHERE id = ?', (item_id,)).fetchone()
    db.commit()
    return wallpaper


def create_user_inventory(user):
    try:
        makedirs('./User_Inventories/{}/wallpapers'.format(str(user)))
    except:
        return(False)


def add_user_wallpaper(user, item_id):
    wallpaper = get_wallpaper(item_id)

    img_data = get(wallpaper[2]).content

    with open(r"./User_Inventories/{}/wallpapers/{}.png".format(str(user), wallpaper[1]), 'wb') as handler:
        handler.write(img_data)

    data=db.execute("INSERT OR IGNORE INTO userWallpaperInventory (user_id, wallpaper) VALUES (?,?)", (user, wallpaper[1],))

    if data.rowcount==0:
        db.execute("UPDATE userWallpaperInventory SET wallpaper = ? WHERE user_id = ?", (wallpaper[1], user,))
    remove_qp(user, 1000)


def add_user_custom_wallpaper(user: int, name: str, link: str):

    img_data = get(link).content

    with open(r"./User_Inventories/{}/wallpapers/{}.png".format(str(user), name), 'wb') as handler:
        handler.write(img_data)

    data = db.execute(
        "INSERT OR IGNORE INTO userWallpaperInventory (user_id, wallpaper) VALUES (?,?)", (user, name,))

    if data.rowcount == 0:
        db.execute(
            "UPDATE userWallpaperInventory SET wallpaper = ? WHERE user_id = ?", (name, user,))

    remove_qp(user, 1000)

################################################################################################################
def selected_wallpaper(user):
    try:
        wallpaper=db.execute("SELECT wallpaper FROM userWallpaperInventory WHERE user_id = ?", (user,)).fetchone()
        db.commit()
        image = path.join(
            path.dirname(__file__), 'User_Inventories', str(user), 'wallpapers', '{}.png'.format(wallpaper[0]))
        return image
    except:
        return ''

def use_wallpaper(name, user):
    db.execute(
        "UPDATE userWallpaperInventory SET wallpaper = ? WHERE user_id = ?", (name, user,))

def fetch_user_inventory(user: int):
    inventory = listdir("./User_Inventories/{}/wallpapers/".format(user))
    inventory.sort()
    return '\n'.join(inventory)
    


def get_member_xp(member: int, server: int):
    xp = db.execute("SELECT exp FROM serverxpData WHERE user_id = ? AND guild_id = ?",
                    (member, server,)).fetchone()
    db.commit()
    return xp[0]


def get_user_xp(user: int):
    xp = db.execute(
        "SELECT exp FROM globalxpData WHERE user_id = ?", (user,)).fetchone()
    db.commit()
    return xp[0]


def get_member_cumulated_xp(member: int, server: int):
    cumulated_exp = db.execute(
        "SELECT cumulative_exp FROM serverxpData WHERE user_id = ? AND guild_id = ?", (member, server,)).fetchone()
    db.commit()
    return cumulated_exp[0]


def get_user_cumulated_xp(user: int):
    cumulated_exp = db.execute(
        "SELECT cumulative_exp FROM globalxpData WHERE user_id = ?", (user,)).fetchone()
    db.commit()
    return cumulated_exp[0]


def get_member_level(member: int, server: int):
    level = db.execute(
        "SELECT lvl FROM serverxpData WHERE user_id = ? AND guild_id = ?", (member, server,)).fetchone()
    db.commit()
    return level[0]


def get_user_level(user: int):
    level = db.execute(
        "SELECT lvl FROM globalxpData WHERE user_id = ?", (user,)).fetchone()
    db.commit()
    return level[0]


def add_xp(member: int, server: int):
    cursor1 = db.execute("INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?,?)", (
        server, member, 0, 5, 5,))

    cursor2 = db.execute(
        "INSERT OR IGNORE INTO globalxpData (user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?)", (member, 0, 5, 5,))

    xp = 5
    if cursor1.rowcount == 0:
        server_exp = get_member_xp(member, server)
        cumulated_exp = get_member_cumulated_xp(member, server)

        server_updated_exp = server_exp + xp
        server_updated_cumulative_exp = cumulated_exp + xp

        db.execute("UPDATE serverxpData SET exp = ?, cumulative_exp = ? WHERE guild_id = ? AND user_id = ?",
                   (server_updated_exp, server_updated_cumulative_exp, server, member,))

    db.commit()

    if cursor2.rowcount == 0:
        global_exp = get_user_xp(member)
        global_cumulated_exp = get_user_cumulated_xp(member)

        global_updated_exp = global_exp + xp
        global_updated_cumulated_exp = global_cumulated_exp + xp

        db.execute("UPDATE globalxpDATA SET exp = ?, cumulative_exp = ? WHERE user_id = ?",
                   (global_updated_exp, global_updated_cumulated_exp, member,))

    db.commit()


def add_level(member: int, server: int):
    server_cumulated_exp = get_member_cumulated_xp(member, server)
    server_level = get_member_level(member, server)
    server_next_lvl_exp = ((server_level * 50) +
                           ((server_level - 1) * 25) + 50)

    if server_cumulated_exp >= server_next_lvl_exp:
        server_updated_exp = server_cumulated_exp - server_next_lvl_exp
        db.execute("UPDATE serverxpData SET lvl = lvl + ?, exp = ? WHERE guild_id = ? AND user_id = ?",
                   (1, server_updated_exp, server, member,))

    db.commit()

    global_cumulated_exp = get_user_cumulated_xp(member)
    global_level = get_user_level(member)
    global_next_lvl_exp = ((global_level * 50) +
                           ((global_level - 1) * 25) + 50)

    if global_cumulated_exp >= global_next_lvl_exp:
        global_updated_exp = global_cumulated_exp - server_next_lvl_exp
        db.execute("UPDATE globalxpData SET lvl = lvl + ?, exp = ? WHERE user_id = ?",
                   (1, global_updated_exp, member,))
    db.commit()


def get_server_rank(server: int):
    leaders_query = db.execute(
        "SELECT user_id FROM serverxpData WHERE guild_id = ? ORDER BY lvl DESC LIMIT 15;", (server,))
    db.commit()
    return leaders_query.fetchall()


def get_global_rank():
    leaders_query = db.execute(
        "SELECT user_id FROM globalxpData ORDER BY lvl DESC LIMIT 15;")
    db.commit()
    return leaders_query.fetchall()


def set_welcomer(server: int, channel: int):
    cursor = db.execute(
        "INSERT OR IGNORE INTO welcomerData (guild_id, channel_id) VALUES (?,?)", (server, channel,))

    if cursor.rowcount == 0:
        db.execute(
            f"UPDATE welcomerData SET channel_id = ? WHERE guild_id = ?", (channel, server,))
    db.commit()


def set_leaver(server: int, channel: int):
    cursor = db.execute(
        "INSERT OR IGNORE INTO leaverData (guild_id, channel_id) VALUES (?,?)", (server, channel,))

    if cursor.rowcount == 0:
        db.execute(
            f"UPDATE leaverData SET channel_id = ? WHERE guild_id = ?", (channel, server,))
    db.commit()


def set_modloger(server: int, channel: int):
    cursor = db.execute(
        "INSERT OR IGNORE INTO modlogData (guild_id, channel_id) VALUES (?,?)", (server, channel,))

    if cursor.rowcount == 0:
        db.execute(
            f"UPDATE modlogData SET channel_id = ? WHERE guild_id = ?", (channel, server,))
    db.commit()


def set_reporter(server: int, channel: int):
    cursor = db.execute(
        "INSERT OR IGNORE INTO reportData (guild_id, channel_id) VALUES (?,?)", (server, channel,))

    if cursor.rowcount == 0:
        db.execute(
            f"UPDATE reportData SET channel_id = ? WHERE guild_id = ?", (channel, server,))
    db.commit()


def remove_welcomer(server: int):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM welcomerData WHERE guild_id = ?", (server,))
    result = cur.fetchone()

    if result == None:
        return(False)

    else:
        cur.execute(
            "SELECT channel_id FROM welcomerData WHERE guild_id = ?", (server,))
        result = cur.fetchone()
        cur.execute(
            "DELETE FROM welcomerData WHERE channel_id = ?", (result[0],))
        db.commit()
        return(True)


def remove_leaver(server: int):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM leaverData WHERE guild_id = ?", (server,))
    result = cur.fetchone()

    if result == None:
        return(False)

    else:
        cur.execute(
            "SELECT channel_id FROM leaverData WHERE guild_id = ?", (server,))
        result = cur.fetchone()
        cur.execute(
            "DELETE FROM leaverData WHERE channel_id = ?", (result[0],))
        db.commit()
        return True


def remove_modloger(server: int):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM modlogData WHERE guild_id = ?", (server,))
    result = cur.fetchone()

    if result == None:
        return(False)

    else:
        cur.execute(
            "SELECT channel_id FROM modlogData WHERE guild_id = ?", (server,))
        result = cur.fetchone()
        cur.execute(
            "DELETE FROM modlogData WHERE channel_id = ?", (result[0],))
        db.commit()
        return(True)


def remove_reporter(server: int):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM reportData WHERE guild_id = ?", (server,))
    result = cur.fetchone()

    if result == None:
        return(False)

    else:
        cur.execute(
            "SELECT channel_id FROM reportData WHERE guild_id = ?", (server,))
        result = cur.fetchone()
        cur.execute(
            "DELETE FROM reportData WHERE channel_id = ?", (result[0],))

        db.commit()
        return(True)


def warn_user(server: int, member: int, moderator: int, reason: str, warn_id: int, date: int):

    db.execute("INSERT OR IGNORE INTO warnData (guild_id, user_id, moderator_id, reason, warn_id, date) VALUES (?,?,?,?,?,?)",
               (server, member, moderator, reason, warn_id, date,))

    cur = db.execute(
        "INSERT OR IGNORE INTO warnDatav2 (guild_id, user_id, warn_points) VALUES (?,?,?)", (server, member, 1))

    if cur.rowcount == 0:
        db.execute(
            "UPDATE warnDatav2 SET warn_points = warn_points + ? WHERE guild_id = ? and user_id = ?", (1, server, member))
    db.commit()


def get_modlog_channel(server: int):
    modlog_channel_query = db.execute(
        f'SELECT channel_id FROM modlogData WHERE guild_id = ?', (server,)).fetchone()

    if modlog_channel_query == None:
        return None
    else:
        return modlog_channel_query[0]


def fetch_warnings_server(server: int):
    cur = db.cursor()
    warnings = cur.execute(
        "SELECT * FROM warnDATAv2 WHERE guild_id = ?", (server,))
    db.commit()
    return warnings


def fetch_warnings_user(member: int, server: int):
    cur = db.cursor()
    warnings = cur.execute(
        "SELECT * FROM warnDATA user WHERE user_id = ? AND guild_id = ?", (member, server,))
    db.commit()
    return warnings


def check_warn_id(server: int, warn_id: int):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM warnData WHERE guild_id = ? AND warn_id = ?", (server, warn_id,))
    result = cur.fetchone()
    db.commit()

    if result == None:
        return None

    else:
        return result


def revoke_warn(member: int, server: int, warn_id: int):
    cur = db.cursor()
    cur.execute("DELETE FROM warnData WHERE warn_id = ?", (warn_id,))

    cur.execute("UPDATE warnDatav2 SET warn_points = warn_points - ? WHERE user_id = ? AND guild_id = ?", (1, member, server))

    wp_query = cur.execute(
        f"SELECT warn_points FROM warnDatav2 WHERE user_id = ? AND guild_id = ?", (member, server))
    warnpoints = wp_query.fetchone()[0]

    if warnpoints == 0:
        cur.execute(
            f"DELETE FROM warnDatav2 WHERE user_id = ? AND guild_id = ?", (member, server))

    db.commit()


def get_report_channel(server: int):
    data = db.execute(
        "SELECT channel_id FROM reportData WHERE guild_id = ?", (server,)).fetchone()
    return data


def fetch_welcomer(channel: int):
    data = db.execute(
        "SELECT guild_id FROM welcomerData where channel_id = ?", (channel,)).fetchone()
    return data[0]


def get_welcomer(server: int):
    data = db.execute(
        "SELECT channel_id FROM welcomerData where guild_id = ?", (server,)).fetchone()
    return data[0]


def fetch_leaver(channel: int):
    data = db.execute(
        "SELECT guild_id FROM leaverData where channel_id = ?", (channel,)).fetchone()
    return data[0]


def get_leaver(server: int):
    data = db.execute(
        "SELECT channel_id FROM leaverData where guild_id = ?", (server,)).fetchone()
    return data[0]

def get_user_bank(user:int):
    data=db.execute("SELECT user_id FROM bankData WHERE user_id = ?", (user)).fetchone()
    return data[0]

def add_wallpaper(id, name, link):
    inv_db.execute("INSERT OR IGNORE INTO wallpapers (id, name, link, price) VALUES (?,?,?,?)", (id, name, link, 1000,))
    db.commit()

def add_voter(user_id:int):
    if check_botbanned_user(user_id) is True:
        pass
    else:

        new_vote=int(round((datetime.now() + timedelta(hours=12)).timestamp()))
        weekend = datetime.today().weekday()

        voted=db.execute("SELECT voted FROM votersData WHERE user_id = ?", (user_id,)).fetchone()

        if voted==None:
            ids=db.execute("INSERT OR IGNORE INTO votersData (user_id, voted) VALUES (?,?)", (user_id, new_vote,))

            if ids.rowcount==0:
                db.execute("UPDATE votersData SET voted = ? WHERE user_id = ?", (new_vote, user_id,))

            db.commit()

            if weekend < 5:
                add_qp(user_id, 50)
            elif weekend > 5:
                add_qp(user_id, 100)

        
        elif int(round(datetime.now().timestamp())) > new_vote:
            db.execute("UPDATE votersData SET voted = ? WHERE user_id = ?", (new_vote, user_id,))
            db.commit()

            if weekend < 5:
                add_qp(user_id, 50)
            elif weekend > 5:
                add_qp(user_id, 100)

            
        else:
            pass

def get_voters():
    voters=db.execute("SELECT user_id FROM votersData").fetchall()

    if voters==None:
        pass
    else:
        for a in voters:
            return a[0]


def check_mute_role(guild_id: int):
    role = db.execute("SELECT role_id FROM muteroleData WHERE guild_id = ?", (guild_id,)).fetchone()
    db.commit()
    if role ==None:
        return(False)
    else:
        return role[0]
    

def add_mute_role(guild:int, role_id:int):
    role=db.execute("INSERT OR IGNORE INTO muteroleData (guild_id, role_id) VALUES (?,?)", (guild, role_id,))

    if role.rowcount==0:
        db.execute("UPDATE muteroleData SET role_id = ? WHERE guild_id = ?", (role_id, guild,))

    db.commit()

def mute_member(member:int, guild:int, ends:str=None):
    
    if ends ==None:
        ends=99999999999 #infinite value for now
    else:
        seconds = parse_timespan(ends)
        ends = round((datetime.now() + timedelta(seconds=seconds)).timestamp())
        
    
    data=db.execute("INSERT OR IGNORE INTO mutedMembers (user_id, guild_id, ends) VALUES (?,?,?)", (member, guild, ends,))
    
    if data.rowcount==0:
        db.execute("UPDATE mutedMembers SET ends = ? WHERE user_id = ? AND guild_id = ?", (ends, member, guild,))

    db.commit()

def get_muted_data():
    data = db.execute("SELECT * FROM mutedMembers").fetchall()
    db.commit()
    return data

def remove_mute(member:int, guild:int):
    db.execute("DELETE FROM mutedMembers WHERE user_id = ? AND guild_id = ?",
               (member, guild,))
    db.commit()


def get_softban_data():
    data = db.execute("SELECT * FROM softbannedMembers").fetchall()
    db.commit()
    return data

def softban_member(member: int, guild: int, ends: str = None):

    if ends == None:
        ends = 99999999999  # infinite value for now
    else:
        seconds = parse_timespan(ends)
        ends = round((datetime.now() + timedelta(seconds=seconds)).timestamp())

    db.execute(
        "INSERT OR IGNORE INTO softbannedMembers (user_id, guild_id, ends) VALUES (?,?,?)", (member, guild, ends,))

    db.commit()

def remove_softban(member:int, guild:int):
    db.execute("DELETE FROM softbannedMembers WHERE user_id = ? AND guild_id = ?",
               (member, guild,))
    db.commit()