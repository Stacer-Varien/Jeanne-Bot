from dataclasses import dataclass
from io import BytesIO
import os
from typing import Literal

import aiohttp
from discord import Interaction, Member, User
from discord.ext.commands import Bot
from PIL import Image, ImageColor, ImageDraw, ImageEnhance, ImageFont

from functions import BetaTest, Currency, Inventory, Levelling, Partner, get_richest


@dataclass(frozen=True)
class MediaInfo:
    animated: bool
    format: str
    size: tuple[int, int]
    byte_size: int


class Profile:
    MAX_SOURCE_BYTES = 25 * 1024 * 1024
    MAX_ANIMATION_FRAMES = 12
    DEFAULT_UPLOAD_LIMIT = 10 * 1024 * 1024

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
    def output_extension(image: BytesIO) -> str:
        return "gif" if image.getbuffer()[:3] == b"GIF" else "png"

    @staticmethod
    def enhance_and_paste(
        image: Image.Image, position: tuple[int, int], card: Image.Image
    ):
        enhanced_image = ImageEnhance.Brightness(image).enhance(1.1)
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
    def draw_progress_bar(
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        width: int,
        height: int,
        percent: float,
        color: tuple,
        bg_color: tuple = (50, 50, 50),
    ):
        draw.rounded_rectangle(
            (x, y, x + width, y + height), radius=height // 2, fill=bg_color
        )
        fill_width = int(width * (max(0.0, min(100.0, percent)) / 100))
        if fill_width > 0:
            draw.rounded_rectangle(
                (x, y, x + fill_width, y + height), radius=height // 2, fill=color
            )

    async def fetch_image(
        self, url: str, max_bytes: int | None = None
    ) -> BytesIO | Literal[False]:
        limit = min(max_bytes or self.MAX_SOURCE_BYTES, self.MAX_SOURCE_BYTES)
        headers = {"User-Agent": "Mozilla/5.0"}
        timeout = aiohttp.ClientTimeout(total=30)
        try:
            async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return False
                    content_length = response.content_length
                    if content_length is not None and content_length > limit:
                        return False
                    data = bytearray()
                    async for chunk in response.content.iter_chunked(64 * 1024):
                        data.extend(chunk)
                        if len(data) > limit:
                            return False
                    return BytesIO(data)
        except (aiohttp.ClientError, TimeoutError):
            return False

    async def inspect_image(
        self, url: str, max_bytes: int | None = None
    ) -> MediaInfo | None:
        data = await self.fetch_image(url, max_bytes)
        if not data:
            return None
        try:
            with Image.open(data) as image:
                image.verify()
            data.seek(0)
            with Image.open(data) as image:
                return MediaInfo(
                    animated=bool(getattr(image, "is_animated", False)),
                    format=image.format or "unknown",
                    size=image.size,
                    byte_size=len(data.getbuffer()),
                )
        except (OSError, ValueError):
            return None

    @staticmethod
    def _extract_frames(
        image: Image.Image,
        size: tuple[int, int],
        brightness: float = 1.0,
        animate: bool = False,
    ) -> tuple[list[Image.Image], list[int]]:
        frame_count = image.n_frames if animate and image.is_animated else 1
        step = max(1, frame_count // Profile.MAX_ANIMATION_FRAMES)
        indexes = list(range(0, frame_count, step))[: Profile.MAX_ANIMATION_FRAMES]
        frames = []
        durations = []
        for index in indexes:
            image.seek(index)
            frame = image.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            if brightness != 1.0:
                frame = ImageEnhance.Brightness(frame).enhance(brightness)
            frames.append(frame)
            durations.append(max(80, min(250, int(image.info.get("duration", 120)))))
        return frames, durations

    async def generate_profile(
        self,
        ctx: Interaction,
        user: User | Member,
        bg_image: str = None,
        preview: bool = False,
        voted: bool = False,
        country: str = None,
    ) -> BytesIO | Literal[False]:
        del preview
        inventory = Inventory(user)
        currency = Currency(user)
        guild = user.guild if isinstance(user, Member) else None
        levelling = Levelling(user, guild)
        upload_limit = getattr(ctx, "filesize_limit", self.DEFAULT_UPLOAD_LIMIT)
        source_limit = min(upload_limit, self.MAX_SOURCE_BYTES)

        if bg_image:
            bg_data = await self.fetch_image(bg_image, source_limit)
        else:
            bg_data = None
        if bg_data:
            background = Image.open(bg_data)
        else:
            background = Image.open(self.default_bg)

        animated_unlocked = inventory.animated_profile_unlocked
        bg_animated = animated_unlocked and bool(
            getattr(background, "is_animated", False)
        )
        bg_frames, bg_durations = self._extract_frames(
            background,
            (900, 500),
            float(inventory.get_brightness) / 100,
            bg_animated,
        )

        avatar_asset = user.display_avatar
        if animated_unlocked and avatar_asset.is_animated():
            avatar_asset = avatar_asset.with_format("gif")
        avatar_data = await self.fetch_image(avatar_asset.url, source_limit)
        if not avatar_data:
            avatar_data = await self.fetch_image(user.default_avatar.url, source_limit)
        if not avatar_data:
            return False
        avatar = Image.open(avatar_data)
        avatar_animated = animated_unlocked and bool(
            getattr(avatar, "is_animated", False)
        )
        avatar_frames, avatar_durations = self._extract_frames(
            avatar, (180, 180), animate=avatar_animated
        )

        badges = await self.get_badges(user, voted, country)
        frame_count = max(len(bg_frames), len(avatar_frames))
        frames = [
            self._render_frame(
                ctx,
                user,
                bg_frames[index % len(bg_frames)],
                avatar_frames[index % len(avatar_frames)],
                badges,
                inventory,
                currency,
                levelling,
            )
            for index in range(frame_count)
        ]

        if frame_count > 1:
            durations = (
                bg_durations if len(bg_frames) > 1 else avatar_durations
            )
            animated = self._save_gif(frames, durations, upload_limit)
            if animated:
                return animated
        return self._save_png(frames[0])

    def _render_frame(
        self,
        ctx: Interaction,
        user: User | Member,
        card_bg: Image.Image,
        profile_img: Image.Image,
        badges: list[tuple[Image.Image, int]],
        inventory: Inventory,
        currency: Currency,
        levelling: Levelling,
    ) -> Image.Image:
        canvas_color = (32, 32, 32)
        canvas = Image.new("RGBA", (900, 900), canvas_color)
        canvas.paste(card_bg, (0, 0))
        draw = ImageDraw.Draw(canvas)
        font_color_hex = inventory.get_color
        theme_color = (
            tuple(ImageColor.getcolor(font_color_hex, "RGB"))
            if font_color_hex
            else (204, 204, 255)
        )

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
        canvas.paste(profile_img, (pfp_x, pfp_y), mask)

        name_font_size = 55
        name_font = ImageFont.truetype(self.font1, name_font_size)
        while draw.textlength(str(user), font=name_font) > 500:
            name_font_size -= 2
            name_font = ImageFont.truetype(self.font1, name_font_size)
        draw.text(
            (250, 425), str(user), fill=(0, 0, 0, 180), font=name_font, stroke_width=1
        )
        draw.text((250, 425), str(user), fill=theme_color, font=name_font)
        for badge, x_pos in badges:
            self.enhance_and_paste(badge, (x_pos, 430), canvas)

        labels = self._labels(ctx)
        font_header = ImageFont.truetype(self.font1, 32)
        font_value = ImageFont.truetype(self.font1, 40)
        font_small = ImageFont.truetype(self.font1, 24)
        stats_y, global_y, server_y, bio_y = 610, 700, 770, 840

        global_rank = levelling.get_user_global_rank
        try:
            server_rank = levelling.get_member_server_rank
            server_level = levelling.get_member_level
            server_xp = levelling.get_member_xp
        except AttributeError:
            server_rank = None
            server_level = 0
            server_xp = 0
        self._draw_stat_box(
            draw,
            50,
            stats_y,
            labels["g_rank"],
            f"#{global_rank}" if global_rank else "N/A",
            theme_color,
            font_header,
            font_value,
        )
        self._draw_stat_box(
            draw,
            320,
            stats_y,
            labels["s_rank"],
            f"#{server_rank}" if server_rank else "N/A",
            theme_color,
            font_header,
            font_value,
        )

        qp_icon = Image.open(self.badges["qp"]).resize((40, 40))
        canvas.paste(qp_icon, (820, stats_y + 10), qp_icon)
        draw.text(
            (810, stats_y), labels["bal"], fill=theme_color, font=font_header, anchor="ra"
        )
        draw.text(
            (810, stats_y + 35),
            self.format_number(currency.get_balance),
            fill=(255, 255, 255),
            font=font_value,
            anchor="ra",
        )

        self._draw_level_bar(
            draw,
            global_y,
            labels["g_lvl"],
            levelling.get_user_level,
            levelling.get_user_xp,
            theme_color,
            font_header,
            font_small,
        )
        self._draw_level_bar(
            draw,
            server_y,
            labels["s_lvl"],
            server_level,
            server_xp,
            theme_color,
            font_header,
            font_small,
        )

        draw.rounded_rectangle(
            (40, bio_y, 860, bio_y + 50),
            radius=10,
            fill=(45, 45, 45),
            outline=theme_color,
            width=1,
        )
        bio_text = inventory.get_bio or labels["bio"]
        if len(bio_text) > 75:
            bio_text = bio_text[:72] + "..."
        draw.text(
            (55, bio_y + 12),
            bio_text,
            fill=(230, 230, 230),
            font=ImageFont.truetype(self.font1, 22),
        )
        return canvas

    def _draw_level_bar(
        self,
        draw: ImageDraw.ImageDraw,
        y: int,
        label: str,
        level: int,
        current_xp: int,
        color: tuple,
        font_header: ImageFont.FreeTypeFont,
        font_small: ImageFont.FreeTypeFont,
    ) -> None:
        previous_xp = self.calculate_level_xp(level - 1) if level > 0 else 0
        next_xp = self.calculate_level_xp(level)
        needed = next_xp - previous_xp
        percent = ((current_xp - previous_xp) / needed * 100) if needed > 0 else 0
        draw.text((50, y), f"{label} {level}", fill=color, font=font_header)
        draw.text(
            (860, y),
            f"{self.format_number(current_xp)} / {self.format_number(next_xp)} XP",
            fill=(200, 200, 200),
            font=font_small,
            anchor="ra",
        )
        self.draw_progress_bar(draw, 50, y + 40, 810, 20, percent, color)

    @staticmethod
    def _labels(ctx: Interaction) -> dict[str, str]:
        if ctx.locale and ctx.locale.value == "fr":
            return {
                "g_rank": "Classement Global",
                "s_rank": "Classement Serveur",
                "bal": "Solde QP",
                "g_lvl": "Niveau Global",
                "s_lvl": "Niveau Serveur",
                "bio": "Aucune bio disponible",
            }
        if ctx.locale and ctx.locale.value == "de":
            return {
                "g_rank": "Globaler Rang",
                "s_rank": "Serverrang",
                "bal": "QP-Guthaben",
                "g_lvl": "Globales Level",
                "s_lvl": "Serverlevel",
                "bio": "Keine Bio verfügbar",
            }
        return {
            "g_rank": "Global Rank",
            "s_rank": "Server Rank",
            "bal": "QP Balance",
            "g_lvl": "Global Level",
            "s_lvl": "Server Level",
            "bio": "No bio available",
        }

    @staticmethod
    def _save_png(frame: Image.Image) -> BytesIO:
        output = BytesIO()
        frame.save(output, "PNG", optimize=True)
        output.seek(0)
        return output

    @staticmethod
    def _save_gif(
        frames: list[Image.Image], durations: list[int], upload_limit: int
    ) -> BytesIO | None:
        working_frames = frames
        working_durations = durations
        while len(working_frames) > 1:
            output = BytesIO()
            palette_frames = [
                frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)
                for frame in working_frames
            ]
            palette_frames[0].save(
                output,
                "GIF",
                save_all=True,
                append_images=palette_frames[1:],
                duration=[
                    working_durations[index % len(working_durations)]
                    for index in range(len(working_frames))
                ],
                loop=0,
                optimize=True,
                disposal=2,
            )
            if len(output.getbuffer()) <= upload_limit:
                output.seek(0)
                return output
            working_frames = working_frames[::2]
            working_durations = working_durations[::2]
        return None

    @staticmethod
    def _draw_stat_box(
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        label: str,
        value: str,
        color: tuple,
        font_label: ImageFont.FreeTypeFont,
        font_value: ImageFont.FreeTypeFont,
    ):
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
        global_rank, richest_rank = Levelling(user).get_user_global_rank, get_richest(
            user
        )
        if global_rank is not None and global_rank <= 100:
            badges.append((self.get_rank_badge(global_rank), x_position))
            x_position -= 60
        if richest_rank < 15:
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
