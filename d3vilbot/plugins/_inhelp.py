import asyncio
import html
import os
import re
import random
import sys

from math import ceil
from re import compile

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from d3vilbot.sql.gvar_sql import gvarstat
from . import *

d3vil_row = Config.BUTTONS_IN_HELP
d3vil_emoji = Config.EMOJI_IN_HELP
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**🚫 Blocked and Reported**"

alive_txt = """
**⚜️ 𝐃3𝐕𝐈𝐋𝐁𝐎𝐓 𝐈𝐒 𝐎𝐍𝐋𝐈𝐍𝐄 ⚜️**
{}
**↼𝗠𝗔𝗦𝗧𝗘𝗥⇀   :**     **『{}』**
**╔══════════════════╗
**╠➳➠ 𝗧𝗲𝗹𝗲𝘁𝗵𝗼𝗻 :**  `{}`
**╠➳➠ 𝗗3𝗩𝗜𝗟𝗕𝗢𝗧  :**  **{}**
**╠➳➠ 𝗨𝗽𝘁𝗶𝗺𝗲   :**  `{}`
**╠➳➠ 𝗔𝗯𝘂𝘀𝗲    :**  **{}**
**╠➳➠ 𝗦𝘂𝗱𝗼      :**  **{}**
**╚══════════════════╝
"""

