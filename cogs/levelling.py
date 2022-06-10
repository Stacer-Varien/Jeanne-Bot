from asyncio import get_event_loop
from functools import partial
from nextcord.ext.commands import Cog, CooldownMapping, BucketType
from nextcord import *
from nextcord import slash_command as jeanne_slash
from config import db
from typing import Optional
from assets.levelcard.generator import Generator

class levelling(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = CooldownMapping.from_cooldown(1, 120, BucketType.member)

    def get_ratelimit(self, message: Message) -> Optional[int]:
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    def get_card(self, args):
        image = Generator().generate_profile(**args)
        return image

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
         ratelimit = self.get_ratelimit(message)
         if ratelimit is None:
            if not message.author.bot: 
                cursor1 = db.execute("INSERT OR IGNORE INTO serverxpData (guild_id, user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?,?)", (
                    message.guild.id, message.author.id, 0, 5, 5))

                cursor2 = db.execute(
                    "INSERT OR IGNORE INTO globalxpData (user_id, lvl, exp, cumulative_exp) VALUES (?,?,?,?)", (message.author.id, 0, 5, 5))
                xp = 5
                if cursor1.rowcount == 0:
                        scurrent_exp_query = db.execute(
                        f"SELECT exp, cumulative_exp, lvl FROM serverxpData WHERE user_id = {message.author.id}")
                        scurrent_exp_data = scurrent_exp_query.fetchone()
                        scurrent_exp = scurrent_exp_data[0]
                        scurrent_cumulative_exp = scurrent_exp_data[1]
                        scurrent_lvl = scurrent_exp_data[2]

                        supdated_exp = scurrent_exp + xp
                        supdated_cumulative_exp = scurrent_cumulative_exp + xp
                        snext_lvl_exp = ((scurrent_lvl * 50) +
                                         ((scurrent_lvl - 1) * 25) + 50)

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
                        gnext_lvl_exp = ((gcurrent_lvl * 50) +
                                         ((gcurrent_lvl - 1) * 25) + 50)

                        if gupdated_cumulative_exp >= gnext_lvl_exp:
                            gupdated_exp = gupdated_cumulative_exp - gnext_lvl_exp
                            db.execute(
                                f"UPDATE globalxpData SET lvl = lvl + 1, exp = {gupdated_exp} WHERE user_id = {message.author.id}")

                        db.execute(
                            f"UPDATE globalxpDATA SET exp = {gupdated_exp}, cumulative_exp = {gupdated_cumulative_exp} WHERE user_id = {message.author.id}")

                db.commit()
            await self.bot.process_commands(message)

    @jeanne_slash(description="See your level or someone else's level")
    async def level(self, ctx: Interaction, member: Member = SlashOption(description="Which member?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            if member is None:
                    member = ctx.user
            try:
                squery = db.execute(
                    f"SELECT * FROM serverxpData where guild_id = {ctx.guild.id} AND user_id = {member.id}")
                squery_data = squery.fetchone()
                slvl = squery_data[2]
                sexp = squery_data[3]

                gquery = db.execute(
                    f"SELECT * FROM globalxpData where user_id = {member.id}")
                gquery_data = gquery.fetchone()
                glvl = gquery_data[1]
                gexp = gquery_data[2]


                args = {
                    'bg_image': '',
 			            'profile_image': str(member.avatar.with_format('png')),
 			            'server_level': slvl,
 			            'server_user_xp': sexp,
 			            'server_next_xp': ((slvl * 50) + ((slvl - 1) * 25) + 50),
                        'global_level': glvl,
 			            'global_user_xp': gexp,
 			            'global_next_xp': ((glvl * 50) + ((glvl - 1) * 25) + 50),
 			            'user_name': str(member),
                        }

                func = partial(self.get_card, args)
                image = await get_event_loop().run_in_executor(None, func)

                file = File(fp=image, filename=f'{member.name}_level_card.png')
                await ctx.followup.send(file=file)
            except:
                no_exp = Embed(description="Failed to get level stats")
                await ctx.followup.send(embed=no_exp)


    @jeanne_slash(description="Check the users with the most XP in the server")
    async def rank(self, ctx: Interaction, type=SlashOption(description="Server or Global specific?", choices=["server", "global"])):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            if type == "server":

                leaders_query = db.execute(
                    f"SELECT user_id FROM serverxpData WHERE guild_id = {ctx.guild.id} ORDER BY cumulative_exp DESC LIMIT 0,15"
                )

                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                r = 1
                for i in leaders_query:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await ctx.followup.send(embed=embed)

                

            elif type == "global":
                leaders_query = db.execute(
                    f"SELECT user_id FROM globalxpData ORDER BY cumulative_exp DESC LIMIT 0,15"
                )


                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                r = 1
                for i in leaders_query:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await ctx.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(levelling(bot))
