import re
from d3vilbot import *
from d3vilbot.assistant import *
from telethon import events, Button
import heroku3
import asyncio
import os
import requests
from d3vilbot.helpers import *
from d3vilbot.utils import *
from d3vilbot.assistant.sql.blacklist_sql import all_bl_users
#from d3vilbot.plugins import TELE_NAME
from d3vilbot.assistant.sql.userbase_sql import add_to_userbase, present_in_userbase, full_userbase
from datetime import datetime
from telethon import events
from d3vilbot.config import Config
from telegraph import Telegraph, upload_file
from d3vilbot import CUSTOM_PMPERMIT

TELE_NAME = bot.me.first_name
OWNER_ID = bot.me.id

##################--CONSTANTS--##################
ASSISTANT  = Config.ASSISTANT 
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
BOT_PIC = Config.BOT_PIC if Config.BOT_PIC else None
heroku_api = "https://api.heroku.com"
path = Config.TMP_DOWNLOAD_DIRECTORY
if not os.path.isdir(path):
    os.makedirs(path)
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]
################--CONSTANTS-END-#################

# start-others


@tgbot.on(events.NewMessage(pattern="^/start"))  # pylint: disable=oof
async def start_all(event):
    if event.chat_id == OWNER_ID:
        return
    target = event.sender_id
    if present_in_userbase(target):
        pass
    else:
        try:
            add_to_userbase(target)
        except BaseException:
            pass
    if ASSISTANT  == "OFF":
        if BOT_PIC:
            await tgbot.send_file(event.chat_id,
                                  BOT_PIC,
                                  caption=startotherdis,
                                  buttons=[
                                      (Button.inline(
                                          "What can I do here?",
                                          data="wew"))]
                                  )
        else:
            await tgbot.send_message(event.chat_id,
                                     startotherdis,
                                     buttons=[
                                         (Button.inline(
                                             "What can I do here?",
                                             data="wew"))]
                                     )
    elif ASSISTANT  == "ON":
        if BOT_PIC:
            await tgbot.send_file(event.chat_id,
                                  BOT_PIC,
                                  caption=startotherena,
                                  buttons=[
                                      [Button.url(
                                          "D3vilBot", url="https://github.com/TEAM-D3VIL/D3vilbot")],
                                      [Button.inline(
                                          "Whats this?", data="d3vilbot")]
                                  ]
                                  )
        else:
            await tgbot.send_message(event.chat_id,
                                     startotherena,
                                     buttons=[
                                         [Button.url(
                                             "D3vilBot", url="https://github.com/TEAM-D3VIL/D3vilbot")],
                                         [Button.inline(
                                             "Whats this?", data="d3vilbot")]
                                     ]
                                     )

# start-owner


@tgbot.on(events.NewMessage(pattern="^/start",
                            from_users=OWNER_ID))  # pylint: disable=oof
async def owner(event):
    await tgbot.send_message(event.chat_id,
                             startowner,
                             buttons=[
                                 [Button.inline(
                                     "Settings ⚙️", data="settings"),
                                  Button.inline(
                                     "Stats ⚙️", data="stats")],
                                 [Button.inline("Broadcast",
                                                data="telebroad")],
                                 [Button.url("Support",
                                             url="https://t.me/D3VIL_BOT_SUPPORT")]
                             ])


@tgbot.on(events.NewMessage(pattern="^/start logs",
                            from_users=OWNER_ID))  # pylint: disable=oof
async def logs(event):
    try:
        Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        app = Heroku.app(Config.HEROKU_APP_NAME)
    except BaseException:
        await tgbot.send_message(event.chat_id, " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku var !")
        return
    with open('logs.txt', 'w') as log:
        log.write(app.get_log())
    ok = app.get_log()
    url = "https://del.dog/documents"
    r = requests.post(url, data=ok.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    await tgbot.send_file(
        event.chat_id,
        "logs.txt",
        reply_to=event.id,
        caption="**Heroku** D3vilBot Logs",
        buttons=[
            [Button.url("View Online", f"{url}")],
            [Button.url("Crashed?", "t.me/D3VIL_BOT_SUPPORT")]
        ])
    await asyncio.sleep(5)
    return os.remove('logs.txt')


# callbacks


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"wew"))
          )  # pylint: disable=oof
async def settings(event):
    await event.delete()
    await tgbot.send_message(event.chat_id,
                             "There isn't much that you can do over here rn.",
                             buttons=[
                                     [Button.inline(
                                         "Deploy me for yourself", data="deployme")]
                             ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"d3vilbot"))
          )  # pylint: disable=oof
