from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from requests import get
from config import *

class slashreactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Hug someone or yourself")
    async def hug(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to hug?", required=False)):
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
            hug_api = get(hug_nekoslife).json()
            if member == None:
                msg=f"*Hugging {interaction.user.mention}*"
            else:
                msg=f"*{interaction.user.mention} hugged {member.mention}*"
            hug = Embed(color=0xFFC0CB)
            hug.set_footer(text="Fetched from nekos.life")
            hug.set_image(url=hug_api["url"])
            await interaction.followup.send(msg, embed=hug)

    @jeanne_slash(description="Slap someone or yourself")
    async def slap(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to slap?", required=False)):
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
            slap_api = get(slap_nekoslife).json()

            slap = Embed(color=0xFFC0CB)
            slap.set_footer(text="Fetched from nekos.life")
            slap.set_image(url=slap_api["url"])
            if member == None:
                    msg=f"*Slapping {interaction.user.mention}*"
            else:
                    msg=f"*{interaction.user.mention} slapped {member.mention}*"
            await interaction.followup.send(msg, embed=slap)

    @jeanne_slash(description="Show a smuggy look")
    async def smug(self, interaction : Interaction):
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
            smug_api = get(smug_nekoslife).json()

            smug = Embed(color=0xFFC0CB)
            smug.set_footer(text="Fetched from nekos.life")
            smug.set_image(url=smug_api["url"])
            await interaction.followup.send(f"*{interaction.user.mention} is smugging*", embed=smug) 

    @jeanne_slash(description="Poke someone or yourself")
    async def poke(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to poke?", required=False)):
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
            poke_api = get(poke_nekoslife).json()
            poke = Embed(color=0xFFC0CB)
            poke.set_footer(text="Fetched from nekos.life")
            poke.set_image(url=poke_api["url"])
            if member == None:
                    msg=f"*Poking {interaction.user.mention}*"
            else:
                    msg=f"*{interaction.user.mention} poked {member.mention}*"
            await interaction.followup.send(msg, embed=poke)

    @jeanne_slash(description="Pat someone or yourself")
    async def pat(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to pat?", required=False)):
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
            pat_api = get(pat_nekoslife).json()
            pat = Embed(color=0xFFC0CB)
            pat.set_footer(text="Fetched from nekos.life")
            pat.set_image(url=pat_api["url"])
            if member == None:
                    msg=f"*Patting {interaction.user.mention}*"
            else:
                    msg=f"*{interaction.user.mention} patted {member.mention}*"
            await interaction.followup.send(msg, embed=pat)

    @jeanne_slash(description="Kiss someone or yourself")
    async def kiss(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to kiss?", required=False)):
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
            kiss_api = get(kiss_nekoslife).json()
            if member == None:
                msg=f"*Kissing {interaction.user.mention}*"
            else:
                msg=f"*{interaction.user.mention} kissed {member.mention}*"
            kiss = Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["url"])
            await interaction.followup.send(msg, embed=kiss)

    @jeanne_slash(description="Tickle someone or yourself")
    async def tickle(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to tickle?", required=False)):
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
            tickle_api = get(tickle_nekoslife).json()
            if member == None:
                msg=f"*Tickling {interaction.user.mention}*"
            else:
                msg=f"*{interaction.user.mention} tickled {member.mention}*"
            tickle = Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await interaction.followup.send(msg, embed=tickle)

    @jeanne_slash(description="Call someone or yourself a baka!")
    async def baka(self, interaction: Interaction, member: Member = SlashOption(description="Who do you calling a baka?", required=False)):
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
            baka_api = get(baka_nekoslife).json()
            if member == None:
                msg=f"*{interaction.user.mention}, you are a baka!*"
            else:
                msg=f"*{member.mention}, {interaction.user.mention} called you a baka!*"
            baka = Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.life")
            baka.set_image(url=baka_api["url"])
            await interaction.followup.send(msg, embed=baka)

    @jeanne_slash(description="Feed someone or yourself")
    async def feed(self, interaction: Interaction, *, member: Member = SlashOption(description="Who do you want to feed?", required=False)):
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
            feed_api = get(feed_nekoslife).json()
            if member == None:
                msg = f"*Feeding {interaction.user.mention}*"
            else:
                msg = f"*{interaction.user.mention} fed {member.mention}*"
            feed = Embed(color=0xFFC0CB)
            feed.set_footer(text="Fetched from nekos.life")
            feed.set_image(url=feed_api["url"])
            await interaction.followup.send(msg, embed=feed)


def setup(bot):
    bot.add_cog(slashreactions(bot))
