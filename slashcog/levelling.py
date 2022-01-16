from nextcord import SlashOption, Member, slash_command as jeanne_slash, Interaction, Embed
from nextcord.ext.commands import Cog
from json import load, dump


async def update_data(users, user, guild):
    if not str(guild.id) in users:
        users[str(guild.id)] = {}
        if not str(user.id) in users[str(guild.id)]:
            users[str(guild.id)][str(user.id)] = {}
            users[str(guild.id)][str(user.id)]['experience'] = 0
            users[str(guild.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(guild.id)]:
        users[str(guild.id)][str(user.id)] = {}
        users[str(guild.id)][str(user.id)]['experience'] = 0
        users[str(guild.id)][str(user.id)]['level'] = 1


async def add_experience(users, user, exp):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp


async def level_up(users, user):
  experience = users[str(user.guild.id)][str(user.id)]['experience']
  lvl_start = users[str(user.guild.id)][str(user.id)]['level']
  lvl_end = int(experience ** (1/4))

  if lvl_start < lvl_end:
      users[str(user.guild.id)][str(user.id)]['level'] = lvl_end

class levelling(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = load(f)

        await update_data(users, member, member.guild)

        with open('users.json', 'w') as f:
            dump(users, f)


    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open('level.json', 'r') as f:
                    users = load(f)
            await update_data(users, message.author, message.guild)
            await add_experience(users, message.author, 5)
            await level_up(users, message.author)

            with open('level.json', 'w') as f:
                dump(users, f)

    @jeanne_slash(description="See your level or someone else's level")
    async def level(self, interaction:Interaction, member: Member = SlashOption(required=False)):
        guild=interaction.guild
        if member==None:
            member = interaction.user
                    
        with open('level.json','r') as f:
            users = load(f)
        lvl = users[str(guild.id)][str(interaction.user.id)]['level']
        exp = users[str(guild.id)][str(interaction.user.id)]['experience']
        boxes = int((exp/(100*((1/2) * lvl)))*10)

        embed=Embed(title=f"{member}'s Level Stats", color=0x00FF00)
        embed.add_field(name="XP", value=f"{exp}/{int(100*((1/2)*lvl))}", inline=True)
        embed.add_field(name="Level", value=f"Level {lvl}")
        embed.add_field(name="Progress Bar", value=boxes * ":blue_square:" + (
            10-boxes) * ":white_large_square:", inline=False)
        embed.set_thumbnail(url=member.display_avatar)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(levelling(bot))            

