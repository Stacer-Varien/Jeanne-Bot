from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,  
)
from discord import Color, Embed, Interaction, app_commands as Jeanne
from discord.ext.commands import GroupCog, Bot
from assets.images import (
    get_jeanne_pic,
    get_kistune_pic,
    get_medusa_pic,
    get_morgan_pic,
    get_neko_pic,
    get_saber_pic,
    get_wallpaper_pic,
    safebooru_pic,
)


class images(GroupCog, name="image"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Get a kitsune image")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def kitsune(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_kistune_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Need a wallpaper for your PC or phone?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def wallpaper(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_wallpaper_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get a Jeanne d'Arc image")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def jeanne(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_jeanne_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get a Saber image")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def saber(self, ctx: Interaction):
        await ctx.response.defer()
        file, embed = get_saber_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get a neko image")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def neko(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_neko_pic()
        await ctx.followup.send(file=file, embed=embed)

    @Jeanne.command(description="Get a Morgan le Fay (Fate) image")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def morgan(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_morgan_pic()
        await ctx.followup.send(file=file, embed=embed)

    @Jeanne.command(description="Get a Medusa (Fate) image")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def medusa(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_medusa_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get an image from Safebooru")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)  
    async def safebooru(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_image(url=safebooru_pic())
        embed.set_footer(text="Fetched from Safebooru • Credits must go to the artist")
        await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(images(bot))
