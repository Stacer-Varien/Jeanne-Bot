from nextcord import Embed
from nextcord.ext.commands import command as jeanne, Cog, has_permissions as perms, BucketType
from nextcord.ext.commands.core import cooldown
from nextcord.ui import Button, View
from nextcord import Embed, ButtonStyle

class invite_button(View):
    def __init__(self):
        super().__init__()

        bot_invite_url="https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands"

        topgg_invite="https://top.gg/bot/831993597166747679"

        discordbots_url="https://discord.bots.gg/bots/831993597166747679"

        haze_url="https://discord.gg/VVxGUmqQhF"

        self.add_item(Button(style=ButtonStyle.url, label="Bot Invite", url=bot_invite_url))
        self.add_item(Button(style=ButtonStyle.url, label="Top.gg", url=topgg_invite))
        self.add_item(Button(style=ButtonStyle.url, label="DiscordBots", url=discordbots_url))
        self.add_item(Button(style=ButtonStyle.url, label="HAZE", url=haze_url))

class misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne()
    async def invite(self, ctx):
        invite = Embed(
            title="Invite me!",
            description="Click on one of these buttons to invite me to you server or join my creator's server",
            color=0x00bfff)

        await ctx.send(embed=invite, view=invite_button)

    @jeanne()
    @perms(administrator=True)
    async def say(self, ctx, *, text):
        message = ctx.message
        await message.delete()
        await ctx.send(text)

    @jeanne(name='saye')
    @perms(administrator=True)
    async def sayembed(self, ctx, *, text):
        message = ctx.message
        say = Embed(description=f"{text}", color=0xADD8E6)
        await message.delete()
        await ctx.send(embed=say)

    @jeanne()
    @cooldown(1, 3600, BucketType.user)
    async def report(self, ctx, *, report):
        await ctx.send("Your report has been sent and will be dealt with. Please note that the cooldown is 1 hour to avoid troll reports.")
        print(report)

def setup(bot):
    bot.add_cog(misc(bot))
