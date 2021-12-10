# Moderation Commands

>**Warn**

* Warn a user for violating a rule. You can add a reason for what they did
* **Required permissions:** Kick Members
* **Aliases:** warn, w

    Exapmle: `j!w USER REASON`

>**Kick**

* Kicks a user out of the server. You can add a reason for what they did
* **NOTE:**  They are able to come back to the server if they have the invite
* **Required permissions:** Kick Members
* **Aliases:** kick, k

    Example: `j!k USER REASON`

>**Ban**

* Bans a user permanently. You can add a reason for what they did
* **Required permissions:** Ban Members
* **Aliases:** ban, b

    Example: `j!b USER REASON`

>**Memberban**

* Bans a user permanently. You can add a reason for what they did
* **NOTE:** This is a slash command that bans a user from the server
* **Required permissions:** Ban Members

    Example: `/memberban USER REASON`

>**Outsideban**

* Bans a user permanently and prevents them from entering your server. You can add a reason for what they did
* **NOTE:** This is a slash command that bans a user outside the server
* **Required permissions:** Ban Members

    Example: `/outsideban USER REASON`

>**Unban**

* Unbans a user so they can be able to come back to the server. You can add a reason why they are unbanned
* **Required permissions:** Ban Members
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

>**Change Nickname**

* Change a member's nickname
* **Required Permission:** Manage Nicknames
* **NOTE:** You cannot change your own nickname. If a nickname has not been provided, it will return with a `Please include nickname` error.

    Example: `j!nick MEMBER NICKNAME`
