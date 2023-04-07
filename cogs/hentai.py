from json import loads
from random import choice
from discord import Color, Embed, Interaction, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from requests import get
from functions import Botban, Hentai
from typing import Literal, Optional
from assets.buttons import ReportContent
from assets.menus import ReportSelect


class nsfw(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(description="Get a random hentai from Jeanne", nsfw=True)
    @Jeanne.describe(rating="Do you want questionable or explicit content?")
    async def hentai(
            self,
            ctx: Interaction,
            rating: Optional[Literal["questionable",
                                     "explicit"]] = None) -> None:
        await ctx.channel.typing()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        if rating == None:
            rating = ["questionable", "explicit"]
            rating = choice(rating)

        gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub"
        response = get(gelbooru_api)
        ret = loads(response.text)
        gelbooru_image = choice(ret['post'])["file_url"]

        yandere_image = choice(
            get(f"https://yande.re/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub"
                ).json())['file_url']

        konachan_image = choice(
            get(f"https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:{rating}+-loli+-shota+-cub"
                ).json())['file_url']

        h = [gelbooru_image, yandere_image, konachan_image]

        hentai: str = choice(h)

        if hentai == gelbooru_image:
            source = 'Gelbooru'

        elif hentai == yandere_image:
            source = 'Yande.re'

        elif hentai == konachan_image:
            source = 'Konachan'

        if hentai.endswith('mp4'):
            await ctx.channel.send(hentai)

        else:
            embed = Embed(color=Color.purple()).set_image(
                url=hentai).set_footer(
                    text="Fetched from {} • Credits must go to the artist".
                    format(source))
            await ctx.channel.send(embed=embed)


    @Jeanne.command(description="Get a random media content from Gelbooru",
                    nsfw=True)
    @Jeanne.describe(rating="Do you want questionable or explicit content?",
                     tag="Add your tag", plus="Need more content? (up to 4)")
    async def gelbooru(self,
                       ctx: Interaction,
                       rating: Optional[Literal["questionable", "explicit"]],
                       tag: Optional[str] = None, plus:Optional[bool]=None) -> None:
        await ctx.channel.typing()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        image = Hentai(plus).gelbooru(rating, tag)

        if plus==True:
            view = ReportSelect(image[0]['file_url'], image[1]['file_url'], image[2]['file_url'], image[3]['file_url'])
            if 'mp4' in str(image):
                media=[image['file_url'] for image in image]
                await ctx.channel.send("\n".join(media), view=view)
            else:
                color = Color.random()
                embed1 = Embed(
                    color=color, url='https://gelbooru.com'
                ).set_image(url=image[0]['file_url']).set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist")
                embed2 = Embed(
                    color=color,
                    url='https://gelbooru.com').set_image(url=image[1]['file_url'])
                embed3 = Embed(
                    color=color,
                    url='https://gelbooru.com').set_image(url=image[2]['file_url'])
                embed4 = Embed(
                    color=color,
                    url='https://gelbooru.com').set_image(url=image[3]['file_url'])
                embeds = [embed1, embed2, embed3, embed4]
                await ctx.channel.send(embeds=embeds, view=view)
        else:
            view=ReportContent(image)
            if image.endswith('mp4'):
                await ctx.channel.send(image, view=view)

            else:
                embed = Embed(color=Color.purple(
                )).set_image(url=image).set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist"
                )
                view = ReportContent(image)
                await ctx.channel.send(embed=embed, view=view)

    @gelbooru.error
    async def gelbooru_error(self, ctx: Interaction,
                             error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if IndexError or KeyError:
                no_tag = Embed(description="The tag could not be found",
                               color=Color.red())
                await ctx.followup.send(embed=no_tag)

    @Jeanne.command(description="Get a random hentai from Yande.re", nsfw=True)
    @Jeanne.describe(rating="Do you want questionable or explicit content?",
                     tag="Add your tag",
                     plus="Need more content? (up to 4)")
    async def yandere(self,
                      ctx: Interaction,
                      rating: Optional[Literal["questionable", "explicit"]],
                      tag: Optional[str] = None, plus:Optional[bool]=None) -> None:
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        if tag == "02":
            await ctx.followup.send(
                "Tag has been blacklisted due to it returning extreme content and guro"
            )

        else:
            image = Hentai(plus).yandere(rating, tag)

            if plus == True:
                color = Color.random()
                embed1 = Embed(
                    color=color, url='https://yande.re'
                ).set_image(url=image[0]['file_url']).set_footer(
                    text="Fetched from Yande.re • Credits must go to the artist"
                )
                embed2 = Embed(color=color,
                               url='https://yande.re').set_image(
                                   url=image[1]['file_url'])
                embed3 = Embed(color=color,
                               url='https://yande.re').set_image(
                                   url=image[2]['file_url'])
                embed4 = Embed(color=color,
                               url='https://yande.re').set_image(
                                   url=image[3]['file_url'])
                embeds = [embed1, embed2, embed3, embed4]
                await ctx.followup.send(embeds=embeds)
            else:
                yandere = Embed(color=Color.random())
                yandere.set_image(url=image['file_url'])
                yandere.set_footer(
                    text="Fetched from Yande.re • Credits must go to the artist")
                await ctx.followup.send(embed=yandere)

    @yandere.error
    async def yandere_error(self, ctx: Interaction,
                            error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if IndexError or KeyError:
                no_tag = Embed(description="The tag could not be found",
                               color=Color.red())
                await ctx.followup.send(embed=no_tag)

    @Jeanne.command(description="Get a random hentai from Konachan")
    @Jeanne.describe(rating="Do you want questionable or explicit content?",
                     tag="Add your tag", plus="Need more content (up to 4)")
    async def konachan(self,
                       ctx: Interaction,
                       rating: Optional[Literal["questionable", "explicit"]],
                       tag: Optional[str] = None, plus:Optional[bool]=None) -> None:
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        image = Hentai(plus).konachan(rating, tag)

        if plus == True:
            color = Color.random()
            embed1 = Embed(
                color=color, url='https://konachan.com'
            ).set_image(url=image[0]['file_url']).set_footer(
                text="Fetched from Yande.re • Credits must go to the artist"
            )
            embed2 = Embed(
                color=color,
                url='https://konachan.com').set_image(url=image[1]['file_url'])
            embed3 = Embed(
                color=color,
                url='https://konachan.com').set_image(url=image[2]['file_url'])
            embed4 = Embed(
                color=color,
                url='https://konachan.com').set_image(url=image[3]['file_url'])
            embeds = [embed1, embed2, embed3, embed4]
            await ctx.followup.send(embeds=embeds)
        else:
            konachan = Embed(color=Color.random())
            konachan.set_image(url=image['file_url'])
            konachan.set_footer(
                text="Fetched from Konachan • Credits must go to the artist"
            )
            await ctx.followup.send(embed=konachan)

    @konachan.error
    async def konachan_error(self, ctx: Interaction,
                             error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if IndexError or KeyError:
                no_tag = Embed(description="The tag could not be found",
                               color=Color.red())
                await ctx.followup.send(embed=no_tag)


async def setup(bot: Bot):
    await bot.add_cog(nsfw(bot))
