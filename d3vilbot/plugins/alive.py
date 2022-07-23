from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

ludosudo = Config.SUDO_USERS

if ludosudo:
    sudou = "True"
else:
    sudou = "False"


edit_time = 16
""" =======================CONSTANTS====================== """
#file1 = "https://telegra.ph/file/e441ee749e930d4f99a6d.jpg"
file1 = Config.ALIVE_PIC
file2 = "https://telegra.ph/file/4cc2b6c2702a1a9c96469.mp4"
file3 = "https://telegra.ph/file/c00cbf9a5331faad7913d.mp4"
file4 = "https://telegra.ph/file/4da06dc332ded806e2705.mp4"
""" =======================CONSTANTS====================== """
pm_caption = "  __**𖣘𖣘𝙳3𝚅𝙸𝙻 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝙸𝚂 𝙰𝙻𝙸𝚅𝙴𖣘𖣘**__\n\n"
pm_caption += f"**━━━━━━━━━━━━━━━━━━━━**\n\n"
pm_caption += (
    f"                 𝙼𝙰𝚂𝚃𝙴𝚁\n  **『 {d3vil_mention} 』**\n\n"
)
pm_caption += f"╔══════════════════╗\n"
pm_caption += f"╠•➳➠ `𝖳𝖾𝗅𝖾𝗍𝗁𝗈𝗇:` `{tel_ver}` \n"
pm_caption += f"╠•➳➠ `𝖵𝖾𝗋𝗌𝗂𝗈𝗇:` `{d3vil_ver}`\n"
pm_caption += f"╠•➳➠ `𝖲𝗎𝖽𝗈:` `{is_sudo}`\n"
pm_caption += f"╠•➳➠ `𝖢𝗁𝖺𝗇𝗇𝖾𝗅:` [𝙹𝗈𝗂𝗇](https://t.me/D3VIL_BOT_OFFICIAL)\n"
pm_caption += f"╠•➳➠ `𝖢𝗋𝖾𝖺𝗍𝗈𝗋:` [𝙳3𝙺𝚁𝙸𝚂𝙷](https://t.me/D3_krish)\n"
pm_caption += f"╠•➳➠ `𝖮𝗐𝗇𝖾𝗋:` [𝙳3𝚅𝙸𝙻𝙶𝚄𝙻𝚂𝙷𝙰𝙽](https://t.me/D3VILGULSHAN)\n"
pm_caption += f"╚══════════════════╝\n"
pm_caption += " [⚡REPO⚡](https://github.com/TEAM-D3VIL/D3vilBot) 🔹 [📜License📜](https://github.com/TEAM-D3VIL/D3vilBot/blob/main/LICENSE)"

 # @command(outgoing=True, pattern="^.alive$")
@bot.on(admin_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    await alive.get_chat()   
    
    on = await borg.send_file(alive.chat_id, file=file1,caption=pm_caption)

    await asyncio.sleep(edit_time)
    ok = await borg.edit_message(alive.chat_id, on, file=file2) 

    await asyncio.sleep(edit_time)
    ok2 = await borg.edit_message(alive.chat_id, ok, file=file3)

    await asyncio.sleep(edit_time)
    ok3 = await borg.edit_message(alive.chat_id, ok2, file=file1)
    
    await asyncio.sleep(edit_time)
    ok4 = await borg.edit_message(alive.chat_id, ok3, file=file3)
    
    await asyncio.sleep(edit_time)
    ok5 = await borg.edit_message(alive.chat_id, ok4, file=file2)
    
    await asyncio.sleep(edit_time)
    ok6 = await borg.edit_message(alive.chat_id, ok5, file=file4)
    
    await asyncio.sleep(edit_time)
    ok7 = await borg.edit_message(alive.chat_id, ok6, file=file1)
    
    await asyncio.sleep(edit_time)
    ok8 = await borg.edit_message(alive.chat_id, ok7, file=file2) 

    await asyncio.sleep(edit_time)
    ok9 = await borg.edit_message(alive.chat_id, ok8, file=file3)

    await asyncio.sleep(edit_time)
    ok10 = await borg.edit_message(alive.chat_id, ok9, file=file1)
    
    await asyncio.sleep(edit_time)
    ok11 = await borg.edit_message(alive.chat_id, ok10, file=file3)
    
    await asyncio.sleep(edit_time)
    ok12 = await borg.edit_message(alive.chat_id, ok11, file=file2)
    
    await asyncio.sleep(edit_time)
    ok13 = await borg.edit_message(alive.chat_id, ok12, file=file4)
    
    await asyncio.sleep(edit_time)
    ok14 = await borg.edit_message(alive.chat_id, on, file=file1)

    """ For .alive command, check if the bot is running.  """
    await borg.send_file(alive.chat_id, caption=pm_caption)
    await alive.delete()
    
msg = f"""
**⚡ 𝐃3𝐕𝐈𝐋𝐁𝐎𝐓 𝐈𝐒 𝐎𝐍𝐋𝐈𝐍𝐄 ⚡**
{Config.ALIVE_MSG}
**🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅**
**↼𝗠𝗔𝗦𝗧𝗘𝗥⇀   :**  **『{d3vil_mention}』**
**╔══════════════════╗**
**╠➳➠ 𝗧𝗲𝗹𝗲𝘁𝗵𝗼𝗻 :**  `{tel_ver}`
**╠➳➠ 𝗗3𝗩𝗜𝗟𝗕𝗢𝗧  :**  **{d3vil_ver}**
**╠➳➠ 𝗨𝗽𝘁𝗶𝗺𝗲   :**  `{uptime}`
**╠➳➠ 𝗔𝗯𝘂𝘀𝗲    :**  **{abuse_m}**
**╠➳➠ 𝗦𝘂𝗱𝗼      :**  **{is_sudo}**
**╚══════════════════╝
"""
botname = Config.BOT_USERNAME

@d3vilbot.on(d3vil_cmd(pattern="d3vil$"))
@d3vilbot.on(sudo_cmd(pattern="d3vil$", allow_sudo=True))
async def d3vil_a(event):
    try:
        d3vil = await bot.inline_query(botname, "alive")
        await d3vil[0].click(event.chat_id)
        if event.sender_id == d3krish:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "d3vil", None, "Shows Inline Alive Menu with more details."
).add()
