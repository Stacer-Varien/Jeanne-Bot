from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
from discord.ext.commands import Bot
import requests

from functions import Levelling



class LeaderboardR:
    def __init__(self, bot: Bot):
        self.font1 = os.path.join(os.path.dirname(__file__), "assets", "font.ttf")
        self.font2 = os.path.join(os.path.dirname(__file__), "assets", "font2.ttf")
        self.bot = bot

    async def generate_leaderboard_global(self):
        leaderboard = Levelling().get_global_rank()
        font_normal = ImageFont.truetype(self.font1, 14)
        font_small = ImageFont.truetype(self.font2, 10)
        STROKE = (151, 151, 151)

        canvas = Image.new(mode="RGBA", size=(200, (100 * len(leaderboard))))
        draw = ImageDraw.Draw(canvas)
        r = 0
        for i in leaderboard:
            r += 1
            user = await self.bot.fetch_user(int(i[0]))
            profile_bytes = BytesIO(requests.get(user.display_avatar.with_format("png")).content)
            profile = Image.open(profile_bytes).convert("RGBA").resize((40, 40), resample=Image.LANCZOS)
            profile_pic_holder = Image.new("RGBA", canvas.size, (255, 255, 255, 0))

            yadd = 10 + (100 * r)
            mask_cor=50, yadd, 90, 40 + yadd
            mask = Image.new("RGBA", canvas.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse(mask_cor, fill=(255, 25, 255, 255))

            if r == 1:
                COLOR = (255, 215, 0)
            elif r == 2:
                COLOR = (192, 192, 192)
            elif r == 3:
                COLOR = (205, 133, 63)
            else:
                COLOR = (70, 130, 180)

            
            draw.rounded_rectangle((10, (10 + yadd), 190, (90 + yadd)), 1, None)
            draw.text((15, (20 + yadd)), f"#{r}", COLOR, font=font_normal, stroke_fill=STROKE, stroke_width=1)
            draw.text((100, (30 + yadd)), str(user), COLOR, font=font_small, stroke_fill=STROKE, stroke_width=1)

            profile_pic_holder.paste(profile, mask_cor)

            pre = Image.composite(profile_pic_holder, canvas, mask)
            blank = Image.new("RGBA", pre.size, 0)

            final = Image.alpha_composite(pre, blank)
        final_bytes=BytesIO()
        final.save(final_bytes, "png")
        final_bytes.seek(0)
        return final_bytes

    def generate_leaderboard_server(self, server:str):
        leaderboard = Levelling(int(server)).get_server_rank()

        font_normal = ImageFont.truetype(self.font1, 14)
        font_small = ImageFont.truetype(self.font2, 10)

        canvas = Image.new(mode="RGBA", size=(200, (100 * len(leaderboard))))
        draw = ImageDraw.Draw(canvas)
        r = 1
        for i in leaderboard:
            r += 1
            user = self.bot.get_user(int(i[0]))
            profile_bytes = requests.get(user.avatar.with_format("png")).content
            profile = Image.open(profile_bytes)
            profile = profile.convert("RGBA").resize((40, 40), resample=Image.LANCZOS)
            profile_pic_holder = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
            mask = Image.new("RGBA", canvas.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            yadd = 10**10 * (r - 1)
            mask_draw.ellipse(
                (50, (10 + yadd), 90, (60 + yadd)), fill=(255, 25, 255, 255)
            )

            STROKE = (151, 151, 151)

            if r == 1:
                COLOR = (255, 215, 0)
            elif r == 2:
                COLOR = (192, 192, 192)
            elif r == 3:
                COLOR = (205, 133, 63)
            else:
                COLOR = (70, 130, 180)

            
            draw.rounded_rectangle((10, (10 + yadd), 190, (90 + yadd)), 1, None)
            draw.text((15, (20 + yadd)), f"#{r}", COLOR, font=font_normal, stroke_fill=STROKE, stroke_width=1)
            draw.text((100, (30 + yadd)), str(user), COLOR, font=font_small, stroke_fill=STROKE, stroke_width=1)

            profile_pic_holder.paste(profile, (50, (10 + yadd), 90, (60 + yadd)))
        
        pre = Image.composite(profile_pic_holder, canvas, mask)
        blank = Image.new("RGBA", pre.size, (255, 255, 255, 0))

        final = Image.alpha_composite(pre, blank)
        final.save(final, "png")
        final.seek(0)
        return bytes(final)