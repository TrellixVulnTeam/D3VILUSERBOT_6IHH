#credit goes to @Chirag_Bhargava & Hellboy owner 
#modified by @D3_krish

import asyncio
import base64
import os
import time

from telethon import functions, types
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import *

SUDO_WALA = Config.SUDO_USERS
lg_id = Config.LOGGER_ID



@bot.on(d3vil_cmd(pattern="fspam (.*)"))
@bot.on(sudo_cmd(pattern="fspam (.*)", allow_sudo=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[7:11])
        spam_message = str(e.text[12:])
        rd = int(counter % 100)
        tot = int((counter - rd )/100)
        a= 30
        for q in range(tot):
            for p in range(100):
                await asyncio.wait([e.respond(spam_message)])
            a = a +2
            await asyncio.sleep(a)

        await e.delete()
        await e.client.send_message(
            lg_id, f"#SPAM \n\nSpammed  {counter}  messages!!"
        )

CmdHelp("fspam").add_command(
  "fspam", "<number> <text>", "spams a message 'X'number of times without flood wait!.", ".spam 9999 Hello"
).add_warning(
  "⚠️ But may you can get ban form Telegram if you will do spam too long"
).add()
