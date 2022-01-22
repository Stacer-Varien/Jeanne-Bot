<<<<<<< Updated upstream
import imp
from nextcord import SlashOption, Member, slash_command as jeanne_slash, Interaction, Embed
from nextcord.ext.commands import Cog
from json import load, dump

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
        
        try:
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

        except KeyError:
            noxp = Embed(description="Member has no XP")
            await interaction.response.send_message(embed=noxp)


def setup(bot):
    bot.add_cog(levelling(bot))            

=======
from math import sqrt
from aiosqlite import connect
from nextcord.ext.commands import Cog
from nextcord import slash_command as jeanne_slash, Embed, Interaction, Member, SlashOption, Colour


class levelling(Cog):
    def __init__(self, bot):
        self.bot = bot
        

    async def initialize(self):
        await self.bot.wait_until_ready()
        db = await connect("expData.db")
        await db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")

    @Cog.listener()
    async def on_message(self, message):
        db = await connect("expData.db")
        multiplier=5
        if not message.author.bot:
            cursor = await db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 5))

            if cursor.rowcount == 0:
                await db.execute("UPDATE guildData SET exp = exp + 5 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                cur = await db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                data = await cur.fetchone()
                exp = data[0]
                lvl = sqrt(exp) / multiplier

                if lvl.is_integer():
                    pass

            await db.commit()

        await self.bot.process_commands(message)

    @jeanne_slash(description="See your level or someone else's level")
    async def level(self, interaction: Interaction, member: Member = SlashOption(required=None)):
        db = await connect("expData.db")
        multiplier=5
        if member is None:
            member = interaction.user

        # get user exp
        async with db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id)) as cursor:
            data = await cursor.fetchone()
            exp = data[0]

            # calculate rank
        async with db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (interaction.guild.id,)) as cursor:
            rank = 1
            async for value in cursor:
                if exp < value[0]:
                    rank += 1

        lvl = int(sqrt(exp)//multiplier)
        next_lvl_exp = (multiplier*((lvl+1)))**2
        lvl_percent= (exp / next_lvl_exp)*100

        embed = Embed(
            title=f"Stats for {member.name}")
        embed.add_field(name="Level", value=str(lvl))
        embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
        embed.add_field(name="Rank", value=f"{rank}/{interaction.guild.member_count}")
        embed.add_field(name="Level Progress", value=f"{round(lvl_percent, 2)}%")
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(levelling(bot))            

>>>>>>> Stashed changes
