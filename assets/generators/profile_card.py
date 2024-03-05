from io import BytesIO
from typing import Literal
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
from discord import Member, User
from functions import BetaTest, Currency, Inventory, Levelling, Partner, get_richest
import requests
import math
import os
from discord.ext.commands import Bot


class Profile:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.default_bg = os.path.join(os.path.dirname(__file__), "assets", "card.png")
        self.font1 = os.path.join(os.path.dirname(__file__), "assets", "font.ttf")
        self.vote_badge = os.path.join(os.path.dirname(__file__), "assets", "voted.png")
        self.first_badge = os.path.join(os.path.dirname(__file__), "assets", "1st.png")
        self.second_badge = os.path.join(os.path.dirname(__file__), "assets", "2nd.png")
        self.third_badge = os.path.join(os.path.dirname(__file__), "assets", "3rd.png")
        self.creator_badge = os.path.join(
            os.path.dirname(__file__), "assets", "creator.png"
        )
        self.richest_badge = os.path.join(
            os.path.dirname(__file__), "assets", "richest.png"
        )
        self.top_30_badge = os.path.join(
            os.path.dirname(__file__), "assets", "top30.png"
        )
        self.top_100_badge = os.path.join(
            os.path.dirname(__file__), "assets", "top100.png"
        )
        self.partner = os.path.join(os.path.dirname(__file__), "assets", "partner.png")
        self.qp = os.path.join(os.path.dirname(__file__), "assets", "qp.png")
        self.beta = os.path.join(os.path.dirname(__file__), "assets", "beta.png")

    async def generate_profile(
        self,
        user: User | Member,
        bg_image:str=None,
        voted: bool = None,
    )->BytesIO|Literal[False]:
        inventory_instance = Inventory(user)
        
        background = BytesIO(
            requests.get(bg_image).content if (bg_image != None) else self.default_bg
        )
        
        currency_instance = Currency(user)
        levelling_instance = Levelling(user, user.guild)
        card = Image.open(background).convert("RGBA")

        card = ImageEnhance.Brightness(card).enhance(
            float(inventory_instance.get_brightness / 100)
        )

        width, height = card.size
        if width == 900 and height == 500:
            pass

        elif width > 900 and height > 500:
            x1 = 0
            y1 = 0
            x2 = width
            nh = math.ceil(width * 0.528888)
            y2 = 0

            if nh < height:
                y2 = nh + y1

            card = card.crop((x1, y1, x2, y2)).resize(
                (900, 500), resample=Image.LANCZOS
            )

        else:
            return False
        
        # profile
        profile_bytes = BytesIO(requests.get(user.display_avatar.url).content)
        profile = Image.open(profile_bytes)
        profile = profile.convert("RGBA").resize((180, 180), resample=Image.LANCZOS)

        profile_pic_holder = Image.new("RGBA", card.size, (255, 255, 255, 0))

        mask = Image.new("RGBA", card.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((30, 250, 210, 430), fill=(255, 25, 255, 255))

        # ======== Fonts to use =============
        font_small = ImageFont.truetype(self.font1, 30)

        # ======== Colors ========================
        font_color = inventory_instance.get_color
        COLOR = (
            tuple(ImageColor.getcolor(font_color, "RGB"))
            if font_color
            else (204, 204, 255)
        )

        def get_str(xp: int):
            if xp < 1000:
                return str(xp)
            if xp >= 1000 and xp < 1000000:
                return str(round(xp / 1000, 1)) + "k"
            if xp > 1000000:
                return str(round(xp / 1000000, 1)) + "M"

        def get_str_qp(balance: int):
            if balance < 1000:
                return str(balance)
            if balance >= 1000 and balance < 1000000:
                return str(round(balance / 1000, 1)) + "k"
            if balance > 1000000:
                return str(round(balance / 1000000, 1)) + "M"

        draw = ImageDraw.Draw(card)
        draw.text(
            (215, 320),
            str(user),
            COLOR,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
        )

        draw.ellipse((30, 250, 210, 430), fill=(255, 255, 255, 0), outline=COLOR)

        voter = Image.open(self.vote_badge).resize((50, 50))
        richest = Image.open(self.richest_badge).resize((50, 50))
        _1st = Image.open(self.first_badge).resize((50, 50))
        _2nd = Image.open(self.second_badge).resize((50, 50))
        _3rd = Image.open(self.third_badge).resize((50, 50))
        top30 = Image.open(self.top_30_badge).resize((50, 50))
        top100 = Image.open(self.top_100_badge).resize((50, 50))
        creator_badge = Image.open(self.creator_badge).resize((50, 50))
        partner_badge = Image.open(self.partner).resize((50, 50))
        qp = Image.open(self.qp).resize((50, 50))
        betatest = Image.open(self.beta).resize((50, 50))

        if voted == True:
            enhancer = ImageEnhance.Brightness(voter)
            voter = enhancer.enhance(1.1)
            card.paste(voter, (840, 430), voter)
        grank, srank, rrank = (
            levelling_instance.get_member_global_rank,
            levelling_instance.get_member_server_rank,
            get_richest(user),
        )

        if grank <= 100:
            if grank == 1:
                ranked = _1st
            elif grank == 2:
                ranked = _2nd
            elif grank == 3:
                ranked = _3rd
            elif grank <= 30:
                ranked = top30
            else:
                ranked = top100

            ranked = ImageEnhance.Brightness(ranked).enhance(1.1)
            card.paste(ranked, (780, 430), ranked)

        if rrank < 15:
            richest = ImageEnhance.Brightness(richest).enhance(1.1)
            card.paste(richest, (720, 430), richest)

        if user.id == 597829930964877369:
            creator_badge = ImageEnhance.Brightness(creator_badge).enhance(1.1)
            card.paste(creator_badge, (660, 430), creator_badge)

        if Partner.check(user.id):
            partner_badge = ImageEnhance.Brightness(partner_badge).enhance(1.1)
            card.paste(partner_badge, (600, 430), partner_badge)

        beta = await BetaTest(self.bot).check(user)
        if beta == True:
            betatest = ImageEnhance.Brightness(betatest).enhance(1.1)
            card.paste(betatest, (540, 430), betatest)

        profile_pic_holder.paste(profile, (30, 250))

        pre = Image.composite(profile_pic_holder, card, mask)

        profile_canvas = Image.new("RGB", (900, 900), (32, 32, 32))
        profile_draw = ImageDraw.Draw(profile_canvas)

        profile_draw.text(
            (30, 510),
            text="Global Rank",
            fill=COLOR,
            font=ImageFont.truetype(self.font1, 35),
            stroke_width=1,
        )
        profile_draw.text(
            (330, 510),
            text="Server Rank",
            fill=COLOR,
            font=ImageFont.truetype(self.font1, 35),
            stroke_width=1,
        )
        profile_draw.text(
            (630, 510),
            text="QP Balance",
            fill=COLOR,
            font=ImageFont.truetype(self.font1, 35),
            stroke_width=1,
        )

        global_rank = ("#" + str(grank)) if grank else "N/A"
        profile_draw.text(
            (70, 570),
            global_rank,
            COLOR,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
        )
        server_rank = ("#" + str(srank)) if srank else "N/A"
        profile_draw.text(
            (370, 570),
            server_rank,
            COLOR,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
        )

        profile_draw.text(
            (640, 570),
            f"{get_str_qp(currency_instance.get_balance)}",
            COLOR,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
        )
        profile_canvas.paste(qp, (760, 570), qp)

        profile_draw.rectangle((10, 680, 890, 693), outline=COLOR, width=2)
        global_level, global_user_xp = (
            levelling_instance.get_user_level,
            levelling_instance.get_user_xp,
        )
        profile_draw.text(
            (20, 640),
            f"Global Level: {global_level}",
            COLOR,
            font=font_small,
            stroke_width=1,
        )
        global_next_xp = (global_level * 50) + ((global_level - 1) * 25) + 50
        profile_draw.text(
            (520, 640),
            f"Global XP: {get_str(global_user_xp)}/{get_str(global_next_xp)}",
            COLOR,
            font=font_small,
            stroke_width=1,
        )

        global_xpneed = global_next_xp - levelling_instance.get_user_xp
        global_xphave = global_user_xp - levelling_instance.get_user_xp

        global_current_percentage = (global_xphave / global_xpneed) * 100
        global_length_of_bar = (global_current_percentage * 8.76) + 12

        profile_draw.rectangle((12, 682, global_length_of_bar, 691), fill=COLOR)
        server_level, server_user_xp = (
            levelling_instance.get_member_level,
            levelling_instance.get_member_xp,
        )

        profile_draw.text(
            (20, 710),
            f"Server Level: {server_level}",
            COLOR,
            font=font_small,
            stroke_width=1,
        )
        server_next_xp = (server_level * 50) + ((server_level - 1) * 25) + 50
        profile_draw.text(
            (520, 710),
            f"Server XP: {get_str(server_user_xp)}/{get_str(server_next_xp)}",
            COLOR,
            font=font_small,
            stroke_width=1,
        )

        profile_draw.rectangle((10, 750, 890, 763), outline=COLOR, width=2)

        server_xpneed = server_next_xp - levelling_instance.get_member_xp
        server_xphave = server_user_xp - levelling_instance.get_member_xp

        server_current_percentage = (server_xphave / server_xpneed) * 100
        server_length_of_bar = (server_current_percentage * 8.76) + 12

        profile_draw.rectangle((12, 752, server_length_of_bar, 761), fill=COLOR)

        bio = inventory_instance.get_bio
        bio = "No bio available" if bio == None else bio

        profile_draw.rounded_rectangle(
            (10, 780, 890, 890), radius=7, width=2, outline=COLOR, fill=(59, 59, 59)
        )
        profile_draw.text(
            (20, 790),
            f"{bio}",
            COLOR,
            font=ImageFont.truetype(self.font1, 25),
            stroke_width=1,
        )

        profile_canvas.paste(pre)
        final_bytes = BytesIO()
        profile_canvas.save(final_bytes, "png")
        final_bytes.seek(0)
        return final_bytes
