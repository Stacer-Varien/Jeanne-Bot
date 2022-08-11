from nextcord import *

from config import WEBHOOK


class Bot_Report_Modal(ui.Modal):
    def __init__(self, type):
        self.type = type
        super().__init__(
            "Report problems with Jeanne"
        )

        self.mdescription = ui.TextInput(label="What problem did you find in Jeanne?", min_length=5, max_length=4000,
                                         required=True,
                                         placeholder="Type the problem here. Don't forget to include how you managed to find it.",
                                         style=TextInputStyle.paragraph)
        self.add_item(self.mdescription)

    async def callback(self, ctx: Interaction) -> None:
        embed = Embed(title="Bot Report", description=self.mdescription.value).add_field(name="Type of report",
                                                                                         value=self.type, inline=False)
        SyncWebhook.from_url(WEBHOOK).send(embed=embed)
        return await ctx.response.send_message(
            "Thank you for your report. I will look into it. Unfortunately, you have to wait for the outcome if it was successful or not.",
            ephemeral=True)


class Embed_Generator(ui.Modal):
    def __init__(self):
        super().__init__("Embed Generator")

        self.emcontent = ui.TextInput(label="Content", placeholder="Add content outside embed", max_length=1024,
                                      style=TextInputStyle.paragraph, required=False)
        self.add_item(self.emcontent)
        self.emtitle = ui.TextInput(label="Embed Title", placeholder="Add title here", max_length=256,
                                    style=TextInputStyle.short, required=False)
        self.add_item(self.emtitle)
        self.emdescription = ui.TextInput(label="Embed Description", placeholder="Add description here",
                                          max_length=4096, style=TextInputStyle.paragraph, required=False)
        self.add_item(self.emdescription)
        self.emcolor = ui.TextInput(label="Embed Color", placeholder="Add color here. Use HEX codes", min_length=6,
                                    max_length=6, style=TextInputStyle.short, required=False)
        self.add_item(self.emcolor)
        self.emname = ui.TextInput(label="Embed Field Name", placeholder="Add name here", max_length=256,
                                   style=TextInputStyle.short, required=False)
        self.add_item(self.emname)
        self.emvalue = ui.TextInput(label="Embed Field Value", placeholder="Add field value here", max_length=1024,
                                    style=TextInputStyle.paragraph, required=False)
        self.add_item(self.emvalue)
        self.emimage = ui.TextInput(label="Embed Field Value", placeholder="Add image URL here", style=TextInputStyle.short,
                                    required=False)
        self.add_item(self.emimage)
        self.emthumbnail = ui.TextInput(label="Embed Thumbnail", placeholder="Add image URL here",
                                        style=TextInputStyle.short, required=False)
        self.add_item(self.emthumbnail)

    async def callback(self, ctx: Interaction) -> None:
        content = self.emcontent.value
        
        embed = Embed()
        embed.title = self.emtitle.value
        embed.description = self.emdescription.value
        embed.color = self.emcolor.value
        embed_field=embed.add_field(name=self.emname, value=self.emvalue, inline=False)
        image=embed.set_image(url=self.emimage.value)
        thumbnail=embed.set_thumbnail(url=self.emthumbnail.value)

        if embed.color == None:
            embed.color = Colour.default()

        if content == None:
            content = None

        embed_gen = [embed.title, embed.description, embed.color, embed_field, image, thumbnail]

        for a in embed_gen:
            try:
                em = a
            except:
                pass

        return await ctx.response.send_message(embed=em)
