from io import BytesIO
from typing import Literal
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
import aiohttp
from discord import Member, User
from functions import BetaTest, Currency, Inventory, Levelling, Partner, get_richest
import requests
from discord import Interaction
import os
from discord.ext.commands import Bot


class Profile:
    def __init__(self, bot: Bot):
        self.bot = bot
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.default_bg = os.path.join(assets_dir, "card.png")
        self.font1 = os.path.join(assets_dir, "font.ttf")
        self.badges = {
            "vote": os.path.join(assets_dir, "voted.png"),
            "first": os.path.join(assets_dir, "1st.png"),
            "second": os.path.join(assets_dir, "2nd.png"),
            "third": os.path.join(assets_dir, "3rd.png"),
            "creator": os.path.join(assets_dir, "creator.png"),
            "richest": os.path.join(assets_dir, "richest.png"),
            "top_30": os.path.join(assets_dir, "top30.png"),
            "top_100": os.path.join(assets_dir, "top100.png"),
            "partner": os.path.join(assets_dir, "partner.png"),
            "qp": os.path.join(assets_dir, "qp.png"),
            "beta": os.path.join(assets_dir, "beta.png"),
        }

    @staticmethod
    def enhance_and_paste(image: Image, position: tuple[int, int], card: Image.Image):
        enhancer = ImageEnhance.Brightness(image)
        enhanced_image = enhancer.enhance(1.1)
        card.paste(enhanced_image, position, enhanced_image)

    @staticmethod
    def format_number(value: int) -> str:
        if value < 1000:
            return str(value)
        if value < 1_000_000:
            return f"{value / 1000:.1f}k"
        return f"{value / 1_000_000:.1f}M"

    async def fetch_image(self, url: str) -> BytesIO | Literal[False]:
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return False
                return BytesIO(await resp.read())

    async def generate_profile(
        self,
        ctx: Interaction,
        user: User | Member,
        bg_image: str = None,
        voted: bool = False,
        country: str = None,
    ) -> BytesIO | Literal[False]:
        inventory_instance = Inventory(user)
        background = await self.fetch_image(bg_image) if bg_image else self.default_bg
        if not background:
            return False

        card = Image.open(background).convert("RGBA")
        card = ImageEnhance.Brightness(card).enhance(
            float(inventory_instance.get_brightness) / 100
        )

        if card.size != (900, 500):
            card = card.resize((900, 500), resample=Image.Resampling.LANCZOS)

        profile_bytes = BytesIO(requests.get(user.display_avatar.url).content)
        profile = (
            Image.open(profile_bytes)
            .convert("RGBA")
            .resize((180, 180), resample=Image.Resampling.LANCZOS)
        )

        mask = Image.new("L", (180, 180), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 180, 180), fill=255)
        profile_pic_holder = Image.new("RGBA", card.size, (255, 255, 255, 0))
        profile_pic_holder.paste(profile, (30, 250), mask)

        font_small = ImageFont.truetype(self.font1, 30)
        font_color = inventory_instance.get_color
        color = (
            tuple(ImageColor.getcolor(font_color, "RGB"))
            if font_color
            else (204, 204, 255)
        )

        draw = ImageDraw.Draw(card)
        draw.text(
            (215, 320),
            str(user),
            color,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
        )
        draw.ellipse((30, 250, 210, 430), outline=color)

        badges = await self.get_badges(user, voted, country)
        for badge, x_pos in badges:
            self.enhance_and_paste(badge, (x_pos, 430), card)

        card.paste(profile_pic_holder, (0, 0), profile_pic_holder)

        profile_canvas = self.create_profile_canvas(ctx, user, color, inventory_instance)
        profile_canvas.paste(card, (0, 0), card)

        final_bytes = BytesIO()
        profile_canvas.save(final_bytes, "png")
        final_bytes.seek(0)
        return final_bytes

    async def get_badges(self, user: User, voted: bool, country: str) -> list[tuple[Image.Image, int]]:
        badges = []
        x_position = 840

        if voted:
            badges.append((Image.open(self.badges["vote"]).resize((50, 50)), x_position))
            x_position -= 60

        grank, rrank = Levelling(user).get_user_global_rank, get_richest(user)
        if grank is not None and grank <= 100:
            rank_badge = self.get_rank_badge(grank)
            badges.append((rank_badge, x_position))
            x_position -= 60

        if rrank < 15:
            badges.append((Image.open(self.badges["richest"]).resize((50, 50)), x_position))
            x_position -= 60

        if country:
            country_img = os.path.join(
                os.path.dirname(__file__), "assets", "country", f"{country}.png"
            )
            badges.append((Image.open(country_img).resize((50, 50)), x_position))
            x_position -= 60

        if Partner.check(user):
            badges.append((Image.open(self.badges["partner"]).resize((50, 50)), x_position))
            x_position -= 60

        if await BetaTest(self.bot).check(user):
            badges.append((Image.open(self.badges["beta"]).resize((50, 50)), x_position))
            x_position -= 60

        if user.id == 597829930964877369:
            badges.append((Image.open(self.badges["creator"]).resize((50, 50)), x_position))
            x_position -= 60

        return badges

    def get_rank_badge(self, rank: int) -> Image.Image:
        if rank == 1:
            return Image.open(self.badges["first"]).resize((50, 50))
        if rank == 2:
            return Image.open(self.badges["second"]).resize((50, 50))
        if rank == 3:
            return Image.open(self.badges["third"]).resize((50, 50))
        if rank <= 30:
            return Image.open(self.badges["top_30"]).resize((50, 50))
        return Image.open(self.badges["top_100"]).resize((50, 50))

    def create_profile_canvas(self, ctx:Interaction, user: User, color: tuple[int, int, int], inventory_instance: Inventory) -> Image.Image:
        canvas = Image.new("RGB", (900, 900), (32, 32, 32))
        draw = ImageDraw.Draw(canvas)

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            global_rank_text = "Global Rank"
            server_rank_text = "Server Rank"
            qp_balance_text = "QP Balance"
            global_level_text = "Global Level"
            global_xp_text = "Global XP"
            server_level_text = "Server Level"
            server_xp_text = "Server XP"
            no_bio_text = "No bio available"
            rank_font_size = 35
        elif ctx.locale.value == "fr":
            global_rank_text = "Classement Global"
            server_rank_text = "Classement Serveur"
            qp_balance_text = "Solde QP"
            global_level_text = "Niveau Global"
            global_xp_text = "XP Globale"
            server_level_text = "Niveau Serveur"
            server_xp_text = "XP Serveur"
            no_bio_text = "Aucune bio disponible"
            rank_font_size = 27

        currency_instance = Currency(user)
        levelling_instance = Levelling(user, user.guild)

        font_small = ImageFont.truetype(self.font1, 30)

        # Draw text and rectangles for ranks, levels, and bio
        draw.text(
            (40, 520),
            text=global_rank_text,
            fill=color,
            font=ImageFont.truetype(self.font1, rank_font_size),
            stroke_width=1,
            align="center",
        )
        draw.text(
            (330, 520),
            text=server_rank_text,
            fill=color,
            font=ImageFont.truetype(self.font1, rank_font_size),
            stroke_width=1,
            align="center",
        )
        draw.text(
            (620, 520),
            text=qp_balance_text,
            fill=color,
            font=ImageFont.truetype(self.font1, 35),
            stroke_width=1,
            align="center",
        )

        # qp rect
        draw.rounded_rectangle((610, 510, 870, 630), outline=color, radius=6)

        global_rank = ("#" + str(levelling_instance.get_user_global_rank)) if levelling_instance.get_user_global_rank else "N/A"
        draw.text(
            (70, 570),
            global_rank,
            color,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
            align="center",
        )
        server_rank = ("#" + str(levelling_instance.get_member_server_rank)) if levelling_instance.get_member_server_rank else "N/A"
        draw.text(
            (370, 570),
            server_rank,
            color,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
        )

        draw.text(
            (640, 570),
            f"{self.format_number(currency_instance.get_balance)}",
            color,
            font=ImageFont.truetype(self.font1, 45),
            stroke_width=1,
        )
        qp = Image.open(self.badges["qp"]).resize((50, 50))
        canvas.paste(qp, (820, 570), qp)

        # global level bar
        draw.rounded_rectangle(
            (10, 680, 890, 693), outline=color, width=2, radius=6
        )
        global_level, global_user_xp = (
            levelling_instance.get_user_level,
            levelling_instance.get_user_xp,
        )
        draw.text(
            (20, 640),
            f"{global_level_text}: {global_level}",
            color,
            font=font_small,
            stroke_width=1,
        )
        global_next_xp = (global_level * 50) + ((global_level - 1) * 25) + 50
        draw.text(
            (520, 640),
            f"{global_xp_text}: {self.format_number(global_user_xp)}/{self.format_number(global_next_xp)}",
            color,
            font=font_small,
            stroke_width=1,
        )

        # global rank rect
        draw.rounded_rectangle((30, 510, 290, 630), outline=color, radius=6)

        global_xpneed = global_next_xp - levelling_instance.get_user_xp
        global_xphave = global_user_xp

        global_current_percentage = (global_xphave / global_xpneed) * 100
        global_length_of_bar = (global_current_percentage * 8.76) + 12

        draw.rounded_rectangle(
            (12, 682, global_length_of_bar, 691), fill=color, radius=6
        )
        server_level, server_user_xp = (
            levelling_instance.get_member_level,
            levelling_instance.get_member_xp,
        )

        draw.text(
            (20, 710),
            f"{server_level_text}: {server_level}",
            color,
            font=font_small,
            stroke_width=1,
        )
        server_next_xp = (server_level * 50) + ((server_level - 1) * 25) + 50
        draw.text(
            (520, 710),
            f"{server_xp_text}: {self.format_number(server_user_xp)}/{self.format_number(server_next_xp)}",
            color,
            font=font_small,
            stroke_width=1,
        )
        # server rank rect
        draw.rounded_rectangle((320, 510, 580, 630), outline=color, radius=6)

        # server rank bar
        draw.rounded_rectangle(
            (10, 750, 890, 763), outline=color, width=2, radius=6
        )

        server_xpneed = server_next_xp - levelling_instance.get_member_xp
        server_xphave = server_user_xp

        server_current_percentage = (server_xphave / server_xpneed) * 100
        server_length_of_bar = (server_current_percentage * 8.76) + 12

        draw.rounded_rectangle(
            (12, 752, server_length_of_bar, 761), fill=color, radius=6
        )

        bio = inventory_instance.get_bio
        bio = no_bio_text if bio == None else bio

        draw.rounded_rectangle(
            (10, 780, 890, 890), radius=7, width=2, outline=color, fill=(59, 59, 59)
        )
        draw.text(
            (20, 790),
            f"{bio}",
            color,
            font=ImageFont.truetype(self.font1, 25),
            stroke_width=1,
        )

        return canvas
