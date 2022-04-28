# Moderation Commands

>**Warn**

* Warn a user for violating a rule. You can add a reason for what they did.
* **NOTE:** A warn ID is given. This warn ID is server specific. This command can work if you have roles set in your server. You won't be able to warn someone higher than you but you can warn people lower than you
* **Required permissions:** Kick Members

    Exapmle: `/warn USER REASON`

>**List Warns**

* List warnings of members in the server or of a member. Their warn IDs are shown
* **NOTE:** Everyone can use this command

    Exapmle: `/list_warns` (if for all members in the server) / `/list_warns MEMBER` (if for a member)

>**Revoke Warn**

* Revokes a warning that a member has by warn ID
* **NOTE:** You must give a valid warn ID to revoke it
* **Required permissions:** Kick Members

    Exapmle: `/revoke_warn WARN_ID`

>**Kick**

* Kicks a user out of the server. You can add a reason for what they did
* **NOTE:**  They are able to come back to the server if they have the invite
* **Required permissions:** Kick Members

    Example: `/kick USER REASON`

>**Ban**

*Member*
* Bans a member of the server permanently. You can add a reason for what they did
* **Required permissions:** Ban Members

    Example: `/memberban USER REASON`

*User*
* Bans a user permanently and prevents them from entering your server before they could. You can add a reason for what they did
* **NOTE:** A user ID must be used for the command
* **Required permissions:** Ban Members

    Example: `/outsideban USER_ID REASON`

>**Unban**

* Unbans a user so they can be able to come back to the server. You can add a reason why they are unbanned
* **NOTE:** A user ID must be used for the command
* **Required permissions:** Ban Members

    Example: `/unban USER_ID REASON`

>**Purge**

* Bulk delete messages
* **Required Permission:** Manage Messages
* **NOTE:** This will delete up to 100 messages. You can also mention a member and/or add a number less than 100 to delete the messages.

    Example: `/purge 20 MEMBER`
    **NOTE**: For purging messages up to the limit, use `/purge`

>**Mute**

* Mute someone and they will not talk. You can add a reason why they are muted
* **Required Permission:** Moderate Members
* **NOTE:** If no mute time has been given, time will be 28 days. You cannout mute someone for more than 28 days due to Discord's API. You also cannot mute bots.

    Example: `/mute MEMBER TIME REASON`

>**Unmute**

* Unmute a muted member so they can talk.
* **Required Permission:** Moderate Members

    Example: `/unmute MEMBER`

>**Change Nickname**

* Change a member's nickname
* **Required Permission:** Manage Nicknames
* **NOTE:** You cannot change your own nickname with this command.

    Example: `/change_nickname MEMBER NICKNAME`
