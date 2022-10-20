from nextcord import *

from config import WEBHOOK


class Bot_Report_Modal(ui.Modal):
    def __init__(self, type:str):
        self.type = type
        super().__init__("Report problems with Jeanne")

        self.mdescription = ui.TextInput(label="What problem did you find in Jeanne?", min_length=5, max_length=4000,
                                         required=True,
                                         placeholder="Type the problem here. Don't forget to include steps of how you managed to find it. If it is a violator report, please send a message link",
                                         style=TextInputStyle.paragraph)
        self.add_item(self.mdescription)

    async def callback(self, ctx: Interaction) -> None:
        embed = Embed(title="Bot Report", description=self.mdescription.value, color=ctx.user.color).add_field(name="Type of report", value=self.type, inline=False)
        embed.set_footer(text="Report by {} | {}".format(ctx.user, ctx.user.id))
        SyncWebhook.from_url(WEBHOOK).send(embed=embed)
        return await ctx.response.send_message(
            "Thank you for your report. I will look into it. Unfortunately, you have to wait for the outcome if it was successful or not.",
            ephemeral=True)


class Say_Modal(ui.Modal):
    def __init__(self, type, channel):
        self.channel=channel
        self.type=type
        super().__init__("Report problems with Jeanne")

        self.message = ui.TextInput(label="Type your message here", min_length=1, max_length=4000,
                                         required=True,
                                         style=TextInputStyle.paragraph)
        self.add_item(self.message)

    async def callback(self, ctx: Interaction) -> None:
        if self.type == "plain":
            embed = Embed(color=ctx.user.color).set_footer(
                text="Author: {} | {}".format(ctx.user, ctx.user.id))
            await ctx.send("Sent", ephemeral=True)
            return await self.channel.send(self.message.value, embed=embed)
        elif self.type == "embed":
            embed_text = Embed(description=self.message.value, color=ctx.user.color).set_footer(
                text="Author: {} | {}".format(ctx.user, ctx.user.id))
            await ctx.send("Sent", ephemeral=True)
            return await self.channel.send(self.message.value, embed=embed_text)
