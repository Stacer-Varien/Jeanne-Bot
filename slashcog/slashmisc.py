from nextcord import Embed, Interaction, slash_command as jeanne_slash, SlashOption
from nextcord.ext.commands import Cog
from nextcord.ui import Button, View
from nextcord import Embed, ButtonStyle
from assets.errormsgs import admin_perm

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

class slashmisc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash()
    async def invite(self, interaction : Interaction):
        invite = Embed(
            title="Invite me!",
            description="Click on one of these buttons to invite me to you server or join my creator's server",
            color=0x00bfff)

        await interaction.response.send_message(embed=invite, view=invite_button)

    @jeanne_slash(description="Type something and I will say it")
    async def say(self, interaction : Interaction, type=SlashOption(description="Plain text or Embed", choices=["Plain text", "Embed"], required=True), text=SlashOption(required=True)):
        if interaction.permissions.administrator is True:
            if type == "Plain text":
                await interaction.response.send_message(text)
            if type == "Embed":
                say = Embed(description=f"{text}", color=0xADD8E6)
                await interaction.response.send_message(embed=say)
        else:
            await interaction.response.send_message(embed=admin_perm)


    @jeanne_slash()
    async def report(self, interaction : Interaction, report):
        await interaction.response.send_message("Your report has been sent and will be dealt with. Please note that the cooldown is 1 hour to avoid troll reports.", ephemeral=True)
        print(report)

def setup(bot):
    bot.add_cog(slashmisc(bot))
