from io import BytesIO
from typing import Literal
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
import aiohttp
from discord import Member, User
from functions import BetaTest, Currency, Inventory, Levelling, Partner, get_richest
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

    @staticmethod
    def calculate_level_xp(level: int) -> int:
        return (level * 50) + ((level - 1) * 25) + 50

    @staticmethod
    def _fit_text(
        draw: ImageDraw.ImageDraw,
        value: str,
        font_path: str,
        start_size: int,
        max_width: int,
    ) -> ImageFont.FreeTypeFont:
        size = start_size
        font = ImageFont.truetype(font_path, size)
        while draw.textlength(value, font=font) > max_width and size > 20:
            size -= 2
            font = ImageFont.truetype(font_path, size)
        return font

    @staticmethod
    def draw_progress_bar(
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        width: int,
        height: int,
        percent: float,
        color: tuple,
        bg_color: tuple = (36, 40, 50, 230),
    ):
        safe_percent = max(0.0, min(100.0, percent))
        fill_width = int(width * (safe_percent / 100))

        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=height // 2,
            fill=bg_color,
        )
        if fill_width > 0:
            draw.rounded_rectangle(
                (x, y, x + fill_width, y + height),
                radius=height // 2,
                fill=color,
            )

    @staticmethod
    def _draw_glass_panel(
        draw: ImageDraw.ImageDraw,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        outline: tuple[int, int, int],
        alpha: int = 155,
    ):
        draw.rounded_rectangle(
            (x1, y1, x2, y2),
            radius=20,
            fill=(20, 24, 33, alpha),
            outline=outline,
            width=2,
        )

    @staticmethod
    def _draw_stat_card(
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        value: str,
        theme_color: tuple[int, int, int],
        font_label: ImageFont.FreeTypeFont,
        font_value: ImageFont.FreeTypeFont,
    ):
        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=16,
            fill=(23, 27, 37, 220),
            outline=theme_color,
            width=1,
        )
        draw.text((x + 14, y + 12), label, fill=theme_color, font=font_label)
        draw.text((x + 14, y + 52), value, fill=(240, 240, 247), font=font_value)

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
        currency_instance = Currency(user)

        guild = user.guild if isinstance(user, Member) else None
        levelling_instance = Levelling(user, guild)

        if bg_image:
            bg_data = await self.fetch_image(bg_image)
            card_bg = (
                Image.open(bg_data).convert("RGBA")
                if bg_data
                else Image.open(self.default_bg).convert("RGBA")
            )
        else:
            card_bg = Image.open(self.default_bg).convert("RGBA")

        card_bg = ImageEnhance.Brightness(card_bg).enhance(
            float(inventory_instance.get_brightness) / 100
        )

        if card_bg.size != (900, 500):
            card_bg = card_bg.resize((900, 500), resample=Image.Resampling.LANCZOS)

        final_canvas = Image.new("RGBA", (900, 900), (12, 16, 24, 255))
        final_canvas.paste(card_bg, (0, 0))

        # Strong top-to-bottom gradient for readability and depth
        overlay = Image.new("RGBA", (900, 500), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        for i in range(500):
            alpha = int(22 + (i / 500) * 110)
            overlay_draw.line((0, i, 900, i), fill=(8, 12, 18, alpha), width=1)
        final_canvas = Image.alpha_composite(final_canvas, overlay)

        draw = ImageDraw.Draw(final_canvas)

        font_color_hex = inventory_instance.get_color
        theme_color = (
            tuple(ImageColor.getcolor(font_color_hex, "RGB"))
            if font_color_hex
            else (204, 204, 255)
        )

        # Main info panel
        self._draw_glass_panel(draw, 25, 355, 875, 875, theme_color, alpha=152)
        draw.rectangle((40, 560, 860, 562), fill=theme_color)

        avatar_url = user.display_avatar.url
        avatar_data = await self.fetch_image(avatar_url)
        if not avatar_data:
            avatar_data = await self.fetch_image(user.default_avatar.url)
        if not avatar_data:
            return False

        profile_img = Image.open(avatar_data).convert("RGBA")
        profile_img = profile_img.resize((190, 190), resample=Image.Resampling.LANCZOS)

        mask = Image.new("L", (190, 190), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 190, 190), fill=255)

        pfp_x, pfp_y = 55, 380
        draw.ellipse(
            (pfp_x - 7, pfp_y - 7, pfp_x + 197, pfp_y + 197), fill=(8, 10, 16, 230)
        )
        draw.ellipse(
            (pfp_x - 3, pfp_y - 3, pfp_x + 193, pfp_y + 193),
            outline=theme_color,
            width=4,
        )
        final_canvas.paste(profile_img, (pfp_x, pfp_y), mask)

        username = str(user)
        name_font = self._fit_text(draw, username, self.font1, 56, 470)
        draw.text((270, 398), username, fill=theme_color, font=name_font)

        badges_list = await self.get_badges(user, voted, country)
        badge_start_x = 270
        for index, (badge, _) in enumerate(badges_list[:8]):
            self.enhance_and_paste(
                badge, (badge_start_x + index * 58, 468), final_canvas
            )

        lang = ctx.locale.value if ctx.locale else "en-US"
        if lang in ["fr"]:
            labels = {
                "g_rank": "Classement Global",
                "s_rank": "Classement Serveur",
                "bal": "Solde QP",
                "g_lvl": "Niveau Global",
                "s_lvl": "Niveau Serveur",
                "bio": "Aucune bio disponible",
            }
        else:
            labels = {
                "g_rank": "Global Rank",
                "s_rank": "Server Rank",
                "bal": "QP Balance",
                "g_lvl": "Global Level",
                "s_lvl": "Server Level",
                "bio": "No bio available",
            }

        font_header = ImageFont.truetype(self.font1, 26)
        font_val = ImageFont.truetype(self.font1, 34)
        font_small = ImageFont.truetype(self.font1, 22)
        bio_font = ImageFont.truetype(self.font1, 22)

        g_rank = (
            f"#{levelling_instance.get_user_global_rank}"
            if levelling_instance.get_user_global_rank
            else "N/A"
        )
        s_rank = (
            f"#{levelling_instance.get_member_server_rank}"
            if levelling_instance.get_member_server_rank
            else "N/A"
        )

        self._draw_stat_card(
            draw,
            50,
            590,
            255,
            120,
            labels["g_rank"],
            g_rank,
            theme_color,
            font_header,
            font_val,
        )
        self._draw_stat_card(
            draw,
            322,
            590,
            255,
            120,
            labels["s_rank"],
            s_rank,
            theme_color,
            font_header,
            font_val,
        )

        qp_text = self.format_number(currency_instance.get_balance)
        self._draw_stat_card(
            draw,
            594,
            590,
            256,
            120,
            labels["bal"],
            qp_text,
            theme_color,
            font_header,
            font_val,
        )
        qp_icon = Image.open(self.badges["qp"]).resize((36, 36))
        final_canvas.paste(qp_icon, (804, 603), qp_icon)

        # Global level bar
        g_level = levelling_instance.get_user_level
        g_xp_cur = levelling_instance.get_user_xp
        g_prev_xp = self.calculate_level_xp(g_level - 1) if g_level > 0 else 0
        g_next_xp = self.calculate_level_xp(g_level)
        g_needed = g_next_xp - g_prev_xp
        g_progress = g_xp_cur - g_prev_xp
        g_percent = (g_progress / g_needed * 100) if g_needed > 0 else 0

        draw.text(
            (50, 735),
            f"{labels['g_lvl']} {g_level}",
            fill=theme_color,
            font=font_header,
        )
        draw.text(
            (850, 735),
            f"{self.format_number(g_xp_cur)} / {self.format_number(g_next_xp)} XP",
            fill=(220, 222, 232),
            font=font_small,
            anchor="ra",
        )
        self.draw_progress_bar(draw, 50, 772, 800, 22, g_percent, theme_color)

        # Server level bar
        s_level = levelling_instance.get_member_level
        s_xp_cur = levelling_instance.get_member_xp
        s_prev_xp = self.calculate_level_xp(s_level - 1) if s_level > 0 else 0
        s_next_xp = self.calculate_level_xp(s_level)
        s_needed = s_next_xp - s_prev_xp
        s_progress = s_xp_cur - s_prev_xp
        s_percent = (s_progress / s_needed * 100) if s_needed > 0 else 0

        draw.text(
            (50, 807),
            f"{labels['s_lvl']} {s_level}",
            fill=theme_color,
            font=font_header,
        )
        draw.text(
            (850, 807),
            f"{self.format_number(s_xp_cur)} / {self.format_number(s_next_xp)} XP",
            fill=(220, 222, 232),
            font=font_small,
            anchor="ra",
        )
        self.draw_progress_bar(draw, 50, 844, 800, 22, s_percent, theme_color)

        bio_text = inventory_instance.get_bio or labels["bio"]
        if len(bio_text) > 70:
            bio_text = bio_text[:67] + "..."

        draw.rounded_rectangle(
            (270, 510, 850, 548),
            radius=12,
            fill=(17, 20, 28, 230),
            outline=theme_color,
            width=1,
        )
        draw.text((285, 518), bio_text, fill=(235, 236, 245), font=bio_font)

        final_bytes = BytesIO()
        final_canvas.save(final_bytes, "png")
        final_bytes.seek(0)
        return final_bytes

    async def get_badges(
        self, user: User, voted: bool, country: str
    ) -> list[tuple[Image.Image, int]]:
        badges = []
        x_position = 840

        if voted:
            badges.append(
                (Image.open(self.badges["vote"]).resize((50, 50)), x_position)
            )
            x_position -= 60

        grank, rrank = Levelling(user).get_user_global_rank, get_richest(user)
        if grank is not None and grank <= 100:
            rank_badge = self.get_rank_badge(grank)
            badges.append((rank_badge, x_position))
            x_position -= 60

        if rrank < 15:
            badges.append(
                (Image.open(self.badges["richest"]).resize((50, 50)), x_position)
            )
            x_position -= 60

        if country:
            country_img = os.path.join(
                os.path.dirname(__file__), "assets", "country", f"{country}.png"
            )
            if os.path.exists(country_img):
                badges.append((Image.open(country_img).resize((50, 50)), x_position))
                x_position -= 60

        if Partner.check(user):
            badges.append(
                (Image.open(self.badges["partner"]).resize((50, 50)), x_position)
            )
            x_position -= 60

        if await BetaTest(self.bot).check(user):
            badges.append(
                (Image.open(self.badges["beta"]).resize((50, 50)), x_position)
            )
            x_position -= 60

        if user.id == 597829930964877369:
            badges.append(
                (Image.open(self.badges["creator"]).resize((50, 50)), x_position)
            )
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
