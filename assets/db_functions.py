from datetime import date, timedelta
from sqlite3 import connect
from nextcord import Embed, Color
from config import db, inv_db
from os import remove

current_time = date.today()

def check_botbanned_user(user: int):
    try:
        botbanquery = db.execute(
            "SELECT * FROM botbannedData WHERE user_id = ?", (user,))
        botbanned_data = botbanquery.fetchone()
        return botbanned_data[0]
    except:
        pass

def get_balance(user: int):
    a = db.execute("SELECT amount FROM bankData WHERE user_id = ?", (user,))
    data = a.fetchone()

    if data == None:
        return 0
    else:
        return data[0]

def add_qp(user: int, amount: int):
    cur = db.execute("INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)", (user, amount, (current_time - timedelta(days=1))))

    if cur.rowcount == 0:
        db.execute("UPDATE bankData SET amount = amount + ? WHERE user_id = ?", (amount, user,))
    db.commit()

def remove_qp(user: int, amount: int):
    db.execute("UPDATE bankData SET amount = amount - ? WHERE user_id = ?", (amount, user,))
    db.commit()

def give_daily(user:int):
    current_time = date.today()

    try:
        claimed = db.execute(
            "SELECT claimed_date FROM bankData WHERE user_id = ?", (user,)).fetchone()
    except:
        pass
    if claimed == None:
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)", (user, 100, current_time))

        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET claimed_date = ? , amount = amount + 100 WHERE user_id = ?", (current_time, user,))
        db.commit()
        return(True)

    elif (date.today() - date.fromisoformat(str(claimed[0]))).days > 0:
        db.execute(
            "UPDATE bankData SET claimed_date = ? , amount = amount + 100 WHERE user_id = ?", (current_time, user,))
        db.commit()
        return(True)

    else:
        return(False)

def add_botbanned_user(user:int, reason:str):
    try:
        db.execute("INSERT OR IGNORE INTO botbannedData (user_id, reason) VALUES (?,?)", (user, reason,))

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
            remove("./User_Inventories/{}.db".format(user))
        except:
            pass

        return(True)
    except:
        return(False)

def fetch_wallpapers():
    w = inv_db.execute("SELECT * FROM wallpapers").fetchall()

    backgrounds = Embed(title='Avaliable Background Pictures for Level Cards', color=Color.blue(
          )).set_footer(text="To view them, click on the hyperlinked names")

    for a in w:
        backgrounds.add_field(name=f"{a[1]}", value='[Item ID: {}]({})'.format(a[0], a[2]), inline=True)
    inv_db.commit()
    return backgrounds

def get_wallpaper(item_id:str):
    wallpaper = inv_db.execute('SELECT * FROM wallpapers WHERE id = ?', (item_id,)).fetchone()
    return wallpaper

def get_user_inventory(user):
    user_inv=connect("./User_Inventories/{}.db".format(user))
    cur=user_inv.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS backgrounds (item_id text, link_bg text, selected int)")
    user_inv.commit()

def add_user_wallpaper(user, item_id):
    user_inv = connect("./User_Inventories/{}.db".format(user))
    cur = user_inv.cursor()
    wallpaper = get_wallpaper(item_id)
    cur.execute("INSERT OR IGNORE INTO backgrounds (item_id, link_bg, selected) VALUES (?,?,?)",
                (item_id, wallpaper[2], 0,))
    user_inv.commit()
    remove_qp(user, 1000)

def add_user_custom_wallpaper(user:int, name:str, link:str):
    user_inv = connect("./User_Inventories/{}.db".format(user))
    cur = user_inv.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS backgrounds (item_id text, link_bg text, selected int)")
    cur.execute(
        "INSERT OR IGNORE INTO backgrounds (item_id, link_bg, selected) VALUES (?,?,?)", (name, link, 0,))
    user_inv.commit()
    remove_qp(user, 1000)

def fetch_user_inventory(user: int):
    user_inv = connect("./User_Inventories/{}.db".format(user))
    cur = user_inv.cursor()
    inv = cur.execute("SELECT * FROM backgrounds").fetchall()
    return inv

def get_member_xp(member:int, server:int):
    xp = db.execute("SELECT exp FROM serverxpData WHERE user_id = ? AND guild_id = ?", (member, server,)).fetchone()
    return xp

