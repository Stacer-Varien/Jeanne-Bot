from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import math
import os


class Generator:
    def __init__(self):
        self.default_bg = os.path.join(os.path.dirname(__file__), 'assets', 'card.png')
        self.font1      = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')
        self.font2      = os.path.join(os.path.dirname(__file__), 'assets', 'font2.ttf')

    def generate_profile(self, bg_image: str = None, profile_image: str = None, server_level: int = 0, server_current_xp: int = 0, server_user_xp: int = 0, server_next_xp: int = 0, global_level: int = 0, global_current_xp: int = 0, global_user_xp: int = 0, global_next_xp: int = 0, user_name: str = 'Varien#1956'):
        if not bg_image:
            card = Image.open(self.default_bg).convert("RGBA")
        else:
            bg_bytes = BytesIO(requests.get(bg_image).content)
            card = Image.open(bg_bytes).convert("RGBA")

            width, height = card.size
            if width == 900 and height == 500:
                pass
            else:
                x1 = 0
                y1 = 0
                x2 = width
                nh = math.ceil(width * 0.264444)
                y2 = 0

                if nh < height:
                    y1 = (height / 2) - 119
                    y2 = nh + y1

                card = card.crop((x1, y1, x2, y2)).resize((900, 500))

        profile_bytes = BytesIO(requests.get(profile_image).content)
        profile = Image.open(profile_bytes)
        profile = profile.convert('RGBA').resize((180, 180))

        profile_pic_holder = Image.new(
            "RGBA", card.size, (255, 255, 255, 0)
        )

        mask = Image.new("RGBA", card.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            (29, 29, 209, 209), fill=(255, 25, 255, 255)
        )

        # ======== Fonts to use =============
        font_normal = ImageFont.truetype(self.font1, 40)
        font_small = ImageFont.truetype(self.font1, 30)

        # ======== Colors ========================
        DARK = (204, 204, 255)

        def get_str(xp):
            if xp < 1000:
                return str(xp)
            if xp >= 1000 and xp < 1000000:
                return str(round(xp / 1000, 1)) + "k"
            if xp > 1000000:
                return str(round(xp / 1000000, 1)) + "M"

        draw = ImageDraw.Draw(card)
        draw.text((245, 22), user_name, DARK, font=font_normal)
        draw.text((245, 98), f"Server Level: {server_level}", DARK, font=font_small)
        draw.text(
            (500, 98),
            f"Server XP: {get_str(server_user_xp)}/{get_str(server_next_xp)}",
            DARK,
            font=font_small,
        )

        blank = Image.new("RGBA", card.size, (255, 255, 255, 0))
        blank_draw = ImageDraw.Draw(blank)
        blank_draw.rectangle(
            (245, 155, 710, 165), fill=(255, 255, 255, 0), outline=DARK
        )

        server_xpneed = server_next_xp - server_current_xp
        server_xphave = server_user_xp - server_current_xp

        server_current_percentage = (server_xphave / server_xpneed) * 100
        server_length_of_bar = (server_current_percentage * 4.9) + 208

        blank_draw.rectangle((248, 158, server_length_of_bar, 162), fill=DARK)        
        blank_draw.ellipse((20, 20, 218, 218), fill=(255, 255, 255, 0), outline=DARK)

########################################################################################

        draw.text((245, 208), f"Global Level: {global_level}", DARK, font=font_small)
        draw.text(
            (500, 208),
            f"Global XP: {get_str(global_user_xp)}/{get_str(global_next_xp)}",
            DARK,
            font=font_small,
        )

        blank_draw.rectangle(
            (245, 265, 710, 275), fill=(255, 255, 255, 0), outline=DARK
        )

        global_xpneed = global_next_xp - global_current_xp
        global_xphave = global_user_xp - global_current_xp

        global_current_percentage = (global_xphave / global_xpneed) * 100
        global_length_of_bar = (global_current_percentage * 4.9) + 208

        blank_draw.rectangle((248, 268, global_length_of_bar, 272), fill=DARK)

        profile_pic_holder.paste(profile, (29, 29, 209, 209))

        pre = Image.composite(profile_pic_holder, card, mask)
        pre = Image.alpha_composite(pre, blank)

        blank = Image.new("RGBA", pre.size, (255, 255, 255, 0))

        final = Image.alpha_composite(pre, blank)
        final_bytes = BytesIO()
        final.save(final_bytes, 'png')
        final_bytes.seek(0)
        return final_bytes