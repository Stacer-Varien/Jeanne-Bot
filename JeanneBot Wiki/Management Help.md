# Management Commands

*Text Channel commands, Voice Channel commands and Category commands require the `manage channels` permisson, Role commands require the `manage roles` permisson and modlog, welcomer and leaver commands requires the `manage server` permission.*

>**Create Channel**

* Create a text channel, voice channel or category. You will given 3 options to pick when creating them

    Example: `/create_channel CHANNEL_TYPE(text, voice or category) NAME`

>**Delete Channel**

* Deletes the text channel, voice channel or category.

    Example:`/delete_channel CHANNEL_NAME`

>**Rename Text Channel**

* Renames the text channel

    Example: `/rename_text_channel CHANNEL_NAME NEW_NAME`

>**Rename Voice Channel**

* Renames the voice channel

    Example: `/rename_voice_channel CHANNEL_NAME NEW_NAME`

>**Create Role**

* Creates a new role

    Example: `/create_role ROLE_NAME`

>**Delete Role**

* Deletes a role

    Example:`/delete_role ROLE_NAME`

>**Rename Role**

* Renames the role

    Example: `/renname_role OLD_NAME NEW_NAME`

>**Rename Category**

* Renames the category

    Example:`/rename_category CATEGORY NAME NEW_NAME`


>**Set**

* Sets a welcomer/leaving/modlog channel for the server
* **NOTE:** Three options will be given to you. You can pick one for a channel then do it again after executing the command. It will only set one channel depending on what you have chosen. The welcomng and leaving message is uncustomisable for now. Channels set for modlog will have warns, mutes and bans posted in there.

    Example:`/set TYPE CHANNEL`

>**Remove**

* Removes a welcomer/leaving/modlog channel for the server
* **NOTE:** Four options will be given to you. You can pick an option then do it again after executing the command. If you want all to be removed, use the `all` option.

    Example:`/remove TYPE`
