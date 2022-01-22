<<<<<<< Updated upstream
from nextcord.ext.commands import Cog
from nextcord import Game, Embed, Activity, ActivityType, slash_command as jeanne_slash, Interaction, SlashOption
from assets.needed import test_server, bot_owner, test_server
from assets.errormsgs import owner_only
from os import execv
from sys import executable, argv

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

def restart_bot():
  execv(executable, ['python'] + argv)

class slashowner(Cog):
    def __init__(self, bot):
        self.bot = bot


    @jeanne_slash(description="Changes the bot's play activity")
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
    async def mutuals(self, interaction : Interaction, user_id=SlashOption(required=None)):
        if interaction.user==self.bot.get_user(bot_owner):
            
            if user_id == None:
                user_id=self.bot.user.id

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

    @jeanne_slash(description="Restart me to be updated")
    async def update(self, interaction):
        await interaction.response.send_message(f"YAY! NEW UPDATE!")
        restart_bot()

def setup(bot):
    bot.add_cog(slashowner(bot))
=======
from random import choices
from nextcord.ext.commands import Cog
from nextcord import Game, Embed, Activity, ActivityType, slash_command as jeanne_slash, Interaction, SlashOption
from assets.needed import test_server, bot_owner, test_server
from assets.errormsgs import owner_only
from os import execv
from sys import executable, argv

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

def restart_bot():
  execv(executable, ['python'] + argv)

class slashowner(Cog):
    def __init__(self, bot):
        self.bot = bot


    @jeanne_slash(description="Changes the bot's play activity")
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
    async def mutuals(self, interaction : Interaction, user_id=SlashOption(required=None)):
        if interaction.user==self.bot.get_user(bot_owner):
            
            if user_id == None:
                user_id=self.bot.user.id

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

    @jeanne_slash(description="Restart me to be updated")
    async def update(self, interaction):
        if interaction.user == self.bot.get_user(bot_owner):
            await interaction.response.send_message(f"YAY! NEW UPDATE!")
            restart_bot()
        else:
            await interaction.response.send_message(embed=owner_only)

    @jeanne_slash(description="Reloads a cog")
    async def reload(self, interaction:Interaction, cog=SlashOption(choices=["Levelling", "Fun", "Help", "Images", "Info", "Manages","Misc", "Owner", "Reaction", "Utilities"])):
        if interaction.user == self.bot.get_user(bot_owner):
            try:
                self.bot.unload_extension(f'slashcog.{cog}.py')
                self.bot.load_extension(f'slashcog.{cog}.py')
                await interaction.response.send_message("Cog reloaded", ephemeral=True)
            except:
                await interaction.response.send_message("Failed to load cog. Restart the bot", ephemeral=True)
        else:
            await interaction.response.send_message(embed=owner_only)

def setup(bot):
    bot.add_cog(slashowner(bot))
>>>>>>> Stashed changes
