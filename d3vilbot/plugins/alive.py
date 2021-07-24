from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

#-------------------------------------------------------------------------------

d3vil_pic = Config.ALIVE_PIC or "https://telegra.ph/file/5abfcff75e1930dcdfaf3.mp4"
pm_caption = "  __**🔥🔥𝐃3𝐕𝐈𝐋 𝐁𝐎𝐓 𝐈𝐒 𝐀𝐋𝐈𝐕𝐄🔥🔥**__\n\n"

pm_caption += f"**━━━━━━━━━━━━━━━━━━━━**\n\n"
pm_caption += (
    f"                 👑𝐌𝐀𝐒𝐓𝐄𝐑👑\n  **『 {d3vil_mention} 』**\n\n"
)
pm_caption += f"┏━━━━━━━━━━━━━━━━━━━\n"
pm_caption += f"┣•➳➠ `Telethon:` `{tel_ver}` \n"
pm_caption += f"┣•➳➠ `Version:` `{d3vil_ver}`\n"
pm_caption += f"┣•➳➠ `Sudo:` `{is_sudo}`\n"
pm_caption += f"┣•➳➠ `Channel:` [ᴊᴏɪɴ](https://t.me/D3VIL_SUPPORT)\n"
pm_caption += f"┣•➳➠ `Creator:` [D3кяιsн](https://t.me/D3_krish)\n"
pm_caption += f"┗━━━━━━━━━━━━━━━━━━━\n"
pm_caption += " [⚡REPO⚡](https://github.com/D3KRISH/D3vilBot) ✘ [⚡License⚡](https://github.com/D3KRISH/D3vilBot/blob/main/LICENSE)"


#-------------------------------------------------------------------------------

@bot.on(d3vil_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def up(d3vil):
    if d3vil.fwd_from:
        return
    await d3vil.get_chat()
    await d3vil.delete()
    await bot.send_file(d3vil.chat_id, d3vil_pic, caption=pm_caption)
    await d3vil.delete()

CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "d3vil", None, "Shows Inline Alive Menu with more details."
).add()
