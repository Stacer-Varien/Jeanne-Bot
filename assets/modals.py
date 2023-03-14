from collections import OrderedDict
from json import loads
from discord import AllowedMentions, Embed, Interaction, TextChannel, ui, TextInput, TextStyle
from assets.buttons import Confirmation
from db_functions import Levelling, Welcomer


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

class Welcomingmsg(ui.Modal, title="Welcoming Message"):

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

        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json['embeds'][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)

        confirm = Embed(
                description=
                "This is the preview of the welcoming message.\nAre you happy with it?"
            )

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


class Leavingmsg(ui.Modal, title="Leaving Message"):

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

        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json['embeds'][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)

        confirm = Embed(
            description=
            "This is the preview of the leaving message.\nAre you happy with it?"
        )

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
            Welcomer(ctx.guild).set_leaving_msg(self.jsonscript.value)

            embed = Embed(description="Leaving message set")
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


class Levelmsg(ui.Modal, title="Level Update Message"):

    def __init__(self, channel:TextChannel) -> None:
        super().__init__()
        self.channel=channel

    jsonscript = TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder=
        "Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000)

    async def on_submit(self, ctx: Interaction) -> None:
        Levelling(server=ctx.guild).add_level_channel(self.channel)
        parameters = OrderedDict([
            ("%member%", str(ctx.user)),
            ("%pfp%", str(ctx.user.display_avatar)),
            ("%server%", str(ctx.guild.name)),
            ("%mention%", str(ctx.user.mention)),
            ("%name%", str(ctx.user.name)),
            ("%newlevel%",
             str(Levelling(ctx.user, ctx.guild).get_member_level()))
        ])


        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json['embeds'][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)

        confirm = Embed(
            description=
            "This is the preview of the level update message whenever someone levels up in the server and will be sent to {}.\nAre you happy with it?"
            .format(self.channel.mention))


        view = Confirmation(ctx.user)
        await ctx.followup.send(content=content,
                                embeds=[embed, confirm],
                                view=view,
                                allowed_mentions=AllowedMentions(
                                    everyone=False, roles=False, users=False),
                                ephemeral=True)
        await view.wait()

        if view.value == True:
            Levelling(server=ctx.guild).add_level_channel(self.channel, self.jsonscript.value)

            embed = Embed(description="Level update message set")
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
