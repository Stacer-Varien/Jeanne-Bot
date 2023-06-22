from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
import requests
import math
import os


class Level:
    def __init__(self):
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.default_bg = os.path.join(assets_dir, "card.png")
        self.font1 = os.path.join(assets_dir, "font.ttf")
        self.font2 = os.path.join(assets_dir, "font2.ttf")

    def generate_level(
        self,
        bg_image=None,
        profile_image=None,
        font_color=None,
        server_level=None,
        server_current_xp=0,
        server_user_xp=None,
        server_next_xp=None,
        global_level=None,
        global_current_xp=0,
        global_user_xp=None,
        global_next_xp=None,
        user_name=None,
        brightness=None,
    ):
        if not bg_image:
            card = Image.open(self.default_bg).convert("RGBA")
        else:
            bg_bytes = BytesIO(requests.get(bg_image).content)
            card = Image.open(bg_bytes).convert("RGBA")

        brightness = brightness or 100
        card = ImageEnhance.Brightness(card).enhance(brightness / 100)

        width, height = card.size
        if width != 900 or height != 500:
            x1 = 0
            y1 = 0
            x2 = width
            nh = math.ceil(width * 0.528888)
            y2 = 0

            if nh < height:
                y2 = nh + y1

            card = card.crop((x1, y1, x2, y2)).resize((900, 500), resample=Image.LANCZOS)

        profile_bytes = BytesIO(requests.get(profile_image).content)
        profile = Image.open(profile_bytes).convert("RGBA").resize((180, 180), resample=Image.LANCZOS)

        profile_pic_holder = Image.new("RGBA", card.size, (255, 255, 255, 0))
        mask = Image.new("RGBA", card.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((29, 29, 209, 209), fill=(255, 25, 255, 255))

        font_normal = ImageFont.truetype(self.font1, 40)
        font_small = ImageFont.truetype(self.font1, 30)

        COLOR = ImageColor.getcolor(("#" + font_color), "RGB") if font_color else (204, 204, 255)
        STROKE = (151, 151, 151)

        def get_str(xp):
            if xp < 1000:
                return str(xp)
            if 1000 <= xp < 1000000:
                return str(round(xp / 1000, 1)) + "k"
            if xp >= 1000000:
                return str(round(xp / 1000000, 1)) + "M"

        draw = ImageDraw.Draw(card)
        draw.text((20, 240), user_name, COLOR, font=font_normal, stroke_fill=STROKE, stroke_width=1)
        draw.text((20, 310), f"Server Level: {server_level}", COLOR, font=font_small, stroke_width=1, stroke_fill=STROKE)
        draw.text((280, 310), f"Server XP: {get_str(server_user_xp)}/{get_str(server_next_xp)}", COLOR, font=font_small, stroke_width=1, stroke_fill=STROKE)

        blank = Image.new("RGBA", card.size, (255, 255, 255, 0))
        blank_draw = ImageDraw.Draw(blank)
        blank_draw.rectangle((25, 375, 520, 385), fill=(255, 255, 255, 0), outline=COLOR)

        server_xpneed = server_next_xp - server_current_xp
        server_xphave = server_user_xp - server_current_xp

        server_current_percentage = (server_xphave / server_xpneed) * 100
        server_length_of_bar = (server_current_percentage * 4.9) + 28

        blank_draw.rectangle((28, 378, server_length_of_bar, 382), fill=COLOR)
        blank_draw.ellipse((29, 29, 209, 209), fill=(255, 255, 255, 0), outline=COLOR)

        draw.text((20, 420), f"Global Level: {global_level}", COLOR, font=font_small, stroke_width=1, stroke_fill=STROKE)
        draw.text((280, 420), f"Global XP: {get_str(global_user_xp)}/{get_str(global_next_xp)}", COLOR, font=font_small, stroke_width=1, stroke_fill=STROKE)

        blank_draw.rectangle((25, 470, 520, 480), fill=(255, 255, 255, 0), outline=COLOR)

        global_xpneed = global_next_xp - global_current_xp
        global_xphave = global_user_xp - global_current_xp

        global_current_percentage = (global_xphave / global_xpneed) * 100
        global_length_of_bar = (global_current_percentage * 4.9) + 28

        blank_draw.rectangle((28, 473, global_length_of_bar, 477), fill=COLOR)

        profile_pic_holder.paste(profile, (29, 29, 209, 209))

        pre = Image.composite(profile_pic_holder, card, mask)
        pre = Image.alpha_composite(pre, blank)

        blank = Image.new("RGBA", pre.size, (255, 255, 255, 0))

        final = Image.alpha_composite(pre, blank)
        final_bytes = BytesIO()
        final.save(final_bytes, "png")
        final_bytes.seek(0)
        return final_bytes
