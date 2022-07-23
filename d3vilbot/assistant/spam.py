from telethon import events
from d3vilbot.utils import *

MY_USERS = bot.uid

a = False

@tgbot.on(events.NewMessage(pattern="^/spam"))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:8])
        spam_message = str(e.text[8:])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()
