from config import db
from time import time
from datetime import timedelta
from sys import version_info as py_version
from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as jeanne_slash, __version__ as discord_version

format = "%a, %d %b %Y | %H:%M:%S"
start_time = time()

class slashinfo(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="See the bot's status from development to now")
    async def stats(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            botowner = self.bot.get_user(597829930964877369)
            embed = Embed(title="Bot stats", color=0x236ce1)
            embed.add_field(
                name="General Information", value=f"**>** **Name:** {self.bot.user}\n**>** **ID:** {self.bot.user.id}\n**>** **Bot Version:** v2.7", inline=True)
            embed.add_field(
                name="Developer", value=f"**>** **Name:** {botowner}\n**>** **ID:** {botowner.id}", inline=True)
            embed.add_field(
                name="Version", value=f"**>** **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n**>** **Nextcord Version:** {discord_version}", inline=True)
            embed.add_field(name="Count",
                            value=f"**>** **Server Count:** {len(self.bot.guilds)} servers\n**>** **User Count:** {len(set(self.bot.get_all_members()))}\n**>** **Goal to verification:** {len(self.bot.guilds)}/100 servers", inline=True)
            embed.add_field(name="Ping",
                            value=f"**>** **Bot Latency:** {round(self.bot.latency * 1000)}ms", inline=True)
            current_time = time()
            difference = int(round(current_time - start_time))
            uptime = str(timedelta(seconds=difference))
            embed.add_field(
                name="Uptime", value=f"{uptime} hours")
            embed.set_thumbnail(
                url=self.bot.user.avatar)
            await interaction.followup.send(embed=embed)

    @jeanne_slash(description="See the information of a member or yourself")
    async def userinfo(self, interaction : Interaction, member: Member = SlashOption(description="Add a member", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member == None:
                member = interaction.user
            hasroles = [
                role.mention for role in member.roles][1:][:: -1]

            if member.bot == True:
                botr = ":o:"
            else:
                botr = ":x:"

            userinfo = Embed(title="{}'s Info".format(member.name),
                            color=0xccff33)
            userinfo.add_field(name="General Information",
                            value=f"**>** **Name:** {member}\n**>** **Nickname:** {member.nick}\n**>** **ID:** {member.id}\n**>** **Creation Date:** {member.created_at.strftime(format)}\n**>** **Is Bot?:** {botr}",
                            inline=True)
            userinfo.add_field(name="Member Information",
                            value=f"**>** **Joined Server:** {member.joined_at.strftime(format)}\n**>** **Number of Roles:** {len(member.roles)}",
                            inline=True)
            userinfo.add_field(name="Roles Held",
                            value=''.join(hasroles[:20]) + '@everyone', inline=False)
            userinfo.set_thumbnail(url=member.display_avatar)
            await interaction.followup.send(embed=userinfo)

    @jeanne_slash(description="Get information about this server")
    async def serverinfo(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:        
            guild = interaction.guild
            emojis = [str(x) for x in guild.emojis]
            features = [str(x) for x in guild.features]
            true_member_count = len([m for m in guild.members if not m.bot])
            bots = len([m for m in guild.members if m.bot])

            if guild.premium_subscription_count < 2:
                boostlevel = "Level 0"
            elif guild.premium_tier == 1:
                boostlevel = "Level 1"
            elif guild.premium_tier == 2:
                boostlevel = "Level 2"
            elif guild.premium_tier == 3:
                boostlevel = "Level 3"

            embed = Embed(title="Server's Info", color=0x00B0ff)
            embed.add_field(name="General Information",
                            value=f"**>** **Name:** {guild.name}\n**>** **ID:** {guild.id}\n**>** **Creation Date:** {guild.created_at.strftime(format)}\n**>** **Member Count:** {len(guild.members)}\n**>** **Verification:** {guild.verification_level}\n**>** **Roles:** {len(guild.roles)}\n**>** **Emojis:** {len(emojis)}\n{''.join(emojis[:10])}", inline=True)
            embed.add_field(
                name="Owner", value=f"**>** **Name:** {guild.owner}\n**>** **ID:** {guild.owner.id}", inline=True)
            embed.add_field(
                name="Members", value=f"**>** **Humans:** {true_member_count}\n**>** **Bots:** {bots}")
            embed.add_field(name="Boost Status",
                            value=f"**>** **Boosters:** {len(guild.premium_subscribers)}\n**>** **Boosts:** {guild.premium_subscription_count}\n**>** **Boost Level:** {boostlevel}",
                            inline=True)
            embed.add_field(name='Features',
                            value=features, inline=False)

            if guild.icon==None:
                pass
            else:
                embed.set_thumbnail(url=guild.icon)

            if guild.splash==None:
                pass
            else:
                embed.set_image(url=guild.splash)
                
            await interaction.followup.send(embed=embed)


    @jeanne_slash(description="Check how fast I respond to a command")
    async def ping(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            start_time = time()
            await interaction.response.defer()
            end_time = time()

            ping = Embed(color=0x236ce1)
            ping.add_field(
                name="**>** Bot Latency", value=f'{round(self.bot.latency * 1000)}ms', inline=False)
            ping.add_field(
                name="**>** API Latency", value=f'{round((end_time - start_time) * 1000)}ms', inline=False)
            await interaction.followup.send(embed=ping)

    @jeanne_slash(description="See the server's banner")
    async def guildbanner(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            guild = interaction.guild
            banner = guild.banner

            if guild.premium_subscription_count < 2:
                nobanner = Embed(description="Server is not boosted at level 2")
                await interaction.followup.send(embed=nobanner)
            
            else:
                try:
                    embed = Embed(colour=0x00B0ff)
                    embed.set_footer(text=f"{guild.name}'s banner")
                    embed.set_image(url=banner)
                    await interaction.followup.send(embed=embed)
                except:
                    embed=Embed(description='Guild has no banner')
                    await interaction.followup.send(embed=embed)

    @jeanne_slash(description="See your avatar or another member's avatar")
    async def avatar(self, interaction: Interaction, member: Member = SlashOption(description="Add a member", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member==None:
                member=interaction.user

            avatar = Embed(title=f"{member}'s Avatar", color=0x236ce1)
            avatar.set_image(url=member.avatar)
            await interaction.followup.send(embed=avatar)

    @jeanne_slash(description="See your guild avatar or a member's guild avatar")
    async def guildavatar(self, interaction: Interaction, member: Member = SlashOption(description="Add a member", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member == None:
                member = interaction.user

            guild_avatar = Embed(title=f"{member}'s Avatar", color=0x236ce1)

            try:
                guild_avatar.set_image(url=member.guild_avatar)
                await interaction.followup.send(embed=guild_avatar)
            except:
                guild_avatar.set_image(url=member.avatar)
                guild_avatar.set_footer(
                    text="Member has no server avatar. Passed normal avatar instead")
                await interaction.followup.send(embed=guild_avatar)

    @jeanne_slash(description="See your banner or someone's banner")
    async def memberbanner(self, interaction: Interaction, member: Member = SlashOption(description="Add a member", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member == None:
                member = interaction.user

            member_id = member.id
            user = await self.bot.fetch_user(member_id)

            try:
                mbanner = Embed(title=f"{user}'s Banner", color=0x236ce1)
                mbanner.set_image(url=user.banner)
                await interaction.followup.send(embed=mbanner)
            except:
                mbanner = Embed(description="Member has no banner", color=0x236ce1)
                await interaction.followup.send(embed=mbanner)

def setup(bot):
    bot.add_cog(slashinfo(bot))
