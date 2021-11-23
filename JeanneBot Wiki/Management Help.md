# Management Commands

*Text Channel commands, Voice Channel commands and Category commands require the `manage channels` permisson and Role commands require the `manage roles` permisson*

>**Create Text Channel**

* Creates a new text channel
* **Aliases:** createtextchannel, ctc

    Example: `j!ctc CHANNEL NAME`

>**Delete Text Channel**

* Deletes the text channel
* **NOTE:** This command requires a mentioned channel or a channel ID in order to delete it.
* **Aliases:** deletetextchannel, dtc

    Example:`j!dtc CHANNEL_NAME` (with channel mentioned) / `j!dtc CHANNEL_ID` (with channel ID)

>**Rename Text Channel**

* Renames the text channel
* **NOTE:** This command requires a mentioned channel or a channel ID in order to rename it.
* **Aliases:** renametextchannel, rntc

    Example: `j!rtc CHANNEL_NAME NEW_NAME`(with channel mentioned) / `j!rntc CHANNEL_ID NEW_NAME (with channel ID)

>**Create Voice Channel**

* Creates a new voice channel
* **Aliases:** createvoicechannel, cvc

    Example:`j!ctc CHANNEL_NAME`

>**Delete Voice Channel**

* Deletes the voice channel
* **NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.
* **Aliases:** deletevoicechannel, dvc

    Example: `j!dvc CHANNEL NAME` \ `j!dvc CHANNEL_ID` (with channel ID)

>**Rename Voice Channel**

* Renames the voice channel
* **NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.
* **Aliases:** renametextchannel, rtc

    Example: `j!rnvc CHANNEL_NAME NEW_NAME` \ `j!rvc CHANNEL_ID NEW_NAME` (with channel ID)

>**Create Role**

* Creates a new role
* **Aliases:** createrole, cr

    Example: `j!cr ROLE_NAME`

>**Delete Role**

* Deletes a role
* **Aliases:** deleterole, dr

    Example:`j!dr ROLE_NAME` \ `j!dvc ROLE_ID` (with role ID)

>**Rename Role**

* Renames the role
* **NOTE:** A role ID or role mentioned can be used to acurately delete the role.
* **Aliases:** renamerole, rnr

    Example: `j!rnr OLD_NAME NEW_NAME` (with role mentioned) \ `j!rnr ROLE_ID NEW_NAME` (with role ID)

>**Muterole**

* Creates a mute role
* **NOTE:** The permissions set will be `View Channels=False` and `Send Messages=False` but you can re-adjust the mute role except renaming it.

    Example: `j!muterole`

>**Create Category**

* Creates a new category
* **Aliases:** ccat, createcatagory, createcat, ccategory

    Example:`j!ccat CATEGORY NAME`

>**Delete Category**

* Deletes the category
* **NOTE:** This command requires a category ID to accurately delete it in case it cannot be found.
* **Aliases:** dcat, deletecat, delcat, deletecategory, dcategory

    Example:`j!dcat CATEGORY NAME` (with category name) / `j!dcat CATEGORY ID` (with category ID)

>**Rename Category**

* Renames the category
* **NOTE:** This command requires a category ID to accurately rename it in case it cannot be found.
* **Aliases:** rncat, renamecat, rncategory, renamecategory

    Example:`j!rncat CATEGORY NAME NEW_NAME`(with category name) / `j!rncat CATEGORY ID NEW_NAME` (with category ID)