def button(page, modules):
    Row = d3vil_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(f"{d3vil_emoji} " + pair + f" {d3vil_emoji}", data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
               f"☜︎︎︎ 𝙱𝙰𝙲𝙺༆ {d3vil_emoji}", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"• ✘ •", data="close"
            ),
            custom.Button.inline(
               f"{d3vil_emoji} ༆𝙽𝙴𝚇𝚃 ☞︎︎︎️", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)
    async def inline_handler(event):
        cids = await client_id(event, event.query.user_id)
        d3vilkrisH, D3VIL_USER, d3vil_mention = cids[0], cids[1], cids[2]
        builder = event.builder
        result = None
        query = event.text
        auth = await clients_list()
        if event.query.user_id in auth and query == "d3vilbot_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            a = gvarstat("HELP_PIC")
            if a:
                help_pic = a.split(" ")[0]
            else:
                help_pic = https://telegra.ph/file/ad8abbfbcb2f93f91b10f.jpg"
            help_msg = f"🔰 **{d3vil_mention}**\n\n📍**𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍** ⭆ `{len(CMD_HELP)}` \n📍**𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍** ⭆`{len(apn)}`\n🎒 **Pαցҽ** ⭆1/{veriler[0]}"
            if help_pic == "DISABLE":
                result = builder.article(
                    f"Hey! Only use {hl}help please",
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic.endswith((".jpg", ".png")):
                result = builder.photo(
                    help_pic,
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic:
                result = builder.document(
                    help_pic,
                    text=help_msg,
                    title="D3vilBot Alive",
                    buttons=veriler[1],
                    link_preview=False,
                )
        elif event.query.user_id in auth and query == "alive":
            uptime = await get_time((time.time() - StartTime))
            alv_msg = gvarstat("ALIVE_MSG") or "»»» <b>ɖ3ʋɨʟɮօȶ ɨֆ օռʟɨռɛ</b> «««"
            d3v_il = alive_txt.format(alv_msg, tel_ver, d3vil_ver, uptime, abuse_m, is_sudo)
            alv_btn = [
                [Button.url(f"{D3VIL_USER}", f"tg://openmessage?user_id={d3vilkrisH}")],
                [Button.url("My Channel", f"https://t.me/{my_channel}"), 
                Button.url("𝖬𝗒 𝖦𝗋𝗈𝗎𝗉", f"https://t.me/{my_group}")],
            ]
            a = gvarstat("ALIVE_PIC")
            pic_list = []
            if a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://telegra.ph/file/ad8abbfbcb2f93f91b10f.jpg"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    PIC,
                    text=d3v_il,
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            elif PIC:
                result = builder.document(
                    PIC,
                    text=d3v_il,
                    title="D3vilBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            else:
                result = builder.article(
                    text=d3v_il,
                    title="D3vilBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )

        elif event.query.user_id in auth and query == "pm_warn":
            CSTM_PMP = gvarstat("CUSTOM_PMPERMIT") or "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
            D3VIL_FIRST = "**🔥  ᗪ3ᏉᎥᏝᏰᎧᏖ Prîvã†é Sêçürïty Prø†öçõl 🔥**\n\nHello!! Welcome to {}'s PM. This is an automated message.\n\n{}".format(d3vil_mention, CSTM_PMP)
            a = gvarstat("PMPERMIT_PIC")
            pic_list = []
            if a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://telegra.ph/file/58df4d86400922aa32acd.jpg"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    file=PIC,
                    text=D3VIL_FIRST,
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            elif PIC:
                result = builder.document(
                    file=PIC,
                    text=D3VIL_FIRST,
                    title="D3vilbot PM Permit",
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=D3VIL_FIRST,
                    title="D3vilbot PM Permit",
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
                
        elif event.query.user_id in auth and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**⚜️ 𝙻𝙴𝙶𝙴𝙽𝙳𝙰𝚁𝚈 𝙰𝙵 𝚃𝙴𝙰𝙼 𝙳3𝚅𝙸𝙻 ⚜️**",
                buttons=[
                    [Button.url("📑 𝚁𝙴𝙿𝙾 📑", "https://github.com/TEAM-D3VIL/D3vilBot")],
                    [Button.url("Update", "https://t.me/D3VIL_BOT_OFFICIAL")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[‏‏‎ ‎]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@D3VIL_BOT_OFFICIAL",
                text="""**Hey! This is [ᗪ3ᏉᎥᏝᏰᎧᏖ](https://t.me/D3VIL_BOT_OFFICIAL) \nYou can know more about me from the links given below 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 𝙲𝙷𝙰𝙽𝙽𝙴𝙻🔥", "https://t.me/D3VIL_BOT_OFFICIAL"),
                        custom.Button.url("⚡ 𝙶𝚁𝙾𝚄𝙿 ⚡", "https://t.me/D3VIL_BOT_SUPPORT"),
                    ],
                    [
                        custom.Button.url("✨ 𝚁𝙴𝙿𝙾 ✨", "https://github.com/TEAM-D3VIL/D3vilBot"),
                        custom.Button.url("🔰 TUTORIAL 🔰", "https://youtu.be/PHJ3O34Pvc0"),
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for Other Users..."
        else:
            reply_pop_up_alert = "🔰 This is ᗪ3ᏉᎥᏝᏰᎧᏖ PM Security to keep away unwanted retards from spamming PM !!"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit("✅ **Request Registered** \n\nMy master will now decide to look for your request or not.\n😐 Till then wait patiently and don't spam!!")
           target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(LOG_GP, f"#PM_REQUEST \n\n⚜️ You got a PM request from [{first_name}](tg://user?id={event.query.user_id}) !")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(f"As you wish. **BLOCKED !!**")
            await H1(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(LOG_GP, f"#BLOCK \n\n**Blocked** [{first_name}](tg://user?id={event.query.user_id}) \nReason:- PM Self Block")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
        cids = await client_id(event, event.query.user_id)
        d3vilkrisH, D3VIL_USER, d3vil_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            current_page_number=0
            simp = button(current_page_number, CMD_HELP)
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            await event.edit(
                f"🔰 **{d3vil_mention}**\n\n📍**𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍** ⭆ `{len(CMD_HELP)}` \n📍**𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍** ⭆`{len(apn)}`\n🎒 **Pαցҽ** ⭆1/{veriler[0]}",
                buttons=simp[1],
                link_preview=False,
            )
        else:
            reply_pop_up_alert = "You are not authorized to use me! \n© ᗪ3ᏉᎥᏝᏰᎧᏖ ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        cids = await client_id(event, event.query.user_id)
        d3vilkrisH, D3VIL_USER, d3vil_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            veriler = custom.Button.inline(f"{d3vil_emoji} Re-Open Menu {d3vil_emoji}", data="reopen")
            await event.edit(f"**⚜️ ᗪ3ᏉᎥᏝᏰᎧᏖ Mêñû Prõvîdêr ìs ñôw Çlösëd ⚜️**\n\n**Bot Of :**  {d3vil_mention}\n\n        [©️ ᗪ3ᏉᎥᏝᏰᎧᏖ ™️]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "You are not authorized to use me! \n© ᗪ3ᏉᎥᏝᏰᎧᏖ ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        cids = await client_id(event, event.query.user_id)
        d3vilkrisH, D3VIL_USER, d3vil_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id in auth:
            await event.edit(
                f"🔰 **{d3vil_mention}**\n\n📍**𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍** ⭆ `{len(CMD_HELP)}`\n📍**𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍** ⭆`{len(apn)}`\n🎒 **Pαցҽ** ⭆{page + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer("You are not authorized to use me! \n© ᗪ3ᏉᎥᏝᏰᎧᏖ ™", cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)")))
    async def Information(event):
        cids = await client_id(event, event.query.user_id)
        d3vilkrisH, D3VIL_USER, d3vil_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline("⚡ " + cmd[0] + " ⚡", data=f"commands[{commands}[{page}]]({cmd[0]})")
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer("No Description is written for this plugin", cache_time=0, alert=True)

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{d3vil_emoji} Main Menu {d3vil_emoji}", data=f"page({page})")])
        if event.query.user_id in auth:
            await event.edit(
                f"**📗 File :**  `{commands}`\n**🔢 Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer("You are not authorized to use me! \n© ᗪ3ᏉᎥᏝᏰᎧᏖ ™", cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)")))
    async def commands(event):
        cids = await client_id(event, event.query.user_id)
        d3vilkrisH, D3VIL_USER, d3vil_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**📗 File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**ℹ️ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n"
        sextraa = CMD_HELP_BOT[cmd]["extra"]
        if sextraa:
            a = sorted(sextraa.keys())
            for b in a:
                c = b
                d = sextraa[c]["content"]
                result += f"**{c} :**  `{d}`\n"
        result += "\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**💬 Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**💬 Explanation :**  `{command['usage']}`\n"
            result += f"**⌨️ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id in auth:
            await event.edit(
                result,
                buttons=[custom.Button.inline(f"{d3vil_emoji} Return {d3vil_emoji}", data=f"Information[{page}]({cmd})")],
                link_preview=False,
            )
        else:
            return await event.answer("You are not authorized to use me! \n© ᗪ3ᏉᎥᏝᏰᎧᏖ ™", cache_time=0, alert=True)


