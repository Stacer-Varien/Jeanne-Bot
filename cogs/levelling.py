from asyncio import get_event_loop
from functools import partial
from discord.ext.commands import Cog, Bot, GroupCog
from discord import (
    AllowedMentions,
    Color,
    Embed,
    File,
    Interaction,
    Member,
    app_commands as Jeanne,
    Message,
)
from config import TOPGG
from functions import Botban, Command, Currency, Inventory, Levelling, get_richest
from typing import Optional
from assets.generators.profile_card import Profile
from collections import OrderedDict
from json import loads
from topgg import DBLClient


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class Rank_Group(GroupCog, name="rank"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name="global", description="Check the users with the most XP globally"
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def _global(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self._global.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name="Global XP Leaderboard")

        leaderboard = Levelling().get_global_rank

        if leaderboard == None:
            embed.description = "No global leaderboard provided"
            await ctx.followup.send(embed=embed)
            return

        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[3]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Check the users with the most XP in the server")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def server(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.server.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name="Server XP Leaderboard")

        leaderboard = Levelling(server=ctx.guild).get_server_rank

        if leaderboard == None:
            embed.description = "No server leaderboard provided"
            await ctx.followup.send(embed=embed)
            return

        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[3]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)

        await ctx.followup.send(embed=embed)


class levelling(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)
        self.profile_context = Jeanne.ContextMenu(
            name="Profile", callback=self.profile_generate
        )
        self.bot.tree.add_command(self.profile_context)
        self.profile_generate_error = self.profile_context.error(
            self.profile_generate_error
        )

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.profile_context.name, type=self.profile_context.type
        )

    @staticmethod
    def get_profile(args):
        image = Profile().generate_profile(**args)
        return image

    async def generate_profile_card(self, ctx: Interaction, member: Member):
        try:
            memdata = Levelling(member, ctx.guild)
            slvl = memdata.get_member_level
            sexp = memdata.get_member_xp

            glvl = memdata.get_user_level
            gexp = memdata.get_user_xp

            bg = Inventory(member).selected_wallpaper
            grank = memdata.get_member_global_rank
            srank = memdata.get_member_server_rank
            rrank = get_richest(member)

            bio = Inventory(member).get_bio
            font_color = Inventory(member).get_color

            voted = await self.topggpy.get_user_vote(member.id)

            args = {
                "bg_image": (bg[1] if bg else ""),
                "profile_image": str(member.avatar.with_format("png")),
                "font_color": font_color,
                "server_level": slvl,
                "server_user_xp": sexp,
                "server_next_xp": ((slvl * 50) + ((slvl - 1) * 25) + 50),
                "global_level": glvl,
                "global_user_xp": gexp,
                "global_next_xp": ((glvl * 50) + ((glvl - 1) * 25) + 50),
                "user_name": str(member),
                "grank": grank,
                "srank": srank,
                "voted": voted,
                "rrank": rrank,
                "creator": member.id,
                "partner": member.id,
                "beta": member,
                "balance": Currency(member).get_balance,
                "bio": str(bio),
                "brightness": (bg[2] if bg else 100),
            }

            func = partial(self.get_profile, args)
            image = await get_event_loop().run_in_executor(None, func)

            file = File(fp=image, filename=f"{member.name}_profile_card.png")
            await ctx.followup.send(file=file)
        except:
            no_exp = Embed(description="Failed to make profile card")
            await ctx.followup.send(embed=no_exp)

    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def profile_generate(self, ctx: Interaction, member: Member):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.profile.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        server = await self.bot.fetch_guild(740584420645535775)
        author = await server.fetch_member(ctx.user.id)
        role = server.get_role(1130430961587335219)
        try:
            if role in author.roles:
                await ctx.response.defer()
                await self.generate_profile_card(ctx, member)
        except:
            await ctx.response.send_message(
                embed=Embed(
                    description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                    color=Color.red(),
                ),
                ephemeral=True,
            )

    async def profile_generate_error(self, ctx: Interaction, error: Exception) -> None:
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.profile.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            cooldown = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Cog.listener()
    async def on_message(self, message: Message):
        if Botban(message.author).check_botbanned_user:
            return

        if not message.author.bot:
            if (
                Levelling(message.author, message.guild).check_xpblacklist_channel(
                    message.channel
                )
                == False
            ):
                try:
                    lvl = await Levelling(message.author, message.guild).add_xp()

                    if lvl == None:
                        return

                    channel, update, levelup = int(lvl[0]), str(lvl[1]), str(lvl[2])

                    def replace_all(text: str, dic: dict):
                        for i, j in dic.items():
                            text = text.replace(i, j)
                        return text

                    role_reward = message.guild.get_role(
                        Levelling(message.author, message.guild).get_role_reward
                    )
                    parameters = OrderedDict(
                        [
                            ("%member%", str(message.author)),
                            ("%pfp%", str(message.author.display_avatar)),
                            ("%server%", str(message.guild.name)),
                            ("%mention%", str(message.author.mention)),
                            ("%name%", str(message.author.name)),
                            (
                                "%newlevel%",
                                str(
                                    Levelling(
                                        message.author, message.guild
                                    ).get_member_level
                                ),
                            ),
                            (
                                "%role%",
                                str((role_reward.name if role_reward else None)),
                            ),
                            (
                                "%rolemention%",
                                str((role_reward.mention if role_reward else None)),
                            ),
                        ]
                    )
                    try:
                        await message.author.add_roles(role_reward)
                        if levelup == "0":
                            msg = "CONGRATS {}! You were role awarded {}".format(
                                message.author,
                                (role_reward.name if role_reward else None),
                            )
                            lvlup = await message.guild.fetch_channel(channel)
                            await lvlup.send(
                                msg,
                                allowed_mentions=AllowedMentions(
                                    roles=False, everyone=False, users=True
                                ),
                            )
                        elif levelup == None:
                            pass
                        else:
                            json = loads(replace_all(levelup, parameters))
                            msg = json["content"]
                            embed = Embed.from_dict(json["embeds"][0])
                            lvlup = await message.guild.fetch_channel(channel)
                            await lvlup.send(content=msg, embed=embed)
                    except:
                        if update == "0":
                            msg = "{} has leveled up to `level {}`".format(
                                message.author,
                                Levelling(
                                    message.author, message.guild
                                ).get_member_level,
                            )
                            lvlup = await message.guild.fetch_channel(channel)
                            await lvlup.send(
                                msg,
                                allowed_mentions=AllowedMentions(
                                    roles=False, everyone=False, users=True
                                ),
                            )
                        elif update == None:
                            pass
                        else:
                            json = loads(replace_all(update, parameters))
                            msg = json["content"]
                            embed = Embed.from_dict(json["embeds"][0])
                            lvlup = await message.guild.fetch_channel(channel)
                            await lvlup.send(content=msg, embed=embed)

                except AttributeError:
                    return

    @Jeanne.command(description="See your profile or someone else's profile")
    @Jeanne.describe(member="Which member?")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def profile(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.profile.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        member = ctx.user if member == None else member
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    @profile.error
    async def profile_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.profile.qualified_name)==True:
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            cooldown = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


async def setup(bot: Bot):
    await bot.add_cog(Rank_Group(bot))
    await bot.add_cog(levelling(bot))
