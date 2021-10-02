import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="See the bot's status from development to now")
    async def help(self, ctx: SlashContext):
        embed = discord.Embed(title="Help Commands",
                              description="Here are some commands to help you.",
                              color=0x236ce1)
        embed.add_field(name="Fun",
                        value="8 Ball (8b, 8ball)\nHentai (h) **NSFW**\nRoll Dice (rd, dice)\nCombine\nFlip (coinflip, headsortails, piece)\nChoose (pick)\nReverse",
                        inline=True)
        embed.add_field(
            name="Info",
            value="User Info (uinfo, minfo, guild, guildinfo)\nServer Info (sinfo)\nAvavtar (av)Ping\nStats",
            inline=True)
        embed.add_field(
            name="Creator Only",
            value="Find Server (fserver)\nFind User (fuser)\nMutuals\nBot Mutuals (bm)",
            inline=True)
        embed.add_field(
            name="Misc", value="Help\nInvite\nSay\nSayembed (saye)", inline=True)
        embed.add_field(name="Moderation",
                        value="Warn (w)\nKick (k)\nBan (b)\nUnban (unb)\nPurge\nMute\nUnmute",
                        inline=True)
        embed.add_field(name="Management",
                        value="Text Channel (tc)\nVoice Channel (vc)\nRole (r)\nCategory (cat)",
                        inline=True)
        embed.add_field(name="Reactions",
                        value="Hug\nSlap\nSmug\nTickle\nPoke\nPat\nKiss",
                        inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))
