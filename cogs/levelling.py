from asyncio import get_event_loop
from functools import partial
from nextcord.ext.commands import Cog, CooldownMapping, BucketType
from nextcord import *
from nextcord import slash_command as jeanne_slash
from assets.db_functions import add_level, add_xp, check_botbanned_user, get_global_rank, get_member_level, get_member_xp, get_server_rank, get_used_wallpaper, get_user_level, get_user_xp
from typing import Optional
from assets.levelcard.generator import Generator
from cooldowns import *

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
        check = check_botbanned_user(message.author.id)
        if check == message.author.id:
            pass
        else:
            ratelimit = self.get_ratelimit(message)
            if ratelimit is None:
                if not message.author.bot:
                    try: 
                        add_xp(message.author.id, message.guild.id)
                        add_level(message.author.id, message.guild.id)
                    except:
                        pass 
        await self.bot.process_commands(message)

    @jeanne_slash(description="See your level or someone else's level")
    @cooldown(1, 60, bucket=SlashBucket.author)
    async def level(self, ctx: Interaction, member: Member = SlashOption(description="Which member?", required=False)):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            if member is None:
                    member = ctx.user
            try:
                slvl = get_member_level(member.id, ctx.guild.id)
                sexp = get_member_xp(member.id, ctx.guild.id)

                glvl = get_user_level(member.id)
                gexp = get_user_xp(member.id)

                bg = get_used_wallpaper(ctx.user.id)

                args = {
                        'bg_image': bg,
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
    @cooldown(1, 60, bucket=SlashBucket.author)
    async def rank(self, ctx: Interaction, type=SlashOption(description="Server or Global specific?", choices=["server", "global"])):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            if type == "server":

                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                leaderboard=get_server_rank(ctx.guild.id)

                r = 1
                for i in leaderboard:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await ctx.followup.send(embed=embed)
            
            elif type == "global":
                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                leaderboard = get_global_rank()

                r = 1
                for i in leaderboard:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await ctx.followup.send(embed=embed)




def setup(bot):
    bot.add_cog(levelling(bot))
