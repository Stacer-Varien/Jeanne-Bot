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
        return Profile().generate_profile(**args)


    async def generate_profile_card(self, ctx: Interaction, member: Member):
        try:
            memdata = Levelling(member, ctx.guild)
            slvl, sexp = memdata.get_member_level, memdata.get_member_xp
            glvl, gexp = memdata.get_user_level, memdata.get_user_xp

            bg = Inventory(member).selected_wallpaper
            grank, srank, rrank = (
                memdata.get_member_global_rank,
                memdata.get_member_server_rank,
                get_richest(member),
            )
            bio, font_color = Inventory(member).get_bio, Inventory(member).get_color
            voted = await self.topggpy.get_user_vote(member.id)

            args = {
                "bg_image": bg[1] if bg else "",
                "profile_image": str(member.avatar.with_format("png")),
                "font_color": font_color,
                "server_level": slvl,
                "server_user_xp": sexp,
                "server_next_xp": (slvl * 50) + ((slvl - 1) * 25) + 50,
                "global_level": glvl,
                "global_user_xp": gexp,
                "global_next_xp": (glvl * 50) + ((glvl - 1) * 25) + 50,
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
                "brightness": bg[2] if bg else 100,
            }

            image = await get_event_loop().run_in_executor(
                None, partial(self.get_profile, args)
            )
            file = File(fp=image, filename=f"{member.name}_profile_card.png")
            await ctx.followup.send(file=file)

        except:
            no_exp = Embed(description=f"Failed to make profile card")
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

        await self.generate_profile_card(ctx, member)

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
        if Botban(message.author).check_botbanned_user or message.author.bot:
            return

        levelling_instance = Levelling(message.author, message.guild)
        if not levelling_instance.check_xpblacklist_channel(message.channel):
            try:
                level_data = await levelling_instance.add_xp()

                if level_data is None:
                    return

                channel, update, levelup = level_data

                role_reward = message.guild.get_role(
                    levelling_instance.get_role_reward()
                )
                parameters = OrderedDict(
                    [
                        ("%member%", str(message.author)),
                        ("%pfp%", str(message.author.display_avatar)),
                        ("%server%", str(message.guild.name)),
                        ("%mention%", str(message.author.mention)),
                        ("%name%", str(message.author.name)),
                        ("%newlevel%", str(levelling_instance.get_member_level())),
                        ("%role%", str((role_reward.name if role_reward else None))),
                        (
                            "%rolemention%",
                            str((role_reward.mention if role_reward else None)),
                        ),
                    ]
                )

                def replace_all(text: str, dic: dict):
                    for i, j in dic.items():
                        text = text.replace(i, j)
                    return text

                try:
                    await message.author.add_roles(role_reward)
                    if levelup == "0":
                        msg = "CONGRATS {}! You were role awarded {}".format(
                            message.author,
                            (role_reward.name if role_reward else None),
                        )
                    elif levelup is None:
                        pass
                    else:
                        json = loads(replace_all(levelup, parameters))
                        msg = json["content"]
                        embed = Embed.from_dict(json["embeds"][0])

                    await self.send_level_message(channel, msg, embed)

                except:
                    if update == "0":
                        msg = "{} has leveled up to `level {}`".format(
                            message.author, levelling_instance.get_member_level()
                        )
                    elif update is None:
                        pass
                    else:
                        json = loads(replace_all(update, parameters))
                        msg = json["content"]
                        embed = Embed.from_dict(json["embeds"][0])

                    await self.send_level_message(channel, msg, embed)

            except AttributeError:
                pass

    async def send_level_message(
        self, channel_id: Optional[int], content: str, embed: Optional[Embed]
    ):
        if channel_id is not None:
            lvlup_channel = await self.bot.fetch_channel(channel_id)
            await lvlup_channel.send(content=content, embed=embed)

    @Jeanne.command(description="See your profile or someone else's profile")
    @Jeanne.describe(member="Which member?")
    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
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
            if Command(ctx.guild).check_disabled(self.profile.qualified_name) == True:
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
