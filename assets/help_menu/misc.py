from nextcord import *
from nextcord.ui import *

misc = Embed(title="Misc Module", color=0x7DF9FF)
misc.add_field(name='Available commands',
                 value="• Invite\n• Say\n• Report")
misc.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class mischelp(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="Invite"), SelectOption(
                label="Say"), SelectOption(label="Report")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0]=="Invite":
            await ctx.response.defer(ephemeral=True)
            invite = Embed(color=0x7DF9FF)
            invite.add_field(
                name="Invite me to your server or join my creator's server", value="• **Example:** `/invite`")
            await ctx.edit_original_message(embed=invite, ephemeral=True)
        if self.values[0] == "Say":
            await ctx.response.defer(ephemeral=True)
            say = Embed(color=0x7DF9FF)
            say.add_field(
                name="Type a message and I will say it in a specific channel\n• **NOTE:** The command is split into 2 subcommands. `say plain` is just plain text and `say embed` is text with embed\n\n• **Required Permission:** Administrator", value="• **Example:** `/say TEXT`")
            await ctx.edit_original_message(embed=say, ephemeral=True)
        if self.values[0] == "Report":
            await ctx.response.defer(ephemeral=True)
            report = Embed(color=0x7DF9FF)
            report.add_field(
                name="Found a bug or fault? Please report to me\n• **NOTE:** You can't use this to appeal a botban", value="• **Example:** `/report`")
            await ctx.edit_original_message(embed=report, ephemeral=True)


class miscview(View):
    def __init__(self):
        super().__init__()
        self.add_item(mischelp())

        

