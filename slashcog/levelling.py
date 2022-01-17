import imp
from nextcord import SlashOption, Member, slash_command as jeanne_slash, Interaction, Embed
from nextcord.ext.commands import Cog
from json import load, dump
from asyncio import sleep



class levelling(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = load(f)

        await self.update_data(users, member)

        with open('users.json', 'w') as f:
            dump(users, f)


    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            with open('users.json', 'r') as f:
                users = load(f)

            await self.update_data(users, message.author)
            await self.add_experience(users, message.author, 5)
            await self.level_up(users, message.author)

            with open('users.json', 'w') as f:
                dump(users, f)



    async def update_data(self, users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 1


    async def add_experience(self, users, user, exp):
        users[f'{user.id}']['experience'] += exp
        await sleep(60)


    async def level_up(self, users, user):
        with open('levels.json', 'r') as g:
            levels = load(g)
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            users[f'{user.id}']['level'] = lvl_end

    @jeanne_slash(description="See your level or someone else's level")
    async def level(self, interaction: Interaction, member: Member = SlashOption(required=False)):

        if not member:
            member = interaction.user
        
        member_id=member.id
        with open('users.json','r') as f:
                users = load(f)
        lvl = users[str(member_id)]['level']
        exp = users[str(member_id)]['experience']

        boxes = int((exp/(100*((1/2) * lvl)))*10)

        embed = Embed(title=f"{member}'s Level Stats", color=0x00FF00)
        embed.add_field(
            name="XP", value=f"{exp}/{int(100*((1/2)*lvl))}", inline=True)
        embed.add_field(name="Level", value=f"Level {lvl}")
        embed.add_field(name="Progress Bar", value=boxes * ":blue_square:" + (
            10-boxes) * ":white_large_square:", inline=False)
        embed.set_thumbnail(url=member.display_avatar)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(levelling(bot))            

