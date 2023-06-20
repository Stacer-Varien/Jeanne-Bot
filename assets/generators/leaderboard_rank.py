from io import BytesIO
from typing import Literal, Optional
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
import os
from discord import Guild
from discord.ext.commands import Bot

from functions import Levelling

class Leaderboard:
    def __init__(self, bot:Bot, server:Optional[Guild]=None):
        self.background = os.path.join(os.path.dirname(__file__), "assets", "leaderboard.png")
        self.font1 = os.path.join(os.path.dirname(__file__), "assets", "font.ttf")
        self.font2 = os.path.join(os.path.dirname(__file__), "assets", "font2.ttf")
        self.bot=bot
        self.server=server
    
    async def generate_leaderboard(self, type:Literal["Global", "Server"]):
        canvas = Image.new(mode="RGBA", size=(60,900))
        
        #x1=9, y1=9, x2=49, y2=49

        if type=="Server":
            leaderboard=Levelling(self.server).get_server_rank()
        elif type=="Global":
            leaderboard=Levelling().get_global_rank()

        r,y1,y2=1,40,5
        for i in leaderboard:
            user= await self.bot.fetch_user(int(i[0]))
            avatar=user.display_avatar
            

            