def get_user_xp(user: int):
    xp = db.execute("SELECT exp FROM globalxpData WHERE user_id =", (user,)).fetchone()
    return xp[0]

def get_member_cumulated_xp(member: int, server: int):
    cumulated_exp = db.execute(
        "SELECT cumulative_exp FROM serverxpData WHERE user_id = ? AND guild_id = ?", (member, server,)).fetchone()
    return cumulated_exp[0]

def get_user_cumulated_xp(user: int):
    cumulated_exp=db.execute("SELECT cumulative_exp FROM globalxpData WHERE user_id =", (user,)).fetchone()
    return cumulated_exp[0]

def get_member_level(member: int, server:int):
    level=db.execute("SELECT lvl FROM serverxpData WHERE user_id =", (member, server,)).fetchone()
    return level[0]

def get_user_level(user: int):
    level = db.execute("SELECT lvl FROM globalxpData WHERE user_id =", (user,)).fetchone()
    return level[0]

def add_xp(member:int, server:int):
    cursor1 = db.execute("INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?,?)", (
        server, member, 0, 5, 5,))

    cursor2 = db.execute(
        "INSERT OR IGNORE INTO globalxpData (user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?)", (member, 0, 5, 5,))

    xp = 5
    if cursor1.rowcount == 0:
        server_exp = get_member_xp(member, server)
        cumulated_exp=get_member_cumulated_xp(member, server)

        server_updated_exp = server_exp + xp
        server_updated_cumulative_exp = cumulated_exp + xp

        db.execute("UPDATE serverxpData SET exp = ?, cumulative_exp = ? WHERE guild_id = ? AND user_id = ?", (server_updated_exp, server_updated_cumulative_exp, server, member,))
    
    db.commit()

    if cursor2.rowcount == 0:
        global_exp=get_user_xp(member)
        global_cumulated_exp=get_user_cumulated_xp(member)

        global_updated_exp = global_exp + xp
        global_updated_cumulated_exp = global_cumulated_exp + xp

        db.execute("UPDATE globalxpDATA SET exp = ?, cumulative_exp = ? WHERE user_id = ?",(global_updated_exp, global_updated_cumulated_exp, member,))
    
    db.commit()

def add_level(member:int, server:int):
    server_cumulated_exp = get_member_cumulated_xp(member, server)
    server_level=get_member_level(member, server)
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

def get_used_wallpaper(user:int):
    user_inv = connect("./User_Inventories/{}.db".format(user))
    cur = user_inv.cursor()

    bg = cur.execute("SELECT link_bg FROM backgrounds WHERE selected = ?", (1,)).fetchone()

    if bg == None:
        return ''
    else:
        return bg[0]

def get_server_rank(server:int):
    leaders_query = db.execute("SELECT user_id FROM serverxpData WHERE guild_id = ? ORDER BY lvl DESC LIMIT 15;", (server,))

    return leaders_query.fetchall()


def get_global_rank():
    leaders_query = db.execute(
            "SELECT user_id FROM globalxpData ORDER BY lvl DESC LIMIT 15;")

    return leaders_query.fetchall()

def set_welcomer(server:int, channel:int):
    cursor = db.execute(
        "INSERT OR IGNORE INTO welcomerData (guild_id, channel_id) VALUES (?,?)", (server, channel,))

    if cursor.rowcount == 0:
        db.execute(f"UPDATE welcomerData SET channel_id = ? WHERE guild_id = ?", (channel, server,))
    db.commit()

def set_leaver(server:int, channel:int):
    cursor = db.execute(
        "INSERT OR IGNORE INTO leaverData (guild_id, channel_id) VALUES (?,?)", (server, channel,))

    if cursor.rowcount == 0:
        db.execute(f"UPDATE leaverData SET channel_id = ? WHERE guild_id = ?", (channel, server,))
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
        return "You have no leaver channel set"

    else:
        cur.execute(
            "SELECT channel_id FROM leaverData WHERE guild_id = ?", (server,))
        result = cur.fetchone()
        cur.execute(
            "DELETE FROM leaverData WHERE channel_id = ?", (result[0],))
        db.commit()


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