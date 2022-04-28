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
            userinfo = Embed(color=0x7DF9FF)
            userinfo.add_field(
                name="Create a text channel, voice channel or category. You will given 3 options to pick when creating them", value="• **Example:** `/create_channel CHANNEL_TYPE(text, voice or category) NAME`")
            await ctx.edit_original_message(embed=userinfo, ephemeral=True)
        if self.values[0] == "Delete Channel":
            await ctx.response.defer(ephemeral=True)
            Serverinfo = Embed(color=0x7DF9FF)
            Serverinfo.add_field(
                name="Deletes the text channel, voice channel or category.", value="• **Example:** `/delete_channel CHANNEL_NAME`")
            await ctx.edit_original_message(embed=Serverinfo, ephemeral=True)
        if self.values[0] == "Rename Text Channel":
            await ctx.response.defer(ephemeral=True)
            ping = Embed(color=0x7DF9FF)
            ping.add_field(
                name="Renames the text channel", value="• **Example:** `/rename_text_channel CHANNEL_NAME NEW_NAME`")
            await ctx.edit_original_message(embed=ping, ephemeral=True)
        if self.values[0] == "Rename Voice Channel":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="Renames the voice channel", value="• **Example:** `/rename_voice_channel CHANNEL_NAME NEW_NAME`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Guild Banner":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See the server's banner\n• **NOTE:** If the server is not boosted to Level 2, it will return with a `Not boosted to Level 2` error. If the server doesn't have a banner, it will return with a footer text only.", value="• **Example:** `/guildbanner`\n• **Expected result**: `SERVER'S BANNER IF APPLICABLE`\n• **Expected failure**: `SERVER NOT BOOSTED TO LEVEL 2 ERROR OR NO SERVER BANNER FOUND`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Avatar":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See your avatar or a member's avatar", value="• **Example:** `/avatar` (IF YOURSELF) / `/avatar MEMBER` (IF MEMBER)\n• **Expected result**: `MEMBERS'S AVATAR`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Guild Avatar":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See your guild avatar or a member's guild avatar\n• **NOTE:** If the member has no guild avatar set, it will return with their normal avatar.", value="• **Example:** `/guildavatar` (IF YOURSELF) / `/guildavatar MEMBER` (IF MEMBER)\n• **Expected result**: `MEMBERS'S SERVER AVATAR`\n• **Expected failure**: `MEMBERS'S NORMAL AVATAR WITH FOOTER TEXT`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)


class infoview(View):
    def __init__(self):
        super().__init__()
        self.add_item(infohelp())

        

