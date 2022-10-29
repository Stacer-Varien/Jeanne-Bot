from asyncio import get_event_loop
from functools import partial
from discord.ext.commands import Cog, CooldownMapping, BucketType, Bot, hybrid_command, hybrid_group, Context, cooldown
from discord import *
from db_functions import add_level, add_xp, check_botbanned_user, get_global_rank, get_member_level, get_member_xp, get_server_rank, selected_wallpaper, get_user_level, get_user_xp
from typing import Optional, Literal
from assets.generators.level_card import Level

class levelling(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self._cd = CooldownMapping.from_cooldown(1, 120, BucketType.member)

    def get_ratelimit(self, message: Message) -> Optional[int]:
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    def get_card(self, args):
        image = Level().generate_level(**args)
        return image

    @Cog.listener()
    async def on_message(self, message:Message):
        if check_botbanned_user(message.author.id) == True:
            pass
        else:
            await self.bot.process_commands(message)
            ratelimit = self.get_ratelimit(message)
            if ratelimit is None:
                if not message.author.bot:
                    try: 
                        add_xp(message.author.id, message.guild.id)
                        add_level(message.author.id, message.guild.id)
                    except:
                        pass 
        

    @hybrid_command(description="See your level or someone else's level")
    @cooldown(1, 60, type=BucketType.user)
    async def level(self, ctx: Context, member: Optional[Member] = None)->None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if member == None:
                member = ctx.author
            try:
                slvl = get_member_level(member.id, ctx.guild.id)
                sexp = get_member_xp(member.id, ctx.guild.id)

                glvl = get_user_level(member.id)
                gexp = get_user_xp(member.id)

                bg = selected_wallpaper(member.id)

                args = {
                        'level_card': bg,
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
                await ctx.send(file=file)
            except:
                no_exp = Embed(description="Failed to get level stats")
                await ctx.send(embed=no_exp)


    @hybrid_group(description="Check the users with the most XP in the server")
    @cooldown(1, 60, type=BucketType.user)
    async def rank(self, ctx: Context, type:Optional[Literal["server", "global"]]=None)->None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:

            if type == "server" or None:

                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                leaderboard=get_server_rank(ctx.guild.id)

                r = 1
                for i in leaderboard:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await ctx.send(embed=embed)
            
            elif type == "global":
                embed = Embed(color=0xFFD700)
                embed.set_author(name="XP Leaderboard")

                leaderboard = get_global_rank()

                r = 1
                for i in leaderboard:
                    p = await self.bot.fetch_user(i[0])
                    embed.add_field(name="_ _", value=f"**{r}**. {p}")
                    r += 1

                await ctx.send(embed=embed)

async def setup(bot:Bot):
    await bot.add_cog(levelling(bot))
