from collections import OrderedDict
from json import loads
from discord import AllowedMentions, Embed, Interaction, ui, TextInput, TextStyle
from assets.buttons import Confirmation
from db_functions import Welcomer


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

class Welcomingmsg(ui.Modal, title="Welcoming Message Set"):

    def __init__(self) -> None:
        super().__init__()


    jsonscript = TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder=
        "Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000)

    async def on_submit(self, ctx: Interaction) -> None:

        humans = str(
            len([member for member in ctx.guild.members if not member.bot]))
        parameters = OrderedDict([("%member%", str(ctx.user)),
                                  ("%pfp%", str(ctx.user.display_avatar)),
                                  ("%server%", str(ctx.guild.name)),
                                  ("%mention%", str(ctx.user.mention)),
                                  ("%name%", str(ctx.user.name)),
                                  ("%members%", str(ctx.guild.member_count)),
                                  ("%humans%", str(humans)),
                                  ("%icon%", str(ctx.guild.icon))])
        json = loads(replace_all(self.jsonscript.value, parameters))

        try:
            content = json["content"]
        except:
            return

        confirm = Embed(
                description=
                "This is the preview of the welcoming message.\nAre you happy with it?"
            )

        try:
                embed = Embed.from_dict(json['embeds'][0])
                view = Confirmation(ctx.user)
                await ctx.response.send_message(content=content,
                                        embeds=[embed, confirm],
                                        view=view,
                                        allowed_mentions=AllowedMentions(
                                            everyone=False,
                                            roles=False,
                                            users=False),
                                        ephemeral=True)
                await view.wait()

                if view.value == True:
                    Welcomer(ctx.guild).set_welcomer_msg(self.jsonscript.value)

                    embed = Embed(description="Welcoming message set")
                    await ctx.edit_original_response(content=None,
                                                     embeds=[embed],
                                                     view=None)

                elif view.value == False:
                    embed = Embed(description="Action cancelled")
                    await ctx.edit_original_response(content=None,
                                                     embeds=[embed],
                                                     view=None)
                else:
                    embed = Embed(description="Timeout")
                    await ctx.edit_original_response(content=None,
                                                     embeds=[embed],
                                                     view=None)

        except:
                view = Confirmation(ctx.user)
                await ctx.followup.send(content=self.jsonscript.value,
                                        embed=confirm,
                                        allowed_mentions=AllowedMentions(
                                            everyone=False,
                                            roles=False,
                                            users=False),
                                        view=view,
                                        ephemeral=True)
                await view.wait()

                if view.value == None:
                    embed = Embed(description="Timeout")
                    await ctx.edit_original_response(content=None,
                                                     embeds=[embed],
                                                     view=None)
                elif view.value:
                    Welcomer(ctx.guild).set_welcomer_msg(self.jsonscript.value)

                    embed = Embed(description="Welcoming message set")
                    await ctx.edit_original_response(content=None,
                                                     embeds=[embed],
                                                     view=None)

                else:
                    embed = Embed(description="Action cancelled")
                    await ctx.edit_original_response(content=None,
                                                     embeds=[embed],
                                                     view=None)

