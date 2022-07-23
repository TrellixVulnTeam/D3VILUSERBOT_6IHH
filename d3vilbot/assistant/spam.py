from telethon import events
from d3vilbot.utils import *

MY_USERS = bot.uid
TELE_NAME = bot.me.first_name
OWNER_ID = bot.me.id


a = False

@tgbot.on(events.NewMessage(pattern="^/spam"))
async def spam(e):
            return await e.reply(usage, parse_mode=None, link_preview=None )
        d3vil = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        smex = await e.get_reply_message()
        if len(d3vil) == 2:
            message = str(d3vil[1])
            counter = int(d3vil[0])
            if counter > 100:
                return await e.reply(error, parse_mode=None, link_preview=None )
            await asyncio.wait([e.respond(message) for i in range(counter)])
        elif e.reply_to_msg_id and smex.media:  
            counter = int(d3vil[0])
            if counter > 100:
                return await e.reply(error, parse_mode=None, link_preview=None )
            for _ in range(counter):
                smex = await e.client.send_file(e.chat_id, smex, caption=smex.text)
                await gifspam(e, smex)  
        elif e.reply_to_msg_id and smex.text:
            message = smex.text
            counter = int(d3vil[0])
            if counter > 100:
                return await e.reply(error, parse_mode=None, link_preview=None )
            await asyncio.wait([e.respond(message) for i in range(counter)])
        else:
            await e.reply(usage, parse_mode=None, link_preview=None )
            