async def settings(event):
    await event.delete()
    await tgbot.send_message(event.chat_id,
                             f"This is the personal help bot of {TELE_NAME}. You can contact me using this bot if necessary, or if I missed out your PM.",
                             buttons=[
                                     [Button.inline(
                                         "Deploy me for yourself", data="deployme")]
                             ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deployme"))
          )  # pylint: disable=oof
async def settings(event):
    await event.edit("Browse through the available options:",
                     buttons=[
                         [(Button.url("Repository", url="https://github.com/TEAM-D3VIL/D3vilbot")),
                          (Button.url("Tutorial", url="https://youtu.be/PHJ3O34Pvc0"))],
                         [Button.url("Support",
                                     url="https://t.me/D3VIL_BOT_SUPPORT")]
                     ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"settings"))
          )  # pylint: disable=oof
async def settings(event): 
    if event.sender_id == OWNER_ID:
        await event.delete()
        ok = Config.BOT_USERNAME
        if ok.startswith('@'):
            ok = ok.split('@')[1]
        await tgbot.send_message(event.chat_id,
                                 "Here are the available options.",
                                 buttons=[
                                     [Button.inline(
                                         "PM Bot", data="pmbot")],
                                     [Button.inline(
                                         "Customs", data="custom")],
                                     [Button.url(
                                         "Logs", url=f"https://t.me/{ok}?start=logs")]
                                 ])
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats"))
          )  # pylint: disable=oof
async def settings(event):
    if event.sender_id == OWNER_ID:
        allu = len(full_userbase())
        blu = len(all_bl_users())
        pop = "Here is the stats for your bot:\nTotal Users = {}\nBlacklisted Users = {}".format(
            allu, blu)
        await event.answer(pop, alert=True)
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmbot"))
          )  # pylint: disable=oof
async def pmbot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "Here are the availabe settings for PM bot.",
                                 buttons=[
                                     [Button.inline("Enable/Disable", data="onoff"), Button.inline(
                                         "Custom Message", data="cmssg")],
                                     [Button.inline("Bot Pic", data="btpic")]
                                 ])
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"onoff"))
          )  # pylint: disable=oof
async def pmbot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 f"Turn the PM bot on or off.\nCurrently enabled: {ASSISTANT }",
                                 buttons=[
                                     [Button.inline("Enable", data="enable"), Button.inline(
                                         "Disable", data="disable")]
                                 ])
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"btpic"))
          )  # pylint: disable=oof
async def bot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the new pic you want to be shown when someone starts the bot:")
            await conv.send_message("Send /cancel to cancel the operation!")
            response = await conv.get_response()
            try:
                themssg = response.message.message
                if themssg == "/cancel":
                    await conv.send_message("Operation cancelled!!")
                    return
            except BaseException:
                pass
            media = await event.client.download_media(response, "Bot_Pic")
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                os.remove(media)
            except BaseException:
                return await conv.send_message("Error!")
        d3vilbot = "BOT_PIC"
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        xx = await tgbot.send_message(event.chat_id, "Changing your Bot Pic, please wait for a minute")
        heroku_var = app.config()
        heroku_var[d3vilbot] = f"{url}"
        mssg = f"Successfully changed your bot pic. Please wait for a minute.\n"
        await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"cmssg"))
          )  # pylint: disable=oof
async def custom(event):
    if event.sender_id == OWNER_ID:
        await event.reply("You can change your BOT STARTMESSAGE here.\n If you don't want to change then send  /cancel to cancel the operation.")
        async with event.client.conversation(OWNER_ID) as conv:
            response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response = await response
            themssg = response.message.message
            if themssg == "/cancel":
                await tgbot.send_message(event.chat_id, "Operation Cancelled.")
                return
            d3vilbot = "PMBOT_START_MSSG"
            if Config.HEROKU_APP_NAME is not None:
                app = Heroku.app(Config.HEROKU_APP_NAME)
            else:
                mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
                return
            heroku_var = app.config()
            heroku_var[d3vilbot] = f"{themssg}"
            mssg = "Changed the PMBot start message!!\n**Restarting now**, please give me a minute."
            await event.delete()
            await tgbot.send_message(event.chat_id, mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"enable"))
          )  # pylint: disable=oof
async def enablee(event):
    if event.sender_id == OWNER_ID:
        d3vilbot = "ASSISTANT"
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        heroku_var = app.config()
        heroku_var[d3vilbot] = "ON"
        mssg = "Successfully turned on PM Bot. Restarting now, please give me a minute."
        await event.delete()
        await tgbot.send_message(event.chat_id, mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"disable"))
          )  # pylint: disable=oof
