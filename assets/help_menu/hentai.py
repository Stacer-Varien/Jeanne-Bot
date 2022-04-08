from nextcord import *
from nextcord.ui import *

hentai = Embed(title="Hentai Module", description="All commands in this module requires an NSFW enabled channel. Certain tags have been blacklisted for the sake of the viewer and/or due to Discord's ToS. All tags must be put in the format the APIs requires. If the channel is not NSFW enabled, expect an NSFW error message", color=0x7DF9FF)
hentai.add_field(name='Available commands',
              value="• Hentai\n• Yandere\n• Konachan")
hentai.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class hentaihelp(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="Hentai"), SelectOption(
                label="Yandere"), SelectOption(label="Konachan")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0]=="Hentai":
            await ctx.response.defer(ephemeral=True)
            hentai = Embed(color=0x7DF9FF)
            hentai.add_field(
                name="Get a random hentai image/video from Jeanne.\n• **NOTE:** There will no API to fetch images as it is fetched from the local storage (aka, my 'homework' folder). The files are JPEG and MP4 and reduced to 8MB or less for storage and Discord reasons.", value="• **Example:** `/hentai`\n• **Expected result**: `HENTAI PICTURE/VIDEO`")
            await ctx.followup.send(embed=hentai, ephemeral=True)
        if self.values[0] == "Yandere":
            await ctx.response.defer(ephemeral=True)
            yandere = Embed(color=0x7DF9FF)
            yandere.add_field(
                name="Get a random hentai image from Yande.re. You can include a tag too for a specific hentai", value="• **Example:** `/yandere (FOR A RANDOM HENTAI)` \ `/yandere TAG (FOR A SPECIFIC TAG)`\n• **Expected result**: `HENTAI GIVEN WITH OR WITHOUT TAG`\n• **Expected failure**: TAG IS NOT API FORMATED")
            await ctx.followup.send(embed=yandere, ephemeral=True)
        if self.values[0] == "Konachan":
            await ctx.response.defer(ephemeral=True)
            konachan = Embed(color=0x7DF9FF)
            konachan.add_field(
                name="Get a random hentai image from Konachan You can include a tag too for a specific hentai", value="• **Example:** `/konachan (FOR A RANDOM HENTAI)` \ `/konachan TAG (FOR A SPECIFIC TAG)`\n• **Expected result**: `HENTAI GIVEN WITH OR WITHOUT TAG`\n• **Expected failure**: TAG IS NOT API FORMATED")
            await ctx.followup.send(embed=konachan, ephemeral=True)

class hentaiview(View):
    def __init__(self):
        super().__init__()
        self.add_item(hentaihelp())

        

