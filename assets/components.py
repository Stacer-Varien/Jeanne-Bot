from functools import partial
from discord import (
    CategoryChannel,
    ui,
    ButtonStyle,
    Interaction,
    User,
    SelectOption,
    AllowedMentions,
    Color,
    Embed,
    SyncWebhook,
    TextChannel,
    TextStyle,
)
from typing import Optional
from collections import OrderedDict
from json import loads
from config import WEBHOOK
from functions import Inventory, Levelling, Logger, Manage, Welcomer


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class Confirmation(ui.View):
    def __init__(self, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, ctx: Interaction, button: ui.Button):
        self.value = True
        button.disabled = True
        self.stop()

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = False
        button.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Heads_or_Tails(ui.View):
    def __init__(self, author: User):
        self.author = author
        super().__init__(timeout=30)
        self.value = None

    @ui.button(label="Heads", style=ButtonStyle.green)
    async def confirm(self, ctx: Interaction, button: ui.Button):
        self.value = "Heads"
        self.stop()

    @ui.button(label="Tails", style=ButtonStyle.green)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = "Tails"
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Cancellation(ui.View):
    def __init__(self, author: User):
        super().__init__()
        self.author = author
        self.value = None

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = "cancel"
        button.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Welcomingmsg(ui.Modal, title="Welcoming Message"):
    def __init__(self) -> None:
        super().__init__()

    jsonscript = ui.TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        humans = str(len([member for member in ctx.guild.members if not member.bot]))
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%members%", str(ctx.guild.member_count)),
                ("%humans%", str(humans)),
                ("%icon%", str(ctx.guild.icon)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)
        confirm = Embed(
            description="This is the preview of the welcoming message.\nAre you happy with it?"
        )
        view = Confirmation(ctx.user)
        try:
            embeds = [embed, confirm]
        except:
            embeds = [confirm]
        await ctx.response.send_message(
            content=content,
            embeds=embeds,
            view=view,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
            ephemeral=True,
        )
        await view.wait()
        if view.value == True:
            await Manage(ctx.guild).set_welcomer_msg(self.jsonscript.value)
            embed = Embed(description="Welcoming message set")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        elif view.value == False:
            embed = Embed(description="Action cancelled")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        else:
            embed = Embed(description="Timeout")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class Leavingmsg(ui.Modal, title="Leaving Message"):
    def __init__(self) -> None:
        super().__init__()

    jsonscript = ui.TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        humans = str(len([member for member in ctx.guild.members if not member.bot]))
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%members%", str(ctx.guild.member_count)),
                ("%humans%", str(humans)),
                ("%icon%", str(ctx.guild.icon)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)
        confirm = Embed(
            description="This is the preview of the leaving message.\nAre you happy with it?"
        )
        view = Confirmation(ctx.user)
        try:
            embeds = [embed, confirm]
        except:
            embeds = [confirm]
        await ctx.response.send_message(
            content=content,
            embeds=embeds,
            view=view,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
            ephemeral=True,
        )
        await view.wait()
        if view.value == True:
            await Manage(ctx.guild).set_leaving_msg(self.jsonscript.value)
            embed = Embed(description="Leaving message set")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        elif view.value == False:
            embed = Embed(description="Action cancelled")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        else:
            embed = Embed(description="Timeout")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class Levelmsg(ui.Modal, title="Level Update Message"):
    def __init__(self, channel: TextChannel) -> None:
        super().__init__()
        self.channel = channel

    jsonscript = ui.TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%newlevel%", str(Levelling(ctx.user, ctx.guild).get_member_level)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)
        confirm = Embed(
            description="This is the preview of the level update message whenever someone levels up in the server and will be sent to {}.\nAre you happy with it?".format(
                self.channel.mention
            )
        )
        view = Confirmation(ctx.user)
        try:
            embeds = [embed, confirm]
        except:
            embeds = [confirm]
        await ctx.response.send_message(
            content=content,
            embeds=embeds,
            view=view,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
            ephemeral=True,
        )
        await view.wait()
        if view.value == True:
            await Manage(server=ctx.guild).add_level_channel(
                self.channel, self.jsonscript.value
            )
            embed = Embed(description="Level update message set")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        elif view.value == False:
            embed = Embed(description="Action cancelled")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        else:
            embed = Embed(description="Timeout")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class RankUpmsg(ui.Modal, title="Role Reward Message"):
    def __init__(self) -> None:
        super().__init__()

    jsonscript = ui.TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%newlevel%", str(Levelling(ctx.user, ctx.guild).get_member_level)),
                ("%role%", str(ctx.user.top_role)),
                ("%rolemention%", str(ctx.user.top_role.mention)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)
        confirm = Embed(
            description="This is the preview of the role reward message whenever someone recieves a role reward after levelling up in the server and will be sent to the current level update channel\nAre you happy with it?"
        )
        view = Confirmation(ctx.user)
        try:
            embeds = [embed, confirm]
        except:
            embeds = [confirm]
        await ctx.response.send_message(
            content=content,
            embeds=embeds,
            view=view,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
            ephemeral=True,
        )
        await view.wait()
        if view.value == True:
            await Manage(server=ctx.guild).add_rankup_rolereward(self.jsonscript.value)
            embed = Embed(description="Level update message set")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        elif view.value == False:
            embed = Embed(description="Action cancelled")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        else:
            embed = Embed(description="Timeout")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class ReportModal(ui.Modal, title="Bot Report"):
    def __init__(self):
        super().__init__()

    report_type = ui.TextInput(
        label="Type of report",
        placeholder="Example: bug, fault, violator",
        required=True,
        min_length=10,
        max_length=30,
        style=TextStyle.short,
    )
    report = ui.TextInput(
        label="Problem",
        placeholder="Type the problem here",
        required=True,
        min_length=10,
        max_length=2000,
        style=TextStyle.paragraph,
    )
    steps = ui.TextInput(
        label="Steps of how you got this problem",
        placeholder="Type the steps here",
        required=False,
        min_length=10,
        max_length=1024,
        style=TextStyle.paragraph,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        report = Embed(title=self.report_type.value, color=Color.brand_red())
        report.description = self.report.value
        if self.steps.value != None or self.steps.value == "":
            report.add_field(name="Steps", value=self.steps.value, inline=False)
        report.set_footer(text="Reporter {}| `{}`".format(ctx.user, ctx.user.id))
        SyncWebhook.from_url(WEBHOOK).send(embed=report)
        embed = Embed(
            description="Thank you for submitting your bot report. The developer will look into it but the will not tell you the results.\n\nPlease know that your user ID has been logged if you are trolling around."
        )
        await ctx.response.send_message(embed=embed)


class ForumGuildlines(ui.Modal, title="Forum Guideline"):
    def __init__(self, name: str, category: CategoryChannel = None):
        self.name = name
        self.category = category
        super().__init__()

    guidelines = ui.TextInput(
        label="Guidelines",
        placeholder="Type here. Markdown supported",
        required=True,
        min_length=1,
        max_length=4000,
        style=TextStyle.paragraph,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        embed = Embed()
        forum = await ctx.guild.create_forum(
            name=self.name, topic=self.guidelines.value
        )
        embed.description = "{} has been created".format(forum.jump_url)
        embed.color = Color.random()
        if self.category:
            await forum.edit(category=self.category)
            embed.add_field(
                name="Added into category", value=self.category.name, inline=True
            )
        await ctx.response.send_message(embed=embed)


class ReportContentM(ui.Modal, title="Illicit Content Report"):
    def __init__(self, link: str):
        self.link = link
        super().__init__()

    illegalcontent = ui.TextInput(
        label="Reason",
        style=TextStyle.short,
        placeholder="Why are you reporting this link? (eg. loli hentai, too much blood)",
        required=True,
        min_length=4,
        max_length=256,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        report = Embed(title="Illicit Content Reported", color=Color.brand_red())
        report.add_field(name="Link", value=self.link, inline=False)
        report.add_field(name="Reason", value=self.illegalcontent.value, inline=False)
        report.set_footer(text="Reporter {}| `{}`".format(ctx.user, ctx.user.id))
        SyncWebhook.from_url(WEBHOOK).send(embed=report)
        embed = Embed(
            description="Than you for submitting the report.\n\nPlease know that your user ID has been logged if you are trolling around."
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)


class ReportContentPlus(ui.Select):
    def __init__(
        self,
        link1: Optional[str] = None,
        link2: Optional[str] = None,
        link3: Optional[str] = None,
        link4: Optional[str] = None,
    ):
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3
        self.link4 = link4
        options = [
            SelectOption(label="Report 1st Media", value=self.link1),
            SelectOption(label="Report 2nd Media", value=self.link2),
            SelectOption(label="Report 3rd Media", value=self.link3),
            SelectOption(label="Report 4th Media", value=self.link4),
        ]
        super().__init__(
            placeholder="Saw something illegal? Report it here",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, ctx: Interaction):
        await ctx.response.send_modal(ReportContentM(self.values[0]))


class ReportSelect(ui.View):
    def __init__(
        self,
        link1: Optional[str] = None,
        link2: Optional[str] = None,
        link3: Optional[str] = None,
        link4: Optional[str] = None,
    ):
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3
        self.link4 = link4
        self.value = None
        super().__init__(timeout=60)
        self.add_item(ReportContentPlus(self.link1, self.link2, self.link3, self.link4))


class ReportContent(ui.View):
    def __init__(self, link: str):
        super().__init__(timeout=180)
        self.link = link
        self.value = None

    @ui.button(label="Report Content", style=ButtonStyle.grey)
    async def report1(self, ctx: Interaction, button: ui.Button):
        self.value = "report"
        await ctx.response.send_modal(ReportContentM(self.link))


class RemoveManage(ui.View):
    def __init__(self, author: User):
        super().__init__(timeout=180)
        self.value = None
        self.author = author

    @ui.button(label="Welcoming Channel", style=ButtonStyle.gray)
    async def welcomer(self, ctx: Interaction, button: ui.Button):
        self.value = "welcomer"
        Embed()
        check = Welcomer(ctx.guild).get_welcomer
        if check == None:
            button.label = "No welcoming channel found"
            button.style = ButtonStyle.danger
            await ctx.response.edit_message(view=self)
            return
        button.style = ButtonStyle.green
        await Manage(ctx.guild).remove_welcomer()
        button.label = "Welcomer Channel Removed"
        await ctx.response.edit_message(view=self)

    @ui.button(label="Greeting Message", style=ButtonStyle.gray)
    async def welcomemsg(self, ctx: Interaction, button: ui.Button):
        self.value = "welcomemsg"
        check = Welcomer(ctx.guild).get_welcoming_msg
        if check == None:
            button.style = ButtonStyle.danger
            button.label = "No welcoming message set"
            await ctx.response.edit_message(view=self)
            return
        button.style = ButtonStyle.green
        button.label = "Welcoming Message Removed"
        await Manage(ctx.guild).remove_welcomemsg()
        await ctx.response.edit_message(view=self)

    @ui.button(label="Leaving Channel", style=ButtonStyle.gray)
    async def leaving(self, ctx: Interaction, button: ui.Button):
        self.value = "leaver"
        check = Welcomer(ctx.guild).get_leaver
        if check == None:
            button.style = ButtonStyle.danger
            button.label = "No leaving channel found"
            await ctx.response.edit_message(view=self)
        else:
            button.style = ButtonStyle.green
            button.label = "Leaving Channel Removed"
            await Manage(ctx.guild).remove_leaver()
            await ctx.response.edit_message(view=self)

    @ui.button(label="Leaving Message", style=ButtonStyle.gray)
    async def leavingmsg(self, ctx: Interaction, button: ui.Button):
        self.value = "leavingmsg"
        check = Welcomer(ctx.guild).get_leaving_msg
        if check == None:
            button.style = ButtonStyle.danger
            button.label = "No leaving message set"
            await ctx.response.edit_message(view=self)
            return
        button.style = ButtonStyle.green
        button.label = "Leaving Message Removed"
        await Manage(ctx.guild).remove_leavingmsg()
        await ctx.response.edit_message(view=self)

    @ui.button(label="Level Update Channel", style=ButtonStyle.gray)
    async def level(self, ctx: Interaction, button: ui.Button):
        self.value = "levelup"
        check = Levelling(server=ctx.guild).get_level_channel[0]
        if check == None:
            button.style = ButtonStyle.danger
            button.label = "No level update channel found"
            await ctx.response.edit_message(view=self)
            return
        button.style = ButtonStyle.green
        button.label = "Level Update Channel Removed"
        await Manage(ctx.guild).remove_levelup()
        await ctx.response.edit_message(view=self)

    @ui.button(label="Level Update Message", style=ButtonStyle.gray)
    async def levelupdate(self, ctx: Interaction, button: ui.Button):
        self.value = "levelnotif"
        check = Levelling(server=ctx.guild).get_level_channel[1]
        if check == None:
            button.style = ButtonStyle.danger
            button.label = "No level update message set"
            await ctx.response.edit_message(view=self)
            return
        button.style = ButtonStyle.green
        button.label = "Level Update Message Removed"
        await Manage(ctx.guild).remove_levelup_msg()
        await ctx.response.edit_message(view=self)

    @ui.button(label="Role Reward Message", style=ButtonStyle.gray)
    async def rolereward(self, ctx: Interaction, button: ui.Button):
        self.value = "rolereward"
        check = Levelling(ctx.guild).get_level_channel[2]
        if check == None:
            button.style = ButtonStyle.danger
            button.label = "No role reward message set"
            await ctx.response.edit_message(view=self)
            return
        button.style = ButtonStyle.green
        button.label = "Role Reward Message Removed"
        await Manage(ctx.guild).remove_rolereward_msg()
        await ctx.response.edit_message(view=self)

    @ui.button(label="Modlog", style=ButtonStyle.gray)
    async def modlog(self, ctx: Interaction, button: ui.Button):
        self.value = "modlog"
        check = Logger(ctx.guild).get_modlog_channel
        if check == None:
            button.style = ButtonStyle.danger
            button.label = "No modlog found"
            await ctx.response.edit_message(view=self)
            return
        button.style = ButtonStyle.green
        button.label = "Modlog Removed"
        await Manage(ctx.guild).remove_modloger()
        await ctx.response.edit_message(view=self)

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class RolesButton(ui.View):
    def __init__(self, member: User, Uinfo: Embed, Roles: list[str]):
        super().__init__(timeout=60)
        self.value = None
        self.member = member
        self.Roles = Roles
        self.Uinfo = Uinfo

    @ui.button(label="Roles", style=ButtonStyle.blurple)
    async def roles(self, ctx: Interaction, button: ui.Button):
        self.value = "roles"
        roles = Embed(
            title="{}'s roles".format(self.member),
            description=" ".join(self.Roles) + " @everyone",
            color=self.member.color,
        )
        await ctx.response.edit_message(embeds=[self.Uinfo, roles], view=None)
        self.stop()


class BioModal(ui.Modal, title="Bio"):
    def __init__(self):
        super().__init__()

    line1 = ui.TextInput(
        label="Line 1",
        style=TextStyle.short,
        required=True,
        min_length=1,
        max_length=60,
    )
    line2 = ui.TextInput(
        label="Line 2",
        style=TextStyle.short,
        required=False,
        min_length=1,
        max_length=60,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        bio = self.line1.value + "\n" + (self.line2.value if self.line2.value else "")
        embed = Embed(title="New bio has been set to:", color=Color.random())
        await Inventory(ctx.user).set_bio(bio)
        embed.description = bio
        await ctx.response.send_message(embed=embed)


class Guess_Buttons(ui.View):
    def __init__(self, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

        for i in range(1, 11):
            button = ui.Button(label=str(i), style=ButtonStyle.grey)
            button.callback = partial(
                self.button_callback, number=i
            )  # Dynamically assign button callbacks
            self.add_item(button)

    async def button_callback(self, ctx: Interaction, number: int):
            self.value = number
            for child in self.children:  # Disable all buttons to prevent further clicks
                child.disabled = True
            self.stop()

    async def interaction_check(self, ctx: Interaction):
            return ctx.user.id == self.author.id
