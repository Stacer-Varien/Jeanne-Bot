from functools import partial
from discord import (
    CategoryChannel,
    File,
    Member,
    Message,
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
from discord.ext.commands import Context, Bot
from assets.generators.profile_card import Profile
from config import WEBHOOK
from functions import Inventory, Levelling, Manage, Moderation, Welcomer


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


class BotReportMenu(ui.Select):
    def __init__(self) -> None:
        options = [
            SelectOption(label="ToS Violator", value="violator"),
            SelectOption(label="Exploit", value="exploit"),
            SelectOption(label="Bug and/or Fault", value="bugorfault"),
            SelectOption(label="Illicit NSFW Content", value="illicit"),
            SelectOption(label="Other", value="other"),
        ]
        super().__init__(
            placeholder="Select type of the report",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, ctx: Interaction):

        await ctx.response.send_modal(ReportModal(self.options[0].label))
        try:
            await ctx.message.delete()
        except:
            pass


class BotReportSelect(ui.View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=60)
        self.add_item(BotReportMenu())


class ReportModal(ui.Modal, title="Bot Report"):
    def __init__(self, type: str):
        self.type = type
        super().__init__()

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
        report = Embed(title=self.type, color=Color.brand_red())
        report.description = self.report.value
        if self.steps.value != None or self.steps.value == "":
            report.add_field(name="Steps", value=self.steps.value, inline=False)
        report.set_footer(text="Reporter {}| `{}`".format(ctx.user, ctx.user.id))
        SyncWebhook.from_url(WEBHOOK).send(embed=report)
        embed = Embed(
            description="Thank you for submitting your bot report. The developer will look into it but will not tell you the results.\n\nPlease know that your user ID has been logged if you are trolling around."
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)


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


class ReportContentPlus(ui.View):

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

    @ui.button(label="Report 1st Content", style=ButtonStyle.grey, row=1)
    async def report1(self, ctx: Interaction, button: ui.Button):
        self.value = "report1"
        await ctx.response.send_modal(ReportContentM(self.link1))
        await ctx.edit_original_response(view=self)

    @ui.button(label="Report 2nd Content", style=ButtonStyle.grey, row=1)
    async def report2(self, ctx: Interaction, button: ui.Button):
        self.value = "report2"
        await ctx.response.send_modal(ReportContentM(self.link2))
        await ctx.edit_original_response(view=self)

    @ui.button(label="Report 3rd Content", style=ButtonStyle.grey, row=2)
    async def report3(self, ctx: Interaction, button: ui.Button):
        self.value = "report3"
        await ctx.response.send_modal(ReportContentM(self.link3))
        await ctx.edit_original_response(view=self)

    @ui.button(label="Report 4th Content", style=ButtonStyle.grey, row=2)
    async def report4(self, ctx: Interaction, button: ui.Button):
        self.value = "report4"
        await ctx.response.send_modal(ReportContentM(self.link4))
        await ctx.edit_original_response(view=self)


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
        check = Levelling(server=ctx.guild).get_levelup_channel
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
        check = Levelling(server=ctx.guild).get_levelup_msg
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
        check = Levelling(server=ctx.guild).get_rank_up_update
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
        check = Moderation(ctx.guild).get_modlog_channel
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


class Guess_Buttons(ui.View):
    def __init__(self, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

        for i in range(1, 11):
            button = ui.Button(label=str(i), style=ButtonStyle.grey)
            button.callback = partial(self.button_callback, number=i)
            self.add_item(button)

    async def button_callback(self, ctx: Interaction, number: int):
        self.value = number
        for child in self.children:
            child.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


async def buy_function_context(bot: Bot, ctx: Context, name: str, message: Message):
    image_url = Inventory().get_wallpaper(name)[2]
    m = await message.edit(
        embed=Embed(
            description="Creating preview... This will take some time <a:loading:1161038734620373062>"
        ),
        view=None,
    )
    image = await Profile(bot).generate_profile(ctx.author, image_url, True)
    file = File(fp=image, filename=f"preview_profile_card.png")
    preview = (
        Embed(
            description="This is the preview of the profile card.",
            color=Color.random(),
        )
        .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
        .set_footer(text="Is this the background you wanted?")
    )
    view = Confirmation(ctx.author)
    m = await m.edit(attachments=[file], embed=preview, view=view)
    await view.wait()

    if view.value == True:
        await Inventory(ctx.author).add_user_wallpaper(name)
        embed1 = Embed(
            description=f"Background wallpaper bought and selected",
            color=Color.random(),
        )
        await m.edit(embed=embed1, view=None)
        return
    await m.edit(embed=Embed(description="Cancel"), view=None, attachments=[])


async def use_function_context(ctx: Context, name: str, message: Message):
    await Inventory(ctx.author).use_wallpaper(name)
    embed = Embed(description=f"{name} has been selected", color=Color.random())
    await message.edit(embed=embed, view=None)


async def buy_function_app(bot: Bot, ctx: Interaction, name: str):
    image_url = Inventory().get_wallpaper(name)[2]
    await ctx.edit_original_response(
        "Creating preview... This will take some time <a:loading:1161038734620373062>"
    )
    image = await Profile(bot).generate_profile(ctx.user, image_url, True)
    file = File(fp=image, filename=f"preview_profile_card.png")
    preview = (
        Embed(
            description="This is the preview of the profile card.",
            color=Color.random(),
        )
        .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
        .set_footer(text="Is this the background you wanted?")
    )
    view = Confirmation(ctx.user)
    await ctx.edit_original_response(
        content=None, attachments=[file], embed=preview, view=view
    )
    await view.wait()
    if view.value == None:
        await ctx.edit_original_response(
            content="Timeout", view=None, embed=None, attachments=[]
        )
        return
    if view.value == True:
        await Inventory(ctx.user).add_user_wallpaper(name)
        embed1 = Embed(
            description=f"Background wallpaper bought and selected",
            color=Color.random(),
        )
        await ctx.edit_original_response(embed=embed1, view=None)
    else:
        await ctx.edit_original_response(
            content="Cancelled", view=None, embed=None, attachments=[]
        )


async def use_function_app(ctx: Interaction, name: str):
    await Inventory(ctx.user).use_wallpaper(name)
    embed = Embed(description=f"{name} has been selected", color=Color.random())
    await ctx.edit_original_response(embed=embed, view=None)


class TopicButton(ui.View):
    def __init__(self, author: Member, name: str, category: CategoryChannel):
        self.value = None
        self.author = author
        self.name = name
        self.category = category
        super().__init__(timeout=180)

    @ui.button(label="Add Guidelines")
    async def guidelines(self, button: ui.Button, ctx: Interaction):
        self.value = "guidelines"
        await ctx.response.send_modal(ForumGuildlines(self.name, self.category))

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class WelcomerSetButtons(ui.View):
    def __init__(self, author: Member, message: Message):
        self.value = None
        self.author = author
        self.message = message
        super().__init__(timeout=180)

    @ui.button(label="Set Welcoming Message")
    async def setwelcomemsg(self, button: ui.Button, ctx: Interaction):
        self.value = "welcomemsg"
        await self.message.edit(view=self)
        await ctx.response.send_modal(Welcomingmsg())

    @ui.button(label="Set Leaving Message")
    async def setleavingmsg(self, button: ui.Button, ctx: Interaction):
        self.value = "leavingmsg"
        await self.message.edit(view=self)
        await ctx.response.send_modal(Leavingmsg())

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class LevelSetButtons(ui.View):
    def __init__(self, author: Member, message: Message, channel: TextChannel):
        self.value = None
        self.author = author
        self.message = message
        self.channel = channel
        super().__init__(timeout=180)

    @ui.button(label="Set Level Update Message")
    async def setwelcomemsg(self, button: ui.Button, ctx: Interaction):
        self.value = "levelmsg"
        await self.message.edit(view=self)
        await ctx.response.send_modal(Levelmsg())

    @ui.button(label="Set Default Role Reward Message")
    async def setdefaultleavingmsg(self, button: ui.Button, ctx: Interaction):
        self.value = "defaultrolerewardmsg"
        await Manage(ctx.guild).add_rankup_rolereward(None)
        await self.message.edit(view=self)

    @ui.button(label="Set Custom Role Reward Message")
    async def setleavingmsg(self, button: ui.Button, ctx: Interaction):
        self.value = "customrolerewardmsg"
        await self.message.edit(view=self)
        await ctx.response.send_modal(RankUpmsg())

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id
