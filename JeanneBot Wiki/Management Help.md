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

>**Set Modlog**

* Sets a modlog channel for the server
* **NOTE:** It will only set one modlog channel. If you want to switch modlog channels, use the command again and select a different channel. All warnings, mutes, bans and unbans are logged in there

    Example:`/set_modlog CHANNEL`

>**Remove Modlog**

* Removes a modlog channel from the databse

    Example:`/remove_modlog`

>**Set Welcomer**

* Sets a welcoming channel for the server
* **NOTE:** It will only set one welcoming channel. The welcoming message is uncustomisable for now.

    Example:`/set_welcomer CHANNEL`

>**Remove Welcomer**

* Removes a welcoming channel from the databse

    Example:`/remove_welcomer`

>**Set Leaver**

* Sets a leaving channel for the server
* **NOTE:** It will only set one leaving channel. The leaving message is uncustomisable for now.

    Example:`/set_leaver CHANNEL`

>**Remove Leaver**

* Removes a leaving channel from the databse

    Example:`/remove_leaving`
