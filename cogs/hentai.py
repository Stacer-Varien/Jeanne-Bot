from json import loads
from nextcord import *
from nextcord import slash_command as jeanne_slash
from glob import glob
from nextcord.ext.commands import Cog
from random import choice
from requests import get
from nextcord.ext.application_checks import *
from config import db




class slashnsfw(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get a random hentai from Jeanne")
    @is_nsfw()
    async def hentai(self, ctx: Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:

            gelbooru_api = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub"
            response = get(gelbooru_api)
            ret = loads(response.text)
            gelbooru_image = choice(ret['post'])["file_url"] 

            yandere_image = choice(get("https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub").json())['file_url']

            konachan_image = choice(get("https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub").json())['file_url']

            h=[gelbooru_image, yandere_image, konachan_image]

            hentai=choice(h)

            if hentai == gelbooru_image:
                source='Gelbooru'

            elif hentai == yandere_image:
                source='Yande.re'

            elif hentai == konachan_image:
                source='Konachan'

            embed = Embed(color=0xFFC0CB).set_image(url=hentai).set_footer(text="Fetched from {}".format(source))
            await ctx.followup.send(embed=embed)            

            
            

    @jeanne_slash(description="Get a random hentai from Gelbooru")
    @is_nsfw()
    async def gelbooru(self, ctx: Interaction, tag=SlashOption(description="Add a tag for something specific", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            if tag == None:
                gelbooru_api = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub"
            else:
                gelbooru_api = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub" + tag
            
            response = get(gelbooru_api)
            ret = loads(response.text)
            image = choice(ret['post'])["file_url"]

            embed = Embed(color=0xFFC0CB).set_image(
                url=image).set_footer(text="Fetched from Gelbooru")
            await ctx.followup.send(embed=embed)


    @jeanne_slash(description="Get a random hentai from Yande.re")
    @is_nsfw()
    async def yandere(self, ctx: Interaction, tag=SlashOption(description="Add a tag for something specific", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
                try:
                    if tag == None:
                        yandere_api = choice(get(
                            "https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub").json())

                    elif tag == "02":
                        await ctx.followup.send("Tag has been blacklisted due to it returning extreme content and guro")

                    else:
                        yandere_api = choice(get(
                            f"https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub" + tag).json())

                    yandere = Embed(color=0xFFC0CB)
                    yandere.set_image(url=yandere_api['file_url'])
                    yandere.set_footer(text="Fetched from Yande.re")
                    await ctx.followup.send(embed=yandere)
                except IndexError:
                    pass

    @jeanne_slash(description="Get a random hentai from Konachan")
    @is_nsfw()
    async def konachan(self, ctx: Interaction, tag=SlashOption(description="Add a tag for something specific", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
                try:
                    if tag == None:
                        konachan_api = choice(get(
                            "https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub").json())

                    else:
                        konachan_api = choice(get(
                            f"https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub+{tag}").json())

                    konachan = Embed(color=0xFFC0CB)
                    konachan.set_image(url=konachan_api['file_url'])
                    konachan.set_footer(text="Fetched from Konachan")
                    await ctx.followup.send(embed=konachan)
                except IndexError:
                    pass

    @Cog.listener()
    async def on_application_command_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationNSFWChannelRequired):
            no_hentai = Embed(
                title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
            no_hentai.add_field(
                name="Reason", value=ApplicationNSFWChannelRequired(ctx.channel))
            await ctx.send(embed=no_hentai)

def setup(bot):
    bot.add_cog(slashnsfw(bot))
