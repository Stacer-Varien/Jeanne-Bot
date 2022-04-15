from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as jeanne_slash
from random import randrange
from config import db

class levelling(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {message.author.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if message.author.id == botbanned_user.id:
                pass
        except:
            if not message.author.bot:
                cursor1 = db.execute("INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?,?)", (
                    message.guild.id, message.author.id, 0, 5, 5))

                cursor2 = db.execute(
                    "INSERT OR IGNORE INTO globalxpData (user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?)", (message.author.id, 0, 5, 5))

                xp = randrange(5, 10)
                if cursor1.rowcount == 0:
                    scurrent_exp_query = db.execute(
                        f"SELECT exp, cumulative_exp, lvl FROM serverxpData WHERE user_id = {message.author.id}")
                    scurrent_exp_data = scurrent_exp_query.fetchone()
                    scurrent_exp = scurrent_exp_data[0]
                    scurrent_cumulative_exp = scurrent_exp_data[1]
                    scurrent_lvl = scurrent_exp_data[2]

                    supdated_exp = scurrent_exp + xp
                    supdated_cumulative_exp = scurrent_cumulative_exp + xp
                    snext_lvl_exp = ((scurrent_lvl * 100) +
                                     ((scurrent_lvl - 1) * 50) + 100)

                    if supdated_cumulative_exp >= snext_lvl_exp:
                        supdated_exp = supdated_cumulative_exp - snext_lvl_exp
                        db.execute(
                            f"UPDATE serverxpData SET lvl = lvl + 1, exp = {supdated_exp} WHERE guild_id = {message.guild.id} AND user_id = {message.author.id}")

                    db.execute(
                        f"UPDATE serverxpData SET exp = {supdated_exp}, cumulative_exp = {supdated_cumulative_exp} WHERE guild_id = {message.guild.id} AND user_id = {message.author.id}")

                db.commit()

                if cursor2.rowcount == 0:
                    gcurrent_exp_query = db.execute(
                        f"SELECT exp, cumulative_exp, lvl FROM globalxpData WHERE user_id = {message.author.id}")
                    gcurrent_exp_data = gcurrent_exp_query.fetchone()
                    gcurrent_exp = gcurrent_exp_data[0]
                    gcurrent_cumulative_exp = gcurrent_exp_data[1]
                    gcurrent_lvl = gcurrent_exp_data[2]

                    gupdated_exp = gcurrent_exp + xp
                    gupdated_cumulative_exp = gcurrent_cumulative_exp + xp
                    gnext_lvl_exp = ((gcurrent_lvl * 100) +
                                     ((gcurrent_lvl - 1) * 50) + 100)

                    if gupdated_cumulative_exp >= gnext_lvl_exp:
                        gupdated_exp = gupdated_cumulative_exp - gnext_lvl_exp
                        db.execute(
                            f"UPDATE globalxpData SET lvl = lvl + 1, exp = {gupdated_exp} WHERE user_id = {message.author.id}")

                    db.execute(
                        f"UPDATE globalxpDATA SET exp = {gupdated_exp}, cumulative_exp = {gupdated_cumulative_exp} WHERE user_id = {message.author.id}")

                db.commit()

            await self.bot.process_commands(message)

    @jeanne_slash(description="See your level or someone else's level")
    async def level(self, interaction: Interaction, member: Member = SlashOption(description="Which member?", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member is None:
                member = interaction.user
            try:
                query1 = db.execute(
                    f"SELECT * FROM serverxpData where guild_id = {interaction.guild.id} AND user_id = {member.id}")
                query1_data = query1.fetchone()
                slvl = query1_data[2]
                sexp = query1_data[3]

                s_next_lvl_exp = ((slvl * 100) + ((slvl - 1) * 50) + 100)

                blue_box = int(round((sexp / s_next_lvl_exp) * 10))
                swhite_box = 10 - blue_box

                query2 = db.execute(
                    f"SELECT lvl FROM globalxpData where user_id = {member.id}")
                query2_data = query2.fetchone()
                glvl = query2_data[0]

                gexp_query = db.execute(
                    f"SELECT exp FROM globalxpData WHERE user_id = {member.id}")
                gexp_data = gexp_query.fetchone()
                gexp = gexp_data[0]

                g_next_lvl_exp = ((glvl * 100) + ((glvl - 1) * 50) + 100)

                red_box = int(round((gexp / g_next_lvl_exp) * 10))
                gwhite_box = 10 - red_box

                embed = Embed(title=f"{member}'s level stats", color=0x008000)
                embed.add_field(name="**__Server__**",
                                value=f"\n**>** **Level:** {slvl}\n**>** **Experience:** {sexp}\{s_next_lvl_exp}XP\n**>** **Experience to Next Level:** {s_next_lvl_exp - sexp}XP", inline=True)
                embed.add_field(name="**__Global__**",
                                value=f"\n**>** **Level:** {glvl}\n**>** **Experience:** {gexp}\{g_next_lvl_exp}XP\n**>** **Experience to Next Level:** {g_next_lvl_exp - gexp}XP", inline=True)
                embed.add_field(
                    name="**__Progress__**", value=f"**>** **Server:** {blue_box * ':blue_square:' + swhite_box * ':white_large_square:'}\n**>** **Global:** {red_box * ':red_square:' + gwhite_box * ':white_large_square:'}", inline=False)
                await interaction.followup.send(embed=embed)
            except:
                no_exp = Embed(description="Failed to get level stats")
                await interaction.followup.send(embed=no_exp)

    @jeanne_slash(description="Check the users with the most XP in the server")
    async def rank(self, interaction: Interaction, type=SlashOption(description="Server or Global specific?", choices=["server", "global"])):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if type == "server":

                leaders_query = db.execute(
                    f"SELECT user_id FROM serverxpData WHERE guild_id = {interaction.guild.id} ORDER BY cumulative_exp DESC LIMIT 15"
                )

                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                r = 1
                for i in leaders_query:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await interaction.followup.send(embed=embed)

                

            elif type == "global":
                leaders_query = db.execute(
                    f"SELECT user_id FROM globalxpData ORDER BY cumulative_exp DESC LIMIT 15"
                )


                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                r = 1
                for i in leaders_query:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(levelling(bot))
