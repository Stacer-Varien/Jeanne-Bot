I am now back with another FAQ. I know someone will ask why was some commands not working and why some disappeared and about the botban that I did not explain more in [Botban info](https://github.com/Varien-1936/Jeanne-Bot/blob/main/JeanneBot%20Wiki/Assets/Botban%20info.md) so I will explain it here including answering questions I might be frequently asked.

Before I go there, I have to thank [Alyx](https://github.com/AlyxFoxy) for contributing to Jeanne and fixing the faults and bugs I didn't have time to do that she is now a collaborator of Jeanne. Congratulations to her.

Now to FAQ time.

# Question

I was botbanned and someone was able to warn, mute, kick, delete my messages and ban me with Jeanne. I thought I was immune to moderation commands. Why?

* **Answer**

    Being botbanned doesn't grant you immunity from commands done on you. Being botbanned renders all commands to you useless but not commands **on** you, meaning someone can still ban you with Jeanne even if you are botbanned.

# Question

I was botbanned but my warnings in a server is still there. Why were they not removed?

* **Answer**

    If you have read from above, being botbanned doesn't grant you immunity on commands done on you and it is only your XP data and currency data (will be implemented) removed from the database. Your warnings will stay in the database after you are botbanned.

# Question

Why was Gelbooru and Danbooru removed?

* **Answer**

    Lets look at Gelbooru:
    Gelbooru's API has changed in a way it was almost impossible to fix. I had revoked the command when this happened temporary but brought it back later but out of nowhere, the API changed.

    Now at Danbooru:
    Danbooru's API was impossible to filter and chances of getting loli or illicit material (due to Discord's new ToS and Guidelines) is low but never zero.

    To give myself a less of a headache, I revoked them. I am happy with having Hentai, Yandere and Konachan as part of the Hentai module.

# Question

Someone used a guess or say command and I want to troll them by ruining the command by typing for them before they finish but failed. Why?

* **Answer**

    The guess and say command is waiting for the response from the person who used the command. Third parties will be unable to type a message for them as it is author target.

# Question

Can I contribute to Jeanne such as fixing your broken codes or faults?

* **Answer**

    I am more than happy that you will contribute to Jeanne. Just make sure you make a pull request and alert me about it so I can have a look at it.

# Question

When will the currency system be implemented?

* **Answer**

    It will take some time to have the currency system working. It is still under testing stage but the 'incomplete but operational' version of it is not yet ready to be published. The daily command still needs attention and the other thing is to sort out the vote rewards. I am confident that before July 2022, the system will be implemented and before December 2022, the system is fully operational. For the vote rewards, the problem is that TopGG depends on the Discord.py library and it is the one used for the 2nd instance but since I am hearing that Rapptz has made a return, I might rewrite her back to Discord.py if it is similar to Nextcord so a little of work can be done on her.

# Question

Why are I not mentioned when I use a reaction command?

* **Answer**

    This is a problem that happened with slash commands not mentioning users after executions. It was later resolved with a new Nextcord update and also allowing Jeanne to mention users and roles. However, I have changed the way the users will be mentioned with a reaction command. Just know that Jeanne will still mention people full on if a say command has been used if a 'plain text' option was selected.

  * The user of the command will not be mentioned
  * The target member used for the reaction command will be mentioned

# Question

Can I customise the welcoming and leaving message?

* **Answer**

    For now, no but this feature will be implemented in the nearby future. If it does, it will be the plain text option for a while until I bring up an embed generator.  

# Question

I want to get rid of the welcomer, leaver and modlog from my server but I do not want to do it one by one. How?

* **Answer**

    Thanks to [Alyx](https://github.com/AlyxFoxy), she has changed the command in a way that you can remove it one by one but she also added the 'all' option. The 'all' option will remove all of them.

# Question

What if I want people to appeal for their warns in the server? Will there be an appeal command?

* **Answer**

    That one is still under questioning but I do not guarantee that it will be implemented.
