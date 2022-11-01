from discord import *
from aiohttp import ClientSession
from discord.ext.commands import Cog, Bot, hybrid_command, hybrid_group, Context, has_permissions
from db_functions import check_botbanned_user, get_report_channel
from assets.buttons import Confirmation
from assets.modals import Bot_Report_Modal, Say_Modal
from config import WEATHER
from discord.abc import GuildChannel
from discord.ui import View
from asyncio import TimeoutError
from py_expression_eval import Parser
from typing import Optional, Literal

bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands"

topgg_invite = "https://top.gg/bot/831993597166747679"

discordbots_url = "https://discord.bots.gg/bots/831993597166747679"

haze_url = "https://discord.gg/VVxGUmqQhF"


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


class slashutilities(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.parser = Parser()

    @hybrid_group(description="Main weather command")
    async def weather(self, ctx: Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="```weather city CITY`\n`weather zip_code ZIP_CODE COUNTRY_CODE```")
            await ctx.send(embed=embed)

    @weather.command(description="Get weather information on a city")
    async def city(self, ctx: Context, city:str):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            min_tempe=self.bot.get_emoji(1009760796017963119)
            max_tempe=self.bot.get_emoji(1009761541169618964)
            guste=self.bot.get_emoji(1009766251431743569)
            globe=self.bot.get_emoji(1009723165305491498)

            urlil = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        feels_like = js['main']['feels_like']
                        min_temp=js['main']['temp_min']
                        max_temp=js['main']['temp_max']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        visibility=js['visibility']
                        clouds=js['clouds']['all']
                        windir = js['wind']['deg']
                        wind_gust=js['wind']['speed']

                        embed = Embed(
                            title=f'⛅ Weather details of {city} ⛅', description=f'{globe} Country: {count}', colour=ctx.author.color)
                        embed.add_field(name=":newspaper: Description", value=desc, inline=True)
                        embed.add_field(name=f"{min_tempe} Minimum Temperature", value=f"{min_temp}°C", inline=True)
                        embed.add_field(name=f"{max_tempe} Maximum Temperature", value=f"{max_temp}°C", inline=True)
                        embed.add_field(name=":raised_back_of_hand: Feels Like", value=f"{feels_like}°C", inline=True)
                        embed.add_field(name=":droplet: Humidity", value=hum, inline=True)
                        embed.add_field(name=":eye: Visibility", value=f"{visibility}m", inline=True)
                        embed.add_field(name=":cloud: Clouds", value=f"{clouds}%", inline=True)
                        embed.add_field(name=":arrow_right: Wind Direction", value=f"{windir}°", inline=True)
                        embed.add_field(name=f"{guste} Wind Gust", value=f"{wind_gust}m/s", inline=True)
                        await ctx.send(embed=embed)

    @weather.command(description="Get weather information on a city but with a ZIP code and Country code", aliases=['zp', 'zip'])
    async def zip_code(self, ctx: Context, zip_code:str, country_code:str):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            min_tempe=self.bot.get_emoji(1009760796017963119)
            max_tempe=self.bot.get_emoji(1009761541169618964)
            guste=self.bot.get_emoji(1009766251431743569)
            urlil = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        feels_like = js['main']['feels_like']
                        min_temp=js['main']['temp_min']
                        max_temp=js['main']['temp_max']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        visibility=js['visibility']
                        clouds=js['clouds']['all']
                        pres = js['wind']['pressure']
                        windir = js['wind']['deg']
                        wind_gust=js['wind']['speed']
                        embed = Embed(
                            title=f'⛅ Weather details of {zip_code} ⛅', description=f':earth_africa: Country: {count}', colour=ctx.author.color)
                        embed.add_field(name=":newspaper: Description", value=desc, inline=True)
                        embed.add_field(name=f"{min_tempe} Minimum Temperature", value=f"{min_temp}°C", inline=True)
                        embed.add_field(name=f"{max_tempe} Maximum Temperature", value=f"{max_temp}°C", inline=True)
                        embed.add_field(name=":raised_back_of_hand: Feels Like", value=f"{feels_like}°C", inline=True)
                        embed.add_field(name=":droplet: Humidity", value=hum, inline=True)
                        embed.add_field(name=":eye: Visibility", value=f"{visibility}m", inline=True)
                        embed.add_field(name=":cloud: Clouds", value=f"{clouds}%", inline=True)
                        embed.add_field(name=":cloud: Pressure", value=f"{pres}hPa", inline=True)
                        embed.add_field(name=":arrow_right: Wind Direction", value=f"{windir}°", inline=True)
                        embed.add_field(name=f"{guste} Wind Gust", value=f"{wind_gust}m/s", inline=True)
                        await ctx.send(embed=embed)

    @hybrid_command(description="Do a calculation")
    async def calculator(self, ctx: Context, calculate):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                answer = self.parser.parse(calculate).evaluate({})
                calculation = Embed(title="Result", color=0x00FFFF)
                calculation.add_field(name=calculate, value=answer)
                await ctx.send(embed=calculation)
            except Exception as e:
                failed = Embed(
                    description=f"{e}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command")
                await ctx.send(embed=failed)

    @hybrid_command(description="Invite me to your server or join the support server")
    async def invite(self, ctx: Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            invite = Embed(
                title="Invite me!",
                description="Click on one of these buttons to invite me to you server or join my creator's server",
                color=0x00bfff)

            await ctx.send(embed=invite, view=invite_button())

    @hybrid_group(description="Main say command")
    async def say(self, ctx: Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="```say plain`\n`say embed```")
            await ctx.send(embed=embed)

    @say.command(name='plain', description="Type something and I will say it in plain text")
    @has_permissions(administrator=True)
    async def say_plain(self, ctx: Interaction, channel: Literal[ChannelType.text, ChannelType.news]):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.send_modal(Say_Modal('plain', channel))

    @say.command(name='embed', description="Type something and I will say it in embed")
    @has_permissions(administrator=True)
    async def say_embed(self, ctx: Interaction, channel: Literal[ChannelType.text, ChannelType.news]):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.send_modal(Say_Modal('embed', channel))

    @hybrid_command(name='bot_report')
    async def bot_report(self, ctx: Interaction, type:Literal['bug', 'fault', 'exploit', 'violator']):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if type == 'bug':
                report_type = "Bug"
            elif type == 'fault':
                report_type = "Fault"
            elif type == 'exploit':
                report_type = "Exploit"
            elif type == 'violator':
                report_type = "Violator"

            await ctx.response.send_modal(Bot_Report_Modal(report_type))


    @hybrid_command(description="Report a member in your server")
    async def report(self, ctx: Interaction, member: Member, anonymous:Literal['True', 'False']):
        await ctx.response.defer(ephemeral=True)
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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
                        msg = await self.bot.wait_for('message', check=check, timeout=600)
                        

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

                            if anonymous == 'False':
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
    await bot.add_cog(slashutilities(bot))
