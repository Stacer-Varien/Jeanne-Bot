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

def get_wallpaper(item_id):
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

def add_user_custom_wallpaper(user, name, link):
    user_inv = connect("./User_Inventories/{}.db".format(user))
    cur = user_inv.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS backgrounds (item_id text, link_bg text, selected int)")
    cur.execute(
        "INSERT OR IGNORE INTO backgrounds (item_id, link_bg, selected) VALUES (?,?,?)", (name, link, 0,))
    user_inv.commit()
    remove_qp(user, 1000)


def fetch_user_inventory(user: int, type=['bg']):
    user_inv = connect("./User_Inventories/{}.db".format(user))
    cur = user_inv.cursor()
    if type == 'bg':
        cur.execute("SELECT * FROM backgrounds").fetchall()
        user_inv.commit()

    
