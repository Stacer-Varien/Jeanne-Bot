from nextcord import *
from nextcord.ui import *

info = Embed(title="Manage Module", description="Text Channel commands, Voice Channel commands and Category commands require the `manage channels` permisson, Role commands require the `manage roles` permisson and modlog, welcomer and leaver commands requires the `manage server` permission.", color=0x7DF9FF)
info.add_field(name='Available commands',
                 value="• Create Channel\n• Delete Channel\n• Rename Text Channel\n• Renanme Voice Channel\n• Create Role\n• Delete Role\n• Rename Role\n• Rename Category\n• Set\n• Remove")
info.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class infohelp(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="Create Channel"), SelectOption(
                label="Delete Channel"), SelectOption(label="Rename Text Channel"), SelectOption(
                label="Rename Voice Channel"), SelectOption(label="Create Role"), SelectOption(
                label="Delete Role"), SelectOption(label="Rename Role"), SelectOption(label="Rename Category"), SelectOption(label="Set"), SelectOption(label="Remove")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0] =="Create channel":
            await ctx.response.defer(ephemeral=True)
            cc = Embed(color=0x7DF9FF)
            cc.add_field(
                name="Create a text channel, voice channel or category. You will given 3 options to pick when creating them", value="• **Example:** `/create_channel CHANNEL_TYPE(text, voice or category) NAME`")
            await ctx.edit_original_message(embed=cc, ephemeral=True)
        if self.values[0] == "Delete Channel":
            await ctx.response.defer(ephemeral=True)
            dc = Embed(color=0x7DF9FF)
            dc.add_field(
                name="Deletes the text channel, voice channel or category.", value="• **Example:** `/delete_channel CHANNEL_NAME`")
            await ctx.edit_original_message(embed=dc, ephemeral=True)
        if self.values[0] == "Rename Text Channel":
            await ctx.response.defer(ephemeral=True)
            rtc = Embed(color=0x7DF9FF)
            rtc.add_field(
                name="Renames the text channel", value="• **Example:** `/rename_text_channel CHANNEL_NAME NEW_NAME`")
            await ctx.edit_original_message(embed=rtc, ephemeral=True)
        if self.values[0] == "Rename Voice Channel":
            await ctx.response.defer(ephemeral=True)
            rvc = Embed(color=0x7DF9FF)
            rvc.add_field(
                name="Renames the voice channel", value="• **Example:** `/rename_voice_channel CHANNEL_NAME NEW_NAME`")
            await ctx.edit_original_message(embed=rvc, ephemeral=True)
        if self.values[0] == "Create Role":
            await ctx.response.defer(ephemeral=True)
            cr = Embed(color=0x7DF9FF)
            cr.add_field(
                name="Creates a new role", value="• **Example:** `/create_role NAME`")
            await ctx.edit_original_message(embed=cr, ephemeral=True)
        if self.values[0] == "Delete Role":
            await ctx.response.defer(ephemeral=True)
            dr = Embed(color=0x7DF9FF)
            dr.add_field(
                name="Deletes a role", value="• **Example:** `/delete_role ROLE_NAME`")
            await ctx.edit_original_message(embed=dr, ephemeral=True)
        if self.values[0] == "Rename Role":
            await ctx.response.defer(ephemeral=True)
            rr = Embed(color=0x7DF9FF)
            rr.add_field(
                name="Renames a role", value="• **Example:** `/rename_role OLD_NAME NEW_NAME`")
            await ctx.edit_original_message(embed=rr, ephemeral=True)
        if self.values[0] == "Set":
            await ctx.response.defer(ephemeral=True)
            rr = Embed(color=0x7DF9FF)
            rr.add_field(
                name="Sets a welcomer/leaver/modlog channel for the server\n• **NOTE:** Three options will be given to you. You can pick one for a channel then do it again after executing the command. It will only set one channel depending on what you have chosen. The welcomng and leaving message is uncustomisable for now. Channels set for modlog will have warns, mutes and bans posted in there.", value="• **Example:** `/set TYPE CHANNEL`")
            await ctx.edit_original_message(embed=rr, ephemeral=True)
        if self.values[0] == "Rename Category":
            await ctx.response.defer(ephemeral=True)
            set = Embed(color=0x7DF9FF)
            set.add_field(
                name="Renames a category", value="• **Example:** `/rename_category OLD_NAME NEW_NAME`")
            await ctx.edit_original_message(embed=set, ephemeral=True)
        if self.values[0] == "Remove":
            await ctx.response.defer(ephemeral=True)
            remove = Embed(color=0x7DF9FF)
            remove.add_field(
                name="Removes a welcomer/leaving/modlog channel for the server\n• **NOTE:** Four options will be given to you. You can pick an option then do it again after executing the command. If you want all to be removed, use the `all` option.", value="• **Example:** `/remove TYPE`")
            await ctx.edit_original_message(embed=remove, ephemeral=True)


class infoview(View):
    def __init__(self):
        super().__init__()
        self.add_item(infohelp())

        

