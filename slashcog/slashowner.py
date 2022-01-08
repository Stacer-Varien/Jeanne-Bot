from nextcord.ext.commands import Cog, is_owner
from nextcord import Game, Embed, Activity, ActivityType, slash_command as jeanne_slash, Interaction, SlashOption
from assets.needed import test_server, bot_owner
from assets.errormsgs import owner_only

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

class slashowner(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="See where which servers Jeanne is in (CREATOR ONLY)")
    async def botmutuals(self, interaction : Interaction):
        if interaction.user==self.bot.get_user(bot_owner):
            mutuals = [str(x) for x in self.bot.guilds]
            botmutuals = f"____\nMutuals: {len(self.bot.guilds)}\nServers: {' ,'.join(mutuals)}\n______"
            print(botmutuals)
            await interaction.response.send_message("`Check console log for bot's mutuals`", ephemeral=True)
        else:
            await interaction.response.send_message(embed=owner_only)


    @jeanne_slash(description="Changes the bot's play activity", guild_ids=[test_server])
    async def activity(self, interaction : Interaction, activitytype=SlashOption(description="Choose an activity type", choices=['listen', 'play'], required=True), activity=SlashOption(description="What is the new activity")):
        if interaction.user==self.bot.get_user(bot_owner):                
            if activitytype=="listen":
                await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
                await interaction.response.send_message(f"Bot's activity changed to `listening to {activity}`")
            elif activitytype=="play":
                await self.bot.change_presence(activity=Game(name=activity))
                await interaction.response.send_message(f"Bot's activity changed to `playing {activity}`")
        else:
            await interaction.response.send_message(embed=owner_only)                
            

    @jeanne_slash(description="Get mutuals of a user")
    async def mutuals(self, interaction : Interaction, user_id):
        if interaction.user==self.bot.get_user(bot_owner):
            user=await self.bot.fetch_user(user_id)
            mutuals = f"______\nName: {user}\nMutuals: {len(user.mutual_guilds)}\nServers: {user.mutual_guilds}\n______"
            print(mutuals)
            await interaction.response.send_message(f"`Check console log for {user.name}'s mutuals`", ephemeral=True)
        else:
            await interaction.response.send_message(embed=owner_only)        



    @jeanne_slash(description="Finds a user")
    async def finduser(self, interaction : Interaction, user_id):
        if interaction.user==self.bot.get_user(bot_owner):
            user = await self.bot.fetch_user(user_id)
            if user.bot == True:
                botr = ":o:"
            else:
                botr = ":x:"
            fuser = Embed(title="User Found", color=0xccff33)
            fuser.add_field(name="User Information",
                            value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}\n**>** **Creation Date:** {user.created_at.strftime(format)}\n**>** **Mutuals:** {len(user.mutual_guilds)}\n**>** **Is Bot?:** {botr}",
                            inline=True)
            fuser.set_image(url=user.display_avatar)
            await interaction.response.send_message(embed=fuser)
        else:
            await interaction.response.send_message(embed=owner_only)             

def setup(bot):
    bot.add_cog(slashowner(bot))
