Since we are approuching 2022, I looked back at the plans I had for Jeanne in the [ReadMe file](https://github.com/Varien-1936/Jeanne-Bot/blob/main/README.md) and I have been neglecting most of the features, even though they have been implemented before but revoked due to accusations of making copycats of certain bots, I will try to bring them back. As of now, I am making small improvements on the current commands so at least they can function properly.

# Currency and leveling system

I had this type of system before however, I had to revoke them due to accusations but not only that. Heroku doesn't support data dumping in JSONs. The VPS requires a proper database such as Redis and MongoDB. If I bring those systems, it would be pre-released (meaning unfinished but functional).

> Currency System

* The currency will be Gil (from the Fate/Extella game) but I have not decided a symbol for it.
* I will try to make a shop system but this can take a while. I need suggestions on items I need to put (they must be SFW, not crossing NSFW borderline and must not break the bot or system in any way or form)
* I'm planning to add a vote reward system so if you vote in Jeanne's [Top.gg](https://top.gg/bot/831993597166747679), you will get a certain amount.

> Levelling System

* A member can get 5 - 10 xp per message to level up. However, the requirement to reach the next level will be more.
* The XP will be server specific but they will be a cooldown I might put such as if someone gains XP in one server and tried to gain almost immediately in another server, they will have to wait 10 seconds until gaining XP. If they try to cheat to gain XP (such as in an empty server), it will not happen because I will put a member requirement to order to gain XP.

# Logging System

Inspired by [Hinata](https://github.com/Drag0nDev/Hinata) made by my friend, [Ddraig](https://github.com/Drag0nDev), I will make a command that allows Jeanne to make log channels such as a join-leave, public modlog and a private server log channels which will log in everything that has happened in the server such as warns, channel renames and changes in roles. However, if their names has changed, Jeanne will not log them in.

# Softban

This I believe is almost as hard as the levelling and currency system. This command involves banning someone for a specific peroid and unbans them after the time limit has reached.

# Full Implemention of Slash Commands

Even though the slash commands has been implement, they dont work the same as the prefixed commands. I might change the way some commands work in order to keep them. I also need full use of the owner commands. As of January 2022, I will revoked all prefixed commands and Jeanne will be used by slash commands. Some commands may work differently than the prefixed commands.

# Transition to NextCord or PyCord

Since Discord.py is about to die and remain outdated until someone takes over the project, I might move Jeanne to NextCord or PyCord but for me to do this, there must be certain conditions that must meet:

> For NextCord:

* If the maintainer of NextCord brings slash command support to the library, I will move Jeanne to it. As of now, there is no news of yet about the support of slash commands. Someone has requested it but got responeded with a laughing emote. The maintainer should be aware that the prefixed commands on verified bots will be removed.

> For PyCord:

* PyCord does have the slash command support but problem is that when using it, the VPS will either install the discord.py from the main python file or requirements.txt or fail to install the developing package. Fortunately, Replit does allow that package but its not 100% reliable on uptime if I use keep_alive unless I have to pay 7 USD which is a complete waste of money since I didn't set up a donation page and I have to think about the benefits of donating to keep Jeanne alive and giving the donators the perks for the amount they've donated.

# Community for Jeanne

Well, it is true that my server, [HAZE](https://discord.gg/VVxGUmqQhF) which serves as a community and support server for Jeanne so people can get updates on developments and report bugs and faults would work but I might be thinking of opening a subreddit for Jeanne. I will post all tutorials and updates in that subreddit but this is a chance that it will happen or not.

I just hope that when 2022 comes, I will implement those features and get them done before the 2022 year ends.
