from io import BytesIO
from typing import Literal, Optional
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
import os
from discord import Guild
from discord.ext.commands import Bot
import requests

from functions import Levelling


class Leaderboard:
    def __init__(self, bot: Bot, server: Optional[Guild] = None):
        self.background = os.path.join(
            os.path.dirname(__file__), "assets", "leaderboard.png"
        )
        self.font1 = os.path.join(os.path.dirname(__file__), "assets", "font.ttf")
        self.font2 = os.path.join(os.path.dirname(__file__), "assets", "font2.ttf")
        self.bot = bot
        self.server = server

    async def generate_leaderboard(self, type: Literal["Global", "Server"]):
        if type == "Server":
            leaderboard = Levelling(self.server).get_server_rank()
        elif type == "Global":
            leaderboard = Levelling().get_global_rank()

        font_normal = ImageFont.truetype(self.font1, 14)
        font_small = ImageFont.truetype(self.font2, 10)

        canvas = Image.new(mode="RGBA", size=(200, (100 * len(leaderboard))))
        r = 1
        for i in leaderboard:
            r += 1
            user = await self.bot.fetch_user(int(i[0]))
            profile_bytes = BytesIO(requests.get(user.avatar.with_format('png')).content)
            profile = Image.open(profile_bytes)
            profile = profile.convert("RGBA").resize((40, 40), resample=Image.LANCZOS)
            profile_pic_holder = Image.new("RGBA", canvas.size, (255, 255, 255, 0))            
            mask = Image.new("RGBA", canvas.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((50,90), fill=(255, 25, 255, 255))

                 
            yrr = 10 + (100 * (r - 1))
            yt = (100 * (r - 1))
            yu1 = (100 * (r - 1))
            
            if r == 1:
                COLOR = (255, 215, 0)
            elif r == 2:
                COLOR = (192, 192, 192)
            elif r == 3:
                COLOR = (205, 133, 63)
            else:
                COLOR = (70, 130, 180)

            draw=ImageDraw.Draw(canvas)
            draw.rounded_rectangle((10, yrr, 190, yrr), 1, None)
            draw.ellipse((50,yt,90,yt))
            draw.text((15, yt), f"#{r}", COLOR, font_normal)
            draw.text((100,yu1), str(user), COLOR, font_small)

