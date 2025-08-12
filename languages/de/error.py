from discord import Color, Embed, Interaction
from discord import app_commands as Jeanne
from discord.ext.commands import Bot


class Errors():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle_missing_permissions(self, ctx: Interaction, error: Jeanne.MissingPermissions):
        embed = Embed(
            description=f"Je mist {''.join(error.missing_permissions)} voor dit commando",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=embed)

    async def handle_bot_missing_permissions(self, ctx: Interaction, error: Jeanne.BotMissingPermissions):
        embed = Embed(
            description=f"Ik mis {''.join(error.missing_permissions)} voor dit commando",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=embed)

