# Moderation Commands

>**Warn**

* Warn a user for violating a rule. You can add a reason for what they did.
* **NOTE:** A warn ID is given. This warn ID is server specific
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

    Example: `/unban USER_ID REASON`

>**Purge**

* Bulk delete messages
* **Required Permission:** Manage Messages
* **NOTE:** This will delete up to 100 messages. You can also mention a member or add a number less than 100 to delete the messages.

    Example: `/purge 20 MEMBER`
    **NOTE**: For purging messages up to the limit, use `/purge`

>**Mute**

* Mute someone and they will not talk. You can add a reason why they are muted
* **Required Permission:** Moderate Members
* **NOTE:** If no mute time has been given, time will be 28 days. You cannout mute someone for more than 28 days due to Discord's API.

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
