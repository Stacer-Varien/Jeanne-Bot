from io import BytesIO
from typing import Literal
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
from discord import Member, User
from config import DBL_AUTH
from functions import BetaTest, Currency, DBLvoter, Inventory, Levelling, Partner, get_richest
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
        self.dbl_badge = os.path.join(
            os.path.dirname(__file__), "assets", "discordbotlist.png"
        )
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

    @staticmethod
    def enhance_and_paste(image: Image, position: int, card: Image.Image):
        enhancer = ImageEnhance.Brightness(image)
        enhanced_image = enhancer.enhance(1.1)
        card.paste(enhanced_image, position, enhanced_image)

    async def generate_profile(
        self,
        user: User | Member,
        bg_image: str = None,
        voted: bool = False,
        dbl_voter: bool = False,
        country: str = None,
    ) -> BytesIO | Literal[False]:
        inventory_instance = Inventory(user)

        background = (
            self.default_bg
            if bg_image is None
            else BytesIO(requests.get(bg_image).content)
        )

        currency_instance = Currency(user)
        levelling_instance = Levelling(user, user.guild)
        card = Image.open(background).convert("RGBA")

        card = ImageEnhance.Brightness(card).enhance(
            float(inventory_instance.get_brightness) / 100
        )

        width, height = card.size
        if width == 900 and height == 500:
            pass
        elif width > 900 and height > 500:
            x1 = 0
            y1 = 0
            x2 = width
            nh = math.ceil(width * 0.528888)
            y2 = nh if nh < height else height
            card = card.crop((x1, y1, x2, y2)).resize(
                (900, 500), resample=Image.Resampling.LANCZOS
            )
        else:
            return False

        profile_bytes = BytesIO(requests.get(user.display_avatar.url).content)
        profile = (
            Image.open(profile_bytes)
            .convert("RGBA")
            .resize((180, 180), resample=Image.Resampling.LANCZOS)
        )
        profile_pic_holder = Image.new("RGBA", card.size, (255, 255, 255, 0))

        mask = Image.new("RGBA", card.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((30, 250, 210, 430), fill=(255, 25, 255, 255))

        font_small = ImageFont.truetype(self.font1, 30)
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
        qp = Image.open(self.qp).resize((50, 50))

        badges = []
        x_position = 840

        if voted:
            voter = Image.open(self.vote_badge).resize((50, 50))
            badges.append((voter, x_position))
            x_position -= 60

        if dbl_voter:
            dblvoter = Image.open(self.dbl_badge).resize((50, 50))
            badges.append((dblvoter, x_position))
            x_position -= 60

        grank, srank, rrank = (
            levelling_instance.get_user_global_rank,
            levelling_instance.get_member_server_rank,
            get_richest(user),
        )

        if grank is not None and grank <= 100:
            if grank == 1:
                ranked = Image.open(self.first_badge).resize((50, 50))
            elif grank == 2:
                ranked = Image.open(self.second_badge).resize((50, 50))
            elif grank == 3:
                ranked = Image.open(self.third_badge).resize((50, 50))
            elif grank <= 30:
                ranked = Image.open(self.top_30_badge).resize((50, 50))
            else:
                ranked = Image.open(self.top_100_badge).resize((50, 50))

            badges.append((ranked, x_position))
            x_position -= 60

        if rrank < 15:
            richest = Image.open(self.richest_badge).resize((50, 50))
            badges.append((richest, x_position))
            x_position -= 60

        if country:
            country_img = os.path.join(
                os.path.dirname(__file__), "assets", "country", f"{country}.png"
            )
            cimage = Image.open(country_img).convert("RGBA").resize((50, 50))
            badges.append((cimage, x_position))
            x_position -= 60

        if Partner.check(user.id):
            partner_badge = Image.open(self.partner).resize((50, 50))
            badges.append((partner_badge, x_position))
            x_position -= 60

        beta = await BetaTest(self.bot).check(user)
        if beta:
            betatest = Image.open(self.beta).resize((50, 50))
            badges.append((betatest, x_position))
            x_position -= 60

        if user.id == 597829930964877369:
            creator_badge = Image.open(self.creator_badge).resize((50, 50))
            badges.append((creator_badge, x_position))
            x_position -= 60

        for badge, x_pos in badges:
            self.enhance_and_paste(badge, (x_pos, 430), card)

        profile_pic_holder.paste(profile, (30, 250))

        pre = Image.composite(profile_pic_holder, card, mask)

        profile_canvas = Image.new("RGB", (900, 900), (32, 32, 32))
        profile_draw = ImageDraw.Draw(profile_canvas)

        profile_draw.text(
            (40, 520),
            text=f"Global Rank",
            fill=COLOR,
            font=ImageFont.truetype(self.font1, 35),
            stroke_width=1, align="center"
        )
        profile_draw.text(
            (330, 520),
            text="Server Rank",
            fill=COLOR,
            font=ImageFont.truetype(self.font1, 35),
            stroke_width=1, align="center"
        )
        profile_draw.text(
            (620, 520),
            text="QP Balance",
            fill=COLOR,
            font=ImageFont.truetype(self.font1, 35),
            stroke_width=1,
            align="center",
        )

        # qp rect
        profile_draw.rounded_rectangle((610, 510, 870, 630), outline=COLOR, radius=6)

        global_rank = ("#" + str(grank)) if grank else "N/A"
        profile_draw.text(
            (70, 570),
            global_rank,
            COLOR,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
            align="center",
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
        profile_canvas.paste(qp, (820, 570), qp)

        # global level bar
        profile_draw.rounded_rectangle((10, 680, 890, 693), outline=COLOR, width=2, radius=6)
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

        # global rank rect
        profile_draw.rounded_rectangle((30,510,290,630), outline=COLOR, radius=6)

        global_xpneed = global_next_xp - levelling_instance.get_user_xp
        global_xphave = global_user_xp

        global_current_percentage = (global_xphave / global_xpneed) * 100
        global_length_of_bar = (global_current_percentage * 8.76) + 12

        profile_draw.rounded_rectangle((12, 682, global_length_of_bar, 691), fill=COLOR, radius=6)
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
        # server rank rect
        profile_draw.rounded_rectangle((320,510,580,630), outline=COLOR, radius=6)

        # server rank bar
        profile_draw.rounded_rectangle((10, 750, 890, 763), outline=COLOR, width=2, radius=6)

        server_xpneed = server_next_xp - levelling_instance.get_member_xp
        server_xphave = server_user_xp

        server_current_percentage = (server_xphave / server_xpneed) * 100
        server_length_of_bar = (server_current_percentage * 8.76) + 12

        profile_draw.rounded_rectangle((12, 752, server_length_of_bar, 761), fill=COLOR, radius=6)

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
