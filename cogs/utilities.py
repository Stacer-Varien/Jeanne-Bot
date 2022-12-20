from discord import *
from aiohttp import ClientSession
from discord.ext.commands import Cog, Bot, GroupCog
from db_functions import check_botbanned_user, get_report_channel
from assets.buttons import Confirmation
from config import WEATHER, WEBHOOK
from discord.ui import View
from asyncio import TimeoutError
from py_expression_eval import Parser
from typing import Literal, Optional
from discord.app_commands import *
from json import loads
from requests import get

bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=1428479601718&scope=bot%20applications.commands"

topgg_invite = "https://top.gg/bot/831993597166747679"

discordbots_url = "https://discord.bots.gg/bots/831993597166747679"

haze_url = "https://discord.gg/jh7jkuk2pp"


def send_bot_report(report_type, report, reporter):
    report = Embed(title=f"{report_type} Report",
                   description=report, color=Color.blurple())
    report.set_footer(text=f"Reporter: {reporter}")

    return report

class invite_button(View):
    def __init__(self):
        super().__init__()

        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="Bot Invite", url=bot_invite_url))
        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="Top.gg", url=topgg_invite))
        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="DiscordBots", url=discordbots_url))
        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="HAZE", url=haze_url))


class Weather_Group(GroupCog, name="weather"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Get weather information on a city")
    @app_commands.describe(city="Add a city")
    async def city(self, ctx: Interaction, city: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            min_tempe = self.bot.get_emoji(1009760796017963119)
            max_tempe = self.bot.get_emoji(1009761541169618964)
            guste = self.bot.get_emoji(1009766251431743569)
            globe = self.bot.get_emoji(1009723165305491498)

            urlil = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        feels_like = js['main']['feels_like']
                        min_temp = js['main']['temp_min']
                        max_temp = js['main']['temp_max']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        visibility = js['visibility']
                        clouds = js['clouds']['all']
                        windir = js['wind']['deg']
                        wind_gust = js['wind']['speed']

                        embed = Embed(
                            title=f'⛅ Weather details of {city} ⛅', description=f'{globe} Country: {count}', colour=ctx.user.color)
                        embed.add_field(
                            name=":newspaper: Description", value=desc, inline=True)
                        embed.add_field(
                            name=f"{min_tempe} Minimum Temperature", value=f"{min_temp}°C", inline=True)
                        embed.add_field(
                            name=f"{max_tempe} Maximum Temperature", value=f"{max_temp}°C", inline=True)
                        embed.add_field(
                            name=":raised_back_of_hand: Feels Like", value=f"{feels_like}°C", inline=True)
                        embed.add_field(name=":droplet: Humidity",
                                        value=hum, inline=True)
                        embed.add_field(name=":eye: Visibility",
                                        value=f"{visibility}m", inline=True)
                        embed.add_field(name=":cloud: Clouds",
                                        value=f"{clouds}%", inline=True)
                        embed.add_field(
                            name=":arrow_right: Wind Direction", value=f"{windir}°", inline=True)
                        embed.add_field(
                            name=f"{guste} Wind Gust", value=f"{wind_gust}m/s", inline=True)
                        await ctx.followup.send(embed=embed)

    @app_commands.command(description="Get weather information on a city but with a ZIP code and Country code")
    @app_commands.describe(zip_code="Add a ZIP code", country_code="Add a country code")
    async def zipcode(self, ctx: Interaction, zip_code: str, country_code: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            min_tempe = self.bot.get_emoji(1009760796017963119)
            max_tempe = self.bot.get_emoji(1009761541169618964)
            guste = self.bot.get_emoji(1009766251431743569)
            urlil = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        feels_like = js['main']['feels_like']
                        min_temp = js['main']['temp_min']
                        max_temp = js['main']['temp_max']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        visibility = js['visibility']
                        clouds = js['clouds']['all']
                        windir = js['wind']['deg']
                        wind_gust = js['wind']['speed']
                        embed = Embed(
                            title=f'⛅ Weather details of {zip_code} ⛅', description=f':earth_africa: Country: {count}', colour=ctx.user.color)
                        embed.add_field(
                            name=":newspaper: Description", value=desc, inline=True)
                        embed.add_field(
                            name=f"{min_tempe} Minimum Temperature", value=f"{min_temp}°C", inline=True)
                        embed.add_field(
                            name=f"{max_tempe} Maximum Temperature", value=f"{max_temp}°C", inline=True)
                        embed.add_field(
                            name=":raised_back_of_hand: Feels Like", value=f"{feels_like}°C", inline=True)
                        embed.add_field(name=":droplet: Humidity",
                                        value=hum, inline=True)
                        embed.add_field(name=":eye: Visibility",
                                        value=f"{visibility}m", inline=True)
                        embed.add_field(name=":cloud: Clouds",
                                        value=f"{clouds}%", inline=True)
                        embed.add_field(
                            name=":arrow_right: Wind Direction", value=f"{windir}°", inline=True)
                        embed.add_field(
                            name=f"{guste} Wind Gust", value=f"{wind_gust}m/s", inline=True)
                        await ctx.followup.send(embed=embed)

class Embed_Group(GroupCog, name="embed"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Generates an embed message. This needs the Discohooks.org embed generator")
    @app_commands.describe(channel="Send to which channel?", jsonscript="Add a JSON script", jsonfile="Add a JSON file")
    @app_commands.checks.has_permissions(administrator=True)
    async def generate(self, ctx: Interaction, channel: TextChannel, jsonscript: Optional[str] = None, jsonfile: Optional[Attachment] = None):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer(ephemeral=True)

            if not jsonscript and not jsonfile:
                embed = Embed(
                    description="You are missing the JSON script or JSON file\nPlease use [Discohooks](https://discohook.org/)")
                await ctx.followup.send(embed=embed)
            elif jsonscript and jsonfile:
                embed = Embed(
                    description="You are using both the JSON script and JSON file\nPlease use one")
                await ctx.followup.send(embed=embed)
            else:
                if jsonscript and not jsonfile:
                    json = loads(jsonscript)

                elif jsonfile and not jsonscript:
                    json_file = jsonfile.url
                    json_request = get(json_file)
                    json_content = json_request.content
                    json = loads(json_content)

                try:
                    content = json["content"]
                except:
                    pass

                try:
                    embed = Embed.from_dict(json['embeds'][0])
                    await channel.send(content=content, embed=embed)
                except:
                    await channel.send(content=content)
                await ctx.followup.send(content="Sent", ephemeral=True)

    @app_commands.command(description="Edits an embed message. This needs the Discohook.org embed generator")
    @app_commands.describe(channel="Which channel is the embed message in?", messageid="What is the message ID?", jsonscript="Add a JSON script", jsonfile="Add a JSON file")
    @app_commands.checks.has_permissions(administrator=True)
    async def edit(self, ctx: Interaction, channel: TextChannel, messageid:str, jsonscript: Optional[str] = None, jsonfile: Optional[Attachment] = None):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer(ephemeral=True)

            try:
                message:Message= await channel.fetch_message(int(messageid))
            except Exception as e:
                embed = Embed(description=e)
                await ctx.followup.send(embed=embed)                
            else:
                if not jsonscript and not jsonfile:
                    embed = Embed(
                        description="You are missing the JSON script or JSON file\nPlease use [Discohooks](https://discohook.org/)")
                    await ctx.followup.send(embed=embed)
                elif jsonscript and jsonfile:
                    embed = Embed(
                        description="You are using both the JSON script and JSON file\nPlease use one")
                    await ctx.followup.send(embed=embed)
                else:
                    if jsonscript and not jsonfile:
                        json = loads(jsonscript)

                    elif jsonfile and not jsonscript:
                        json_file = jsonfile.url
                        json_request = get(json_file)
                        json_content = json_request.content
                        json = loads(json_content)

                    try:
                        content = json["content"]

                        if content=='':
                            content=None
                    except:
                        pass

                    try:
                        embed = Embed.from_dict(json['embeds'][0])
                        await message.edit(content=content, embed=embed)
                    except:
                        await message.edit(content=content)
                    await ctx.followup.send(content="Message edited", ephemeral=True)

class slashutilities(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.parser = Parser()

    @app_commands.command(description="Type something and I will say it")
    @app_commands.describe(channel="Send to which channel?", message="What should I say?")
    @app_commands.checks.has_permissions(administrator=True)
    async def say(self, ctx: Interaction, channel: TextChannel, message: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer(ephemeral=True)
            await ctx.followup.send(content="Sent")
            await channel.send(message)


    @app_commands.command(description="Do a calculation")
    @app_commands.describe(calculate="Add a calculation")
    async def calculator(self, ctx: Interaction, calculate:str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            try:
                answer = self.parser.parse(calculate).evaluate({})
                calculation = Embed(title="Result", color=0x00FFFF)
                calculation.add_field(name=f"`{calculate}`", value=answer)
                await ctx.followup.send(embed=calculation)
            except Exception as e:
                failed = Embed(
                    description=f"{e}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command")
                await ctx.followup.send(embed=failed)

    @app_commands.command(description="Invite me to your server or join the support server")
    async def invite(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            invite = Embed(
                title="Invite me!",
                description="Click on one of these buttons to invite me to you server or join my creator's server",
                color=0x00bfff)

            await ctx.followup.send(embed=invite, view=invite_button())



    @app_commands.command(description="Submit a bot report if you found something wrong")
    @app_commands.describe(type="What is the nature of the report?")
    @checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def botreport(self, ctx: Interaction, type:Literal['bug', 'fault', 'exploit', 'violator']):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if type == 'bug':
                report_type = "Bug"
            elif type == 'fault':
                report_type = "Fault"
            elif type == 'exploit':
                report_type = "Exploit"
            elif type == 'violator':
                report_type = "Violator"

            try:            
                if report_type == 'bug' or 'fault' or 'exploit':
                    m = await ctx.user.send("What have you found?\nPlease include steps on how you were able to find it and include proof if possible")
                
                elif report_type == 'violator':
                    m = await ctx.user.send("Who has violated the ToS of Jeanne? Please include proof if possible")

                await ctx.followup.send("Please go to your [DMs]({}) to report what you have found about Jeanne".format(m.jump_url), ephemeral=True)

                def check(m:Message):
                    attachments = bool(m.attachments)
                    content=bool(m.content)
                    if attachments and content == True:
                        return m.author == ctx.user and m.content and m.attachments
                    elif content == True:
                        return m.author == ctx.user and m.content
                    elif attachments==True:
                        return m.author == ctx.user and m.attachments
                    elif attachments==True and content=='':
                        return m.author == ctx.user and m.attachments
                try:
                    msg:Message = await self.bot.wait_for('message', check=check, timeout=600)

                    view=Confirmation(ctx.user)
                    embed = Embed(title="Before it gets submitted, did you make sure everything you have told is legit?")
                    await ctx.user.send(embed=embed, view=view)
                    await view.wait()

                    if view.value == None:
                        await ctx.user.send("Timeout")

                    elif view.value == True:
                        await ctx.user.send("Thank you for submitting your bot report. I will look into it. Unfortunately, you have to wait for the outcome if it was successful or not.")
                        report = Embed(title=f'{report_type} reported',
                                            color=Color.brand_red())
                        report.set_footer(text='Reporter {}| `{}`'.format(ctx.user, ctx.user.id))
                                
                        if msg.content!='':
                            report.description=msg.content
                        else:
                            pass

                        try:
                            image_urls = [x.url for x in msg.attachments]
                            images = "\n".join(image_urls)
                            SyncWebhook.from_url(WEBHOOK).send(content=images,embed=report)
                        except:
                            SyncWebhook.from_url(WEBHOOK).send(embed=report)

                    elif view.value == False:
                        await ctx.user.send("Bot Report Cancelled")
                except TimeoutError:
                    await ctx.user.send("Timeout")
            except:
                await ctx.followup.send("Your DMs are not opened. Please open them for this process", ephemeral=True)



    @app_commands.command(description="Report a member in your server")
    @app_commands.describe(member="Who are you reporting?", anonymous="Do you want your name to be hidden?")
    async def report(self, ctx: Interaction, member: Member, anonymous:Optional[Literal['True', 'False']]=None)->None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer(ephemeral=True)
            report_channel = get_report_channel(ctx.guild.id)
            if report_channel == None:
                await ctx.followup.send("This server doesn't have a report channel set")
            else:
                    m = await ctx.user.send("Why are you reporting {}?".format(member))

                    await ctx.followup.send("Please go to your [DMs]({}) to report. Please remember that it is private and only authorised users can view your report".format(m.jump_url), ephemeral=True)

                    def check(m:Message):
                        attachments = bool(m.attachments)
                        content=bool(m.content)
                        if attachments and content == True:
                            return m.author == ctx.user and m.content and m.attachments
                        elif content == True:
                            return m.author == ctx.user and m.content
                        elif attachments==True:
                            return m.author == ctx.user and m.attachments
                    try:
                        msg:Message = await self.bot.wait_for('message', check=check, timeout=600)
                        

                        report_channel_id = report_channel[0]
                        channel = self.bot.get_channel(report_channel_id)
                    
                        view=Confirmation()
                        embed = Embed(
                            title="Before it gets submitted, did you make sure that the evidence against this member is valid, accurate and honest?")
                        await ctx.user.send(embed=embed, view=view)
                        await view.wait()

                        if view.value == None:
                            await ctx.user.send("Timeout")

                        elif view.value == True:
                            await ctx.user.send("Report sent")
                            report = Embed(title='Member reported',
                                           color=Color.brand_red())
                            report.add_field(name="Reported Member", value=(
                                f"{member}\n{member.id}"), inline=False)
                            
                            if msg.content=='':
                                msg.content="No explaination applicable"

                            report.add_field(
                                name='Reason', value=msg.content, inline=False)

                            if anonymous == 'True':
                                report.set_footer(
                                    text="Made by an anonymous member of {}".format(ctx.guild.name))

                            elif anonymous == 'False' or None:
                                report.set_footer(text="Made by {} | {} of {}".format(
                                    ctx.user, ctx.user.id, ctx.guild.name))

                            try:
                                image_urls = [x.url for x in msg.attachments]
                                image_urls = "\n".join(image_urls)
                                await channel.send(embed=report)
                                await channel.send(image_urls)
                            except:
                                await channel.send(embed=report)

                        elif view.value == False:
                            await ctx.user.send("Report Cancelled")
                    except TimeoutError:
                        await ctx.user.send("Timeout")

async def setup(bot:Bot):
    await bot.add_cog(Weather_Group(bot))
    await bot.add_cog(Embed_Group(bot))
    await bot.add_cog(slashutilities(bot))
