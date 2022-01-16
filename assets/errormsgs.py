from nextcord import Embed

owner_only = Embed(title="Owner only command", description="This command failed to commit because you are not the bot owner", color=0xff0000)

no_bot_mutual = Embed(description="Bot is not in this server", color=0xff0000)

no_user = Embed(title="User does not exist", description="Please make sure the USER_ID is valid.", color=0xff0000)

no_hentai = Embed(title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
no_hentai.add_field(name="Reason", value="Channel is not NSFW enabled")

no_member = Embed(description="Member is not in this server")

channel_perm=Embed(title='Manage Channel Failed', description="This channel couldn't be managed", color=0xff0000)
channel_perm.add_field(name="Reason", value="Missing Permissions: Manage Channels")

role_perm=Embed(title='Manage Role Failed', description="This role couldn't be managed", color=0xff0000)
role_perm.add_field(name="Reason", value="Missing Permissions: Manage Roles")   

nick_perm=Embed(title='Manage Nickname Failed', description="This nickname couldn't be managed", color=0xff0000)
nick_perm.add_field(name="Reason", value="Missing Permissions: Manage Nicknames") 

cat_perm=Embed(title='Manage Category Failed', description="This category couldn't be managed", color=0xff0000)
cat_perm.add_field(name="Reason", value="Missing Permissions: Manage Channels")                                              

mute_perm=Embed(title="Mute failed", description="Sorry but you cannot mute this user", color=0xff0000)
mute_perm.add_field(name="Reason", value="Missing permissions: Moderate Members", inline=False)

kick_perm=Embed(title="Kick failed", description="Sorry but you cannot kick this user", color=0xff0000)
kick_perm.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)

unban_perm = Embed(title="Unban failed", description="Sorry but you cannot unban this user", color=0xff0000)
unban_perm.add_field(name="Reason", value="Missing permissions: Ban Members", inline=False)

failed_unban = Embed(title="Unban failed", description="Invalid user ID given.", color=0xff0000)

ban_perm=Embed(title="Ban failed", description="Sorry but you cannot ban this user", color=0xff0000)
ban_perm.add_field(name="Reason", value="Missing permissions: Ban Members", inline=False)

failed_ban = Embed(
                title="Ban failed", description="Invalid user ID given.", color=0xff0000)

warn_perm=Embed(title="Warn failed", description="Sorry but you cannot warn this user", color=0xff0000)
warn_perm.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)

unmute_perm=Embed(title="Unmute failed", description="Sorry but you cannot unmute this user", color=0xff0000)
unmute_perm.add_field(name="Reason", value="Missing permissions: Moderate Members", inline=False)

message_perm=Embed(title="Purge failed", description="Sorry but you cannot purge messages", color=0xff0000)
message_perm.add_field(name="Reason", value="Missing permissions: Manage Messages", inline=False)

admin_perm=Embed(title="Say failed", description="Sorry but I cannot say this message", color=0xff0000)
admin_perm.add_field(name="Reason", value="Missing permissions: Administrator", inline=False)