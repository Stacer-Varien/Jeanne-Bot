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
        """Calculates the cumulative XP required to reach the END of the given level."""
        return (level * 50) + ((level - 1) * 25) + 50

    @staticmethod
    def draw_progress_bar(
        draw: ImageDraw,
        x: int,
        y: int,
        width: int,
        height: int,
        percent: float,
        color: tuple,
        bg_color: tuple = (50, 50, 50),
    ):
        """Draws a modern progress bar with a background track."""
        # Draw background track
        draw.rounded_rectangle(
            (x, y, x + width, y + height), radius=height // 2, fill=bg_color
        )

        # Calculate fill width (clamped between 0 and 100%)
        safe_percent = max(0.0, min(100.0, percent))
        fill_width = int(width * (safe_percent / 100))

        # Draw fill
        if fill_width > 0:
            draw.rounded_rectangle(
                (x, y, x + fill_width, y + height), radius=height // 2, fill=color
            )

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
        # Initialize Data
        inventory_instance = Inventory(user)
        currency_instance = Currency(user)

        # Safety check for DM contexts
        guild = user.guild if isinstance(user, Member) else None
        levelling_instance = Levelling(user, guild)

        # --- 1. Background Setup ---
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

        # --- 2. Canvas Setup ---
        canvas_color = (32, 32, 32)
        final_canvas = Image.new("RGBA", (900, 900), canvas_color)
        final_canvas.paste(card_bg, (0, 0))
        draw = ImageDraw.Draw(final_canvas)

        # Theme Color
        font_color_hex = inventory_instance.get_color
        theme_color = (
            tuple(ImageColor.getcolor(font_color_hex, "RGB"))
            if font_color_hex
            else (204, 204, 255)
        )

        # --- 3. Profile Picture ---
        avatar_url = user.display_avatar.url
        avatar_data = await self.fetch_image(avatar_url)
        if not avatar_data:
            avatar_data = await self.fetch_image(user.default_avatar.url)

        profile_img = Image.open(avatar_data).convert("RGBA")
        profile_img = profile_img.resize((180, 180), resample=Image.Resampling.LANCZOS)

        mask = Image.new("L", (180, 180), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 180, 180), fill=255)

        pfp_x, pfp_y = 50, 410
        draw.ellipse(
            (pfp_x - 5, pfp_y - 5, pfp_x + 185, pfp_y + 185), fill=canvas_color
        )
        draw.ellipse(
            (pfp_x - 2, pfp_y - 2, pfp_x + 182, pfp_y + 182),
            outline=theme_color,
            width=3,
        )
        final_canvas.paste(profile_img, (pfp_x, pfp_y), mask)

        # Username with dynamic font size adjustment
        name_font_size = 55
        name_font = ImageFont.truetype(self.font1, name_font_size)
        username_width = draw.textlength(str(user), font=name_font)
        max_width = 500  # Maximum width before shrinking

        while username_width > max_width:
            name_font_size -= 2
            name_font = ImageFont.truetype(self.font1, name_font_size)
            username_width = draw.textlength(str(user), font=name_font)

        draw.text(
            (250, 425), str(user), fill=(0, 0, 0, 180), font=name_font, stroke_width=1
        )
        draw.text((250, 425), str(user), fill=theme_color, font=name_font)

        # Badges
        badges_list = await self.get_badges(user, voted, country)
        for badge, x_pos in badges_list:
            self.enhance_and_paste(badge, (x_pos, 430), final_canvas)

        # --- 4. Stats & Progress Bars ---
        # Adjusted Y coordinates to prevent overlap
        stats_y = 610
        g_bar_y = 700
        s_bar_y = 770
        bio_y = 840
        col_margin = 50

        # Localization
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

        font_header = ImageFont.truetype(self.font1, 32)
        font_val = ImageFont.truetype(self.font1, 40)
        font_small = ImageFont.truetype(self.font1, 24)

        # Row 1: Ranks & Balance
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

        self._draw_stat_box(
            draw,
            col_margin,
            stats_y,
            labels["g_rank"],
            g_rank,
            theme_color,
            font_header,
            font_val,
        )
        self._draw_stat_box(
            draw,
            col_margin + 270,
            stats_y,
            labels["s_rank"],
            s_rank,
            theme_color,
            font_header,
            font_val,
        )

        # Balance
        qp_icon = Image.open(self.badges["qp"]).resize((40, 40))
        final_canvas.paste(qp_icon, (820, stats_y + 10), qp_icon)
        draw.text(
            (810, stats_y),
            labels["bal"],
            fill=theme_color,
            font=font_header,
            anchor="ra",
        )
        draw.text(
            (810, stats_y + 35),
            self.format_number(currency_instance.get_balance),
            fill=(255, 255, 255),
            font=font_val,
            anchor="ra",
        )

        # Row 2: Global Level Bar
        g_level = levelling_instance.get_user_level
        g_xp_cur = levelling_instance.get_user_xp

        # Calculate thresholds
        g_prev_xp = self.calculate_level_xp(g_level - 1) if g_level > 0 else 0
        g_next_xp = self.calculate_level_xp(g_level)

        # Progress Calculation
        g_needed = g_next_xp - g_prev_xp
        g_progress = g_xp_cur - g_prev_xp
        g_percent = (g_progress / g_needed * 100) if g_needed > 0 else 0

        draw.text(
            (col_margin, g_bar_y),
            f"{labels['g_lvl']} {g_level}",
            fill=theme_color,
            font=font_header,
        )
        draw.text(
            (860, g_bar_y),
            f"{self.format_number(g_xp_cur)} / {self.format_number(g_next_xp)} XP",
            fill=(200, 200, 200),
            font=font_small,
            anchor="ra",
        )
        self.draw_progress_bar(
            draw, col_margin, g_bar_y + 40, 810, 20, g_percent, theme_color
        )

        # Row 3: Server Level Bar
        s_level = levelling_instance.get_member_level
        s_xp_cur = levelling_instance.get_member_xp

        s_prev_xp = self.calculate_level_xp(s_level - 1) if s_level > 0 else 0
        s_next_xp = self.calculate_level_xp(s_level)

        s_needed = s_next_xp - s_prev_xp
        s_progress = s_xp_cur - s_prev_xp
        s_percent = (s_progress / s_needed * 100) if s_needed > 0 else 0

        draw.text(
            (col_margin, s_bar_y),
            f"{labels['s_lvl']} {s_level}",
            fill=theme_color,
            font=font_header,
        )
        draw.text(
            (860, s_bar_y),
            f"{self.format_number(s_xp_cur)} / {self.format_number(s_next_xp)} XP",
            fill=(200, 200, 200),
            font=font_small,
            anchor="ra",
        )
        self.draw_progress_bar(
            draw, col_margin, s_bar_y + 40, 810, 20, s_percent, theme_color
        )

        # Row 4: Bio
        bio_text = inventory_instance.get_bio or labels["bio"]
        draw.rounded_rectangle(
            (40, bio_y, 860, bio_y + 50),
            radius=10,
            fill=(45, 45, 45),
            outline=theme_color,
            width=1,
        )

        bio_font = ImageFont.truetype(self.font1, 22)
        if len(bio_text) > 75:
            bio_text = bio_text[:72] + "..."
        draw.text((55, bio_y + 12), bio_text, fill=(230, 230, 230), font=bio_font)

        final_bytes = BytesIO()
        final_canvas.save(final_bytes, "png")
        final_bytes.seek(0)
        return final_bytes

    def _draw_stat_box(self, draw, x, y, label, value, color, font_label, font_value):
        draw.text((x, y), label, fill=color, font=font_label)
        draw.text((x, y + 35), value, fill=(255, 255, 255), font=font_value)

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
