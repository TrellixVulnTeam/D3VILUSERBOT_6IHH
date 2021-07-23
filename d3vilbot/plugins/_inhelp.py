from math import ceil
from re import compile
import asyncio
import html
import os
import re
import sys

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from . import *

d3vil_row = Config.BUTTONS_IN_HELP
d3vil_emoji = Config.EMOJI_IN_HELP
d3vil_pic = Config.PMPERMIT_PIC or "https://telegra.ph/file/ad8abbfbcb2f93f91b10f.jpg"
cstm_pmp = Config.CUSTOM_PMPERMIT
ALV_PIC = Config.ALIVE_PIC

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**🚫 Blocked and Reported**"

D3VIL_FIRST = (
    "**🔥 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 Prîvã†é Sêçürïty Prø†öçõl 🔥**\n\nThis is to inform you that "
    "{} is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**Please Choose Why You Are Here!!**".format(d3vil_mention, mssge))

alive_txt = """
**⚜️ 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 𝔦𝔰 𝔬𝔫𝔩𝔦𝔫𝔢 ⚜️**
{}
**🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅**

**Telethon :**  `{}`
**𝔇3𝔳𝔦𝔩𝔅𝔬𝔱  :**  **{}**
**Uptime   :**  `{}`
**Abuse    :**  **{}**
**Sudo      :**  **{}**
"""