async def dissable(event):
    if event.sender_id == OWNER_ID:
        d3vilbot = "ASSISTANT "
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        heroku_var = app.config()
        heroku_var[d3vilbot] = "OFF"
        mssg = "Successfully turned off PM Bot. Restarting now, please give me a minute."
        await event.delete()
        await tgbot.send_message(event.chat_id, mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"telebroad"))
          )  # pylint: disable=oof
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        await event.answer("You can't use this bot")
        return
    await tgbot.send_message(event.chat_id, "Send the message you want to broadcast!\nSend /cancel to stop.")
    async with event.client.conversation(OWNER_ID) as conv:
        response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
        response = await response
        themssg = response.message.message
    if themssg is None:
        await tgbot.send_message(event.chat_id, "An error has occured...")
    if themssg == "/cancel":
        await tgbot.send_message(event.chat_id, "Broadcast cancelled!")
        return
    targets = full_userbase()
    users_cnt = len(full_userbase())
    err = 0
    success = 0
    lmao = await tgbot.send_message(event.chat_id, "Starting broadcast to {} users.".format(users_cnt))
    start = datetime.now()
    for ok in targets:
        try:
            await tgbot.send_message(int(ok.chat_id), themssg)
            success += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            err += 1
            try:
                await tgbot.send_message(Config.LOGGER_ID, f"**Error**\n{str(e)}\nFailed for user: {chat_id}")
            except BaseException:
                pass
    end = datetime.now()
    ms = (end - start).seconds
    done_mssg = """
Broadcast completed!\n
Sent to `{}` users in `{}` seconds.\n
Failed for `{}` users.\n
Total users in bot: `{}`.\n
""".format(success, ms, err, users_cnt)
    await lmao.edit(done_mssg)
    try:
        await tgbot.send_message(Config.LOGGER_ID, f"#Broadcast\nCompleted sending a broadcast to {success} users.")
    except BaseException:
        await tgbot.send_message(event.chat_id, "Please add me to your Private log group for proper use.")


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"custom"))
          )  # pylint: disable=oof
async def custommm(event):
    await event.edit("Modules which you can customise -",
                     buttons=[
                         [Button.inline("Alive", data="alive_cus")],
                         [Button.inline("PMSecurity", data="pm_cus")]
                     ]
                     )
# fmt: off
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"alive_cus")))
async def alv(event):
    await event.edit("Here are the avaialble customisations for alive",
                    buttons=[
                        [Button.inline("Text", data="alv_txt")],
                        [Button.inline("Picture", data="alv_pic")]
                    ])

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"alv_txt")))
async def a_txt(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_alv=Config.ALIVE_MSG if Config.ALIVE_MSG else "Default Alive message"
        d3vilbot="ALIVE_MSG"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the text which you want as your alive text.\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                return await conv.send_message("Cancelled!!")
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing your Alive Message, please wait for a minute")
            heroku_var[d3vilbot]=f"{themssg}"
            mssg=f"Changed your alive text from\n`{old_alv}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"alv_pic"))
           )  # pylint: disable=C0321
async def alv_pic(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id, "Send me a pic so as to set it as your alive pic.")
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send /cancel to cancel the operation!")
            response = await conv.get_response()
            try:
                themssg=response.message.message
                if themssg == "/cancel":
                    await conv.send_message("Operation cancelled!!")
                    return
            except:
                pass
            media=await event.client.download_media(response, "Alive_Pic")
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                os.remove(media)
            except BaseException:
                return await conv.send_message("Error!")
        d3vilbot="ALIVE_PIC"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        xx = await tgbot.send_message(event.chat_id, "Changing your Alive Pic, please wait for a minute")
        heroku_Config=app.config()
        heroku_Config[d3vilbot]=f"{url}"
        mssg=f"Successfully changed your alive pic. Please wait for a minute.\n"
        await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pm_cus")))
async def alv(event):
    await event.edit("Here are the avaialble customisations for PMSecurity",
                    buttons=[
                        [Button.inline("Message", data="pm_txt")],
                        [Button.inline("Picture", data="pm_pic")]
                    ])

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pm_txt")))
async def a_txt(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_alv= CUSTOM_PMPERMIT if CUSTOM_PMPERMIT else "Default PMSecurity message"
        d3vilbot="CUSTOM_PMPERMIT"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send text to change your pm security message if don't want to change. \n  /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, " Updating Mode ON, please wait for a minute")
            heroku_var[d3vilbot]=f"{themssg}"
            mssg=f"Changed your PMsecurity  from\n`{old_alv}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pm_pic"))
           )  # pylint: disable=C0321
async def alv_pic(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id, "Send me a pic so as to set it as your PMSecurity pic.")
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send /cancel to cancel the operation!")
            response = await conv.get_response()
            try:
                themssg=response.message.message
                if themssg == "/cancel":
                    await conv.send_message("Operation cancelled!!")
                    return
            except:
                pass
            media=await event.client.download_media(response, "PM_PIC")
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                os.remove(media)
            except BaseException:
                return await conv.send_message("Error!")
        d3vilbot="PMPERMIT_PIC"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        xx = await tgbot.send_message(event.chat_id, "Changing your PMSecurity Pic, please wait for a minute")
        heroku_var=app.config()
        heroku_var[d3vilbot]=f"{url}"
        mssg=f"Successfully changed your PMSecurity pic. Please wait for a minute.\n"
        await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)

# fmt: on
