from nextcord import *
from nextcord.ui import *

image = Embed(title="Image Module", description="Kitsune is the only command that uses the Nekoslife API. The rest are fetched from local storage", color=0x7DF9FF)
image.add_field(name='Available commands',
                 value="• Kitsune\n• Wallpaper\n• Jeanne\n• Saber\n• Neko")
image.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class imagehelp(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="Kistune"), SelectOption(
                label="Wallpaper"), SelectOption(label="Jeanne"), SelectOption(
                label="Saber"), SelectOption(label="Neko")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0]=="Kistune":
            await ctx.response.defer(ephemeral=True)
            kitsune = Embed(color=0x7DF9FF)
            kitsune.add_field(
                name="Get a random kitsune (foxgirl) image from nekos.life.", value="• **Example:** `/kitsune`\n• **Expected result**: `FOXGIRL PICTURE`")
            await ctx.edit_original_message(embed=kitsune, ephemeral=True)
        if self.values[0] == "Wallpaper":
            await ctx.response.defer(ephemeral=True)
            wallpaper = Embed(color=0x7DF9FF)
            wallpaper.add_field(
                name="Need a wallpaper? Get a random wallpaper from Jeanne", value="• **Example:** `/wallpaper`\n• **Expected result**: `WALLPAPER PICTURE`\n• **Expected bug/fault**: `NO IMAGE AND ON 'THINKING' STATUS. PLEASE REPORT`")
            await ctx.edit_original_message(embed=wallpaper, ephemeral=True)
        if self.values[0] == "Jeanne":
            await ctx.response.defer(ephemeral=True)
            jeanne = Embed(color=0x7DF9FF)
            jeanne.add_field(
                name="Get a random Jeanne d'Arc image from Jeanne", value="• **Example:** `/jeanne`\n• **Expected result**: `JEANNE D' ARC/JALTER PICTURE`\n• **Expected bug/fault**: `NO IMAGE AND ON 'THINKING' STATUS. PLEASE REPORT`")
            await ctx.edit_original_message(embed=jeanne, ephemeral=True)
        if self.values[0] == "Saber":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="Get a random Saber image from Jeanne", value="• **Example:** `/saber`\n• **Expected result**: `SABER/SALTER PICTURE`\n• **Expected bug/fault**: `NO IMAGE AND ON 'THINKING' STATUS. PLEASE REPORT`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Neko":
            await ctx.response.defer(ephemeral=True)
            neko = Embed(color=0x7DF9FF)
            neko.add_field(
                name="Get a random Neko image from Jeanne", value="• **Example:** `/neko`\n• **Expected result**: `CATGIRL PICTURE`\n• **Expected bug/fault**: `NO IMAGE AND ON 'THINKING' STATUS. PLEASE REPORT`")
            await ctx.edit_original_message(embed=neko, ephemeral=True)

class imageview(View):
    def __init__(self):
        super().__init__()
        self.add_item(imagehelp())

        

