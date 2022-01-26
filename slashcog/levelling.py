from sqlite3 import connect
from nextcord.ext.commands import Cog
from nextcord import slash_command as jeanne_slash, Embed, Interaction, Member, SlashOption

db = connect("expData.db")

class levelling(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            cursor = db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?,?)",
                                        (message.guild.id, message.author.id, 0, 5, 5))

            if cursor.rowcount == 0:
                current_exp_query = db.execute(
                    f"SELECT exp, cumulative_exp, lvl FROM guildData WHERE user_id = {message.author.id}")
                current_exp_data = current_exp_query.fetchone()
                current_exp = current_exp_data[0]
                current_cumulative_exp = current_exp_data[1]
                current_lvl = current_exp_data[2]

                xp = 5
                updated_exp = current_exp + xp
                updated_cumulative_exp = current_cumulative_exp + xp
                next_lvl_exp=(current_lvl * 100) + ((current_lvl - 1) * 10)

                if updated_cumulative_exp >= next_lvl_exp:
                    updated_exp = updated_cumulative_exp - next_lvl_exp
                    db.execute(f"UPDATE guildData SET lvl = lvl + 1, exp = {updated_exp} WHERE guild_id = ? AND user_id = ?",
                                        (message.guild.id, message.author.id))

                db.execute(f"UPDATE guildData SET exp = {updated_exp}, cumulative_exp =? WHERE guild_id = ? AND user_id = ?",
                                    (updated_cumulative_exp, message.guild.id, message.author.id))

            db.commit()

        await self.bot.process_commands(message)

    @jeanne_slash(description="See your level or someone else's level")
    async def level(self, interaction: Interaction, member: Member = SlashOption(required=None)):
        if member is None:
            member = interaction.user
        try:
            lvl_query = db.execute(f"SELECT lvl FROM guildData where user_id = {member.id}")
            lvl_data = lvl_query.fetchone()
            lvl = lvl_data[0]

            exp_query = db.execute(f"SELECT exp FROM guildData WHERE user_id = {member.id}")
            exp_data = exp_query.fetchone()
            exp = exp_data[0]

            embed = Embed(title=f"{member}'s level stats", color=0x008000)
            blue_box = int(round((exp / 100) * 10))
            white_box = 10 - blue_box
            embed.add_field(name="**Level**", value=f"Level {lvl}", inline=True)
            embed.add_field(name="**Experience**", value=f"{exp}XP", inline=True)
            embed.add_field(name="**Progress**", value=f"**>** {blue_box * ':blue_square:' + white_box * ':white_large_square:'} **<**", inline=False)
            await interaction.response.send_message(embed=embed)
        except:
            no_exp=Embed(description="Failed to get level stats")
            await interaction.response.send_message(embed=no_exp)



    @jeanne_slash(description="Check the top 10 users in the server")
    async def rank(self, interactions:Interaction):
        leaders_query = db.execute(
            f"SELECT user_id FROM guildData WHERE guild_id = {interactions.guild.id} ORDER BY cumulative_exp DESC LIMIT 10"
        )

        embed = Embed(color=0xFFD700)
        embed.set_author(name="Leaderboard: TOP 10")
        embed.description = ""

        r = 1
        for i in leaders_query:
            p = await self.bot.fetch_user(i[0])
            embed.description += f"**{r}**. {p}\n\n"
            r += 1

        await interactions.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(levelling(bot))            

