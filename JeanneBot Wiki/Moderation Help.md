# Moderation Commands

>**Warn**
* Warn a user for violating a rule. You can add a reason for what they did
* **Required permissions:** Kick Members
* **Aliases:** warn, w

    Exapmle: `j!w USER REASON`

>**Kick**
* Kicks a user out of the server. They are able to come back to the server. You can add a reason for what they did
* **Required permissions:** Kick Members
* **Aliases:** kick, k

    Example: `j!k USER REASON`

>**Ban**
* Bans a user permanently. You can add a reason for what they did
* **Required permissions:** Ban Members
* **NOTE:** For an outside ban, use the prefixed ban command
* **Aliases:** ban, b

    Example: `j!b USER REASON`

>**Unban**
* Unbans a user so they can be able to come back to the server. You can add a reason why they are unbanned
* **Required permissions:** Ban Members
* **NOTE:**This command can only work by a prefixed unban command
* **Aliases:** unban, unb

    Example: `j!unb USER REASON`

>**Purge**
* Bulk delete messages
* **Required Permission:** Manage Messages
* **NOTE:** This is a **slash only** command. Will delete up to 100 messages. You can also mention a member or add a number less than 100 to delete the messages.

    Example: `/purge 20 MEMBER`
    **NOTE**: For purging messages up to the limit, use `/purge`

>**Mute**
* Mute someone and they will not talk. You can add a reason why they are muted
* **Required Permission:** Kick Members
* **NOTE:** If a mute role doesn't exist, make a new 'Muted' role or use the `muterole` command and Jeanne will make a new one or she will ignore the command and will not mute the member. If there is no time given, it will be infinite. All times displayed by Jeanne will be in seconds instead of actual time duration.

    Example: `j!mute MEMBER TIME REASON`

>**Unmute**
* Unmute a muted member so they can talk.
* **Required Permission:** Kick Members

    Example: `j!unmute MEMBER`