def button(page, modules):
    Row = d3vil_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::3], modules[1::3])))
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
               f"{d3vil_emoji} ༆𝙽𝙴𝚇𝚃 ☞︎︎︎", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query == "d3vilbot_d3vlp":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            result = await builder.article(
                f"Hey! Only use .d3vlp please",
                text=f"『 **{d3vil_mention}』**\n\n📜 __𝑁𝑜.𝑜𝑓 𝑃𝑙𝑢𝑔𝑖𝑛𝑠__ : `{len(CMD_HELP)}` \n🗒️ __𝑃𝑎𝑔𝑒__ : 1/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        elif event.query.user_id == bot.uid and query.startswith("fsub"):
            hunter = event.pattern_match.group(1)
            d3vil = hunter.split("+")
            user = await bot.get_entity(int(d3vil[0]))
            channel = await bot.get_entity(int(d3vil[1]))
            msg = f"**👋 𝑊𝑒𝑙𝑐𝑜𝑚𝑒** [{user.first_name}](tg://user?id={user.id}), \n\n** 𝑌𝑜𝑢 𝑛𝑒𝑒𝑑 𝑡𝑜 𝐽𝑜𝑖𝑛** {channel.title} **𝑡𝑜 𝑐𝒉𝑎𝑡 𝑖𝑛 𝑡𝒉𝑖𝑠 𝑔𝑟𝑜𝑢𝑝.**"
            if not channel.username:
                link = (await bot(ExportChatInviteRequest(channel))).link
            else:
                link = "https://t.me/" + channel.username
            result = [
                await builder.article(
                    title="force_sub",
                    text = msg,
                    buttons=[
                        [Button.url(text="Channel", url=link)],
                        [custom.Button.inline("🔓 𝑈𝑛𝑚𝑢𝑡𝑒 𝑀𝑒", data=unmute)],
                    ],
                )
            ]

        elif event.query.user_id == bot.uid and query == "alive":
            kr_ish = alive_txt.format(Config.ALIVE_MSG, tel_ver, d3vil_ver, uptime, abuse_m, is_sudo)
            alv_btn = [
                [Button.url(f"{D3VIL_USER}", f"tg://openmessage?user_id={d3krish}")],
                [Button.url("My Channel", f"https://t.me/{my_channel}"), 
                Button.url("My Group", f"https://t.me/{my_group}")],
            ]
            if ALV_PIC and ALV_PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    ALV_PIC,
                    text=kr_ish,
                    buttons=alv_btn,
                    link_preview=False,
                )
            elif ALV_PIC:
                result = builder.document(
                    ALV_PIC,
                    text=kr_ish,
                    title="D3vilBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=kr_ish,
                    title="D3vilBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )

        elif event.query.user_id == bot.uid and query == "pm_warn":
            d3vl_l = D3VIL_FIRST.format(d3vil_mention, mssge)
            result = builder.photo(
                file=d3vil_pic,
                text=d3vl_l,
                buttons=[
                    [
                        custom.Button.inline("📝 𝑅𝑒𝑞𝑢𝑒𝑠𝑡 📝", data="req"),
                        custom.Button.inline("💬 𝐶𝒉𝑎𝑡 💬", data="chat"),
                    ],
                    [custom.Button.inline("🚫 𝑆𝑝𝑎𝑚 🚫", data="heheboi")],
                    [custom.Button.inline("𝐶𝑢𝑟𝑖𝑜𝑢𝑠 ❓", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**[⚜️ 𝙻𝙴𝙶𝙴𝙽𝙳𝙰𝚁𝚈 𝙰𝙵 𝚃𝙴𝙰𝙼 𝙳3𝚅𝙸𝙻 ⚜️](https://t.me/D3VIL_SUPPORT)**",
                buttons=[
                    [Button.url("📑 𝑅𝑒𝑝𝑜 📑", "https://github.com/TEAM-D3VIL/D3vilBot")],
                    [Button.url("🚀 𝐷𝑒𝑝𝑙𝑜𝑦 🚀", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FTEAM-D3VIL%2FD3vilBot&template=https%3A%2F%2Fgithub.com%2FTEAM-D3VIL%2FD3vilBot")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**𝐹𝑖𝑙𝑒 𝑢𝑝𝑙𝑜𝑎𝑑𝑒𝑑 𝑠𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑙𝑦 𝑡𝑜 {part[2]} site.\n\n𝑈𝑝𝑙𝑜𝑎𝑑 𝑇𝑖𝑚𝑒 : {part[1][:3]} 𝑠𝑒𝑐𝑜𝑛𝑑\n[‏‏‎ ‎]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@D3VIL_SUPPORT",
                text="""**𝐻𝑒𝑦! 𝑇𝒉𝑖𝑠 𝑖𝑠 [✘•𝙳3𝚅𝙸𝙻𝙱𝙾𝚃•✘](https://t.me/D3VIL_OP_BOLTE)  \nYou 𝑐𝑎𝑛 𝑘𝑛𝑜𝑤 𝑚𝑜𝑟𝑒 𝑎𝑏𝑜𝑢𝑡 𝑚𝑒 𝑓𝑟𝑜𝑚 𝑡𝒉𝑒 𝑙𝑖𝑛𝑘𝑠 𝑔𝑖𝑣𝑒𝑛 𝑏𝑒𝑙𝑜𝑤 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 🔥", "https://t.me/D3VIL_SUPPORT"),
                        custom.Button.url(
                            "⚡ 𝙶𝚁𝙾𝚄𝙿 ⚡", "https://t.me/D3VIL_BOT_SUPPORT"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "✨ 𝚁𝙴𝙿𝙾 ✨", "https://github.com/D3KRISH/D3vilBot"),
                        custom.Button.url
                    (
                            "🔰 𝙾𝚆𝙽𝙴𝚁 🔰", "https://t.me/D3_krish"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for Other Users..."
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"🔰 𝑇𝒉𝑖𝑠 𝑖𝑠 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 𝑃𝑀 𝑆𝑒𝑐𝑢𝑟𝑖𝑡𝑦 𝑓𝑜𝑟 {d3vil_mention} 𝑡𝑜 𝑘𝑒𝑒𝑝 𝑎𝑤𝑎𝑦 𝑢𝑛𝑤𝑎𝑛𝑡𝑒𝑑 𝑟𝑒𝑡𝑎𝑟𝑑𝑠 𝑓𝑟𝑜𝑚 𝑠𝑝𝑎𝑚𝑚𝑖𝑛𝑔 𝑃𝑀..."
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"✅ **𝑅𝑒𝑞𝑢𝑒𝑠𝑡 𝑅𝑒𝑔𝑖𝑠𝑡𝑒𝑟𝑒𝑑** \n\n{d3vil_mention} 𝑤𝑖𝑙𝑙 𝑛𝑜𝑤 𝑑𝑒𝑐𝑖𝑑𝑒 𝑡𝑜 𝑙𝑜𝑜𝑘 𝑓𝑜𝑟 𝑦𝑜𝑢𝑟 𝑟𝑒𝑞𝑢𝑒𝑠𝑡 𝑜𝑟 𝑛𝑜𝑡.\n😐 𝑇𝑖𝑙𝑙 𝑡𝒉𝑒𝑛 𝑤𝑎𝑖𝑡 𝑝𝑎𝑡𝑖𝑒𝑛𝑡𝑙𝑦 𝑎𝑛𝑑 𝑑𝑜𝑛'𝑡 𝑠𝑝𝑎𝑚!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**👀 𝐻𝑒𝑦 {d3vil_mention} !!** \n\n⚜️ 𝑌𝑜𝑢 𝐺𝑜𝑡 𝐴 𝑅𝑒𝑞𝑢𝑒𝑠𝑡 𝐹𝑟𝑜𝑚 [{first_name}](tg://user?id={ok}) 𝐼𝑛 𝑃𝑀!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"chat")))
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Ahh!! You here to do chit-chat!!\n\nPlease wait for {d3vil_mention} to come. Till then keep patience and don't spam."
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**👀 Hey {d3vil_mention} !!** \n\n⚜️ You Got A PM from  [{first_name}](tg://user?id={ok})  for random chats!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"🥴 **Nikal lawde\nPehli fursat me nikal**"
            )
            await bot(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await bot.send_message(
                LOG_GP,
                f"**𝐵𝑙𝑜𝑐𝑘𝑒𝑑**  [{first_name}](tg://user?id={ok}) \n\n𝑅𝑒𝑎𝑠𝑜𝑛:- 𝑆𝑝𝑎𝑚",
            )


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"unmute")))
    async def on_pm_click(event):
        hunter = (event.data_match.group(1)).decode("UTF-8")
        d3vil = hunter.split("+")
        if not event.sender_id == int(d3vil[0]):
            return await event.answer("This Ain't For You!!", alert=True)
        try:
            await bot(GetParticipantRequest(int(d3vil[1]), int(d3vil[0])))
        except UserNotParticipantError:
            return await event.answer(
                "You need to join the channel first.", alert=True
            )
        await bot.edit_permissions(
            event.chat_id, int(d3vil[0]), send_message=True, until_date=None
        )
        await event.edit("Yay! You can chat now !!")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
            if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
                current_page_number=0
                simp = button(current_page_number, CMD_HELP)
                veriler = button(0, sorted(CMD_HELP))
                apn = []
                for x in CMD_LIST.values():
                    for y in x:
                        apn.append(y)
                await event.edit(
                    f" **『{d3vil_mention}』**\n\n📜 __𝑁𝑜.𝑜𝑓 𝑃𝑙𝑢𝑔𝑖𝑛𝑠__ : `{len(CMD_HELP)}` \n🗒️ __𝙿𝙰𝙶𝙴__ : 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = "𝐻𝑜𝑜 𝑔𝑦𝑎 𝑎𝑎𝑝𝑘𝑎. 𝐾𝑎𝑏𝑠𝑒 𝑡𝑎𝑝𝑎𝑟 𝑡𝑎𝑝𝑎𝑟 𝑑𝑎𝑏𝑎𝑒 𝑗𝑎𝑎 𝑟𝒉𝑒 𝒉. 𝐾𝒉𝑢𝑑𝑘𝑎 bna 𝑙𝑜 𝑛𝑎 𝑎𝑔𝑟 𝑐𝒉𝑎𝑖𝑦𝑒 𝑡𝑜. © 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 ™"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            veriler = custom.Button.inline(f"{d3vil_emoji} Re-Open Menu {d3vil_emoji}", data="reopen")
            await event.edit(f"**⚜️ 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 Mêñû Prõvîdêr ìs ñôw Çlösëd ⚜️**\n\n**Bot Of :**  {d3vil_mention}\n\n        [©️ 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 ™️]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "𝐻𝑜𝑜 𝑔𝑦𝑎 𝑎𝑎𝑝𝑘𝑎. 𝐾𝑎𝑏𝑠𝑒 𝑡𝑎𝑝𝑎𝑟 𝑡𝑎𝑝𝑎𝑟 𝑑𝑎𝑏𝑎𝑒 𝑗𝑎𝑎 𝑟𝒉𝑒 𝒉. 𝐾𝒉𝑢𝑑𝑘𝑎 𝑏𝑛𝑎 𝑙𝑜 𝑛𝑎 𝑎𝑔𝑟 𝑐𝒉𝑎𝑖𝑦𝑒 𝑡𝑜. © 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f" **『{d3vil_mention}』**\n\n📜 __𝑁𝑜.𝑜𝑓 𝑃𝑙𝑢𝑔𝑖𝑛𝑠__ : `{len(CMD_HELP)}`\n🗂️ __𝐶𝑜𝑚𝑚𝑎𝑛𝑑𝑠__ : `{len(apn)}`\n🗒️ __𝑃𝑎𝑔𝑒__ : {page + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. © 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 ™",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "✘ " + cmd[0] + " 1✘", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{d3vil_emoji} Main Menu {d3vil_emoji}", data=f"page({page})")])
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"**📗 𝐹𝑖𝑙𝑒 :**  `{commands}`\n**🔢 𝑁𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑐𝑜𝑚𝑚𝑎𝑛𝑑𝑠 :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "𝐻𝑜𝑜 𝑔𝑦𝑎 𝑎𝑎𝑝𝑘𝑎. 𝐾𝑎𝑏𝑠𝑒 𝑡𝑎𝑝𝑎𝑟 𝑡𝑎𝑝𝑎𝑟 𝑑𝑎𝑏𝑎𝑒 𝑗𝑎𝑎 rhe 𝒉. 𝐾𝒉𝑢𝑑𝑘𝑎 𝑏𝑛𝑎 𝑙𝑜 𝑛𝑎 𝑎𝑔𝑟 𝑐𝒉𝑎𝑖𝑦𝑒 𝑡𝑜. © 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 ™",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**📗 File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**ℹ️ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n\n"
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
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(f"{d3vil_emoji} Return {d3vil_emoji}", data=f"Information[{page}]({cmd})")
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "𝐻𝑜𝑜 𝑔𝑦𝑎 𝑎𝑎𝑝𝑘𝑎. 𝐾𝑎𝑏𝑠𝑒 𝑡𝑎𝑝𝑎𝑟 𝑡𝑎𝑝𝑎𝑟 𝑑𝑎𝑏𝑎𝑒 𝑗𝑎𝑎 𝑟𝒉𝑒 𝒉. 𝐾𝒉𝑢𝑑𝑘𝑎 𝑏𝑛𝑎 𝑙𝑜 𝑛𝑎 𝑎𝑔𝑟 𝑐𝒉𝑎𝑖𝑦𝑒 𝑡𝑜. © 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 ™",
                cache_time=0,
                alert=True,
            )


# d3vilbot
