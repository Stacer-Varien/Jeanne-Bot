from enum import Enum


class HelpModules(Enum):
    currency = "currency"
    fun = "fun"
    hentai = "hentai"
    image = "image"
    info = "info"
    inventory = "inventory"
    levelling = "levelling"
    manage = "manage"
    moderation = "moderation"
    reactions = "reaction"
    utility = "utility"

class HelpCommands(Enum):
    #currency
    daily = "daily"
    balance = "balance"
    vote = "vote"
    guess = "guess"
    dice = "dice"
    flip = "flip"
    #fun
    eight_ball = "8ball"
    reverse = "reverse"
    animeme = "animeme"
    combine = "combine"
    choose = "choose"
    simprate = "simprate"
    gayrate = "gayrate"
    #hentai
    hentai='hentai'
    gelbooru='gelbooru'
    yandere='yandere'
    konachan='konachan'
    #image
    kitsune='kitsune'
    wallpaper='wallpaper'
    jeanne='jeanne'
    saber='saber'
    neko='neko'
    medusa='medusa'
    safebooru='safebooru'
    #info
    stats='stats'
    userinfo='userinfo'
    serverinfo='serverinfo'
    ping='ping'
    serverbanner='serverbanner'
    avatar='avatar'
    sticker='sticker'
    emoji='emoji'
    #inventory
    shop='shop'
    backgrounds='backgrounds'
    background_preview='background preview'
    background_buy='background buy'
    background_use='background use'
    background_buy_custom='background buy custom'
    background_list='background list'
    #levelling
    rank='rank'
    global_rank='global rank'
    server_rank='server rank'
    level='level'
    profile='profile'
    #manage
    add_role='add role'
    remove_role='remove role'
    remove='remove'
    clone='clone'
    ##create
    create_text_channel='create text channel'
    create_voice_channel='create voice channel'
    create_category='create category'
    create_stage_channel='create stage channel'
    create_forum='create forum'
    create_role='create role'
    create_thread='create thread'
    create_emoji='create emoji'
    create_sticker='create sticker'
    ##delete
    delete_channel='delete channel'
    delete_role='delete role'
    delete_emoji='delete emoji'
    delete_sticker='delete sticker'
    ##edit
    edit_text_channel='edit text channel'
    edit_role='edit role'
    edit_server='edit server'
    ##set
    set_welcomer='set welcomer'
    set_modlog='set modlog'
    set_welcomermsg='set welcomermsg'
    set_leavingmsg='set leavingmsg'
    set_level_update='set level update'
    set_brightness='set brightness'
    set_bio='set bio'
    set_color='set color'
    ##xp
    xp_blacklist='xp blacklist'
    xp_unblacklist='xp unblacklist'
    xp_blacklisted_channels='xp blacklisted channels'
    ##rename
    rename_emoji='rename emoji'
    rename_sticker='rename sticker'
    rename_category='rename category'
    #mod
    warn='warn'
    clear_warn='clear warn'
    kick='kick'
    prune='prune'
    change_nickname='change nickname'
    unban='unban'
    timeout='timeout'
    untimeout='timeout'
    massban='massban'
    massunban='massunban'
    ##ban
    ban_member='ban member'
    ban_user='ban user'
    ##listwarns
    listwarns_server='listwarns server'
    listwarns_user='listwarns user'
    #react
    hug='hug'
    slap='slap'
    smug='smug'
    poke='poke'
    pat='pat'
    kiss='kiss'
    tickle='tickle'
    baka='baka'
    feed='feed'
    cry='cry'
    bite='bite'
    blush='blush'
    cuddle='cuddle'
    dance='dance'
    #utilities
    weather_city='city weather'
    weather_zipcode='zip code weather'
    embed_generate='embed generate'
    embed_edit='embed edit'
    reminder_add='reminder add'
    reminder_list='reminder list'
    reminder_cancel='reminder cancel'
    say='say'
    calculator='calculator'
    invite='invite'
    botreport='bot report'
    dictionary='dictionary'



