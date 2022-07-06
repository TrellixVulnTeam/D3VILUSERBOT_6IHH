from telethon import custom, events
from telethon.tl.types import Channel
from telethon.utils import get_display_name

from . import *

if Config.TAG_LOGGER:
    tagger = int(Config.TAG_LOGGER)

if Config.TAG_LOGGER:
    @d3vil_handler(func=lambda e: (e.mentioned))
    async def all_messages_catcher(event):
        ammoca_message = ""
        __, _, d3vil_men = await client_id(event)
        d3vilkrish  = await event.client.get_entity(event.sender_id)
        if d3vilkrish .bot or d3vilkrish .verified or d3vilkrish .support:
            return
        d3krish  = f"[{get_display_name(d3vilkrish )}](tg://user?id={d3vilkrish .id})"
        where_ = await event.client.get_entity(event.chat_id)
        where_m = get_display_name(where_)
        button_text = "See the tag 📬"
        if isinstance(where_, Channel):
            message_link = f"https://t.me/c/{where_.id}/{event.id}"
        else:
            message_link = f"tg://openmessage?chat_id={where_.id}&message_id={event.id}"
        ammoca_message += f"👆 #TAG\n\n**• Tag By :** {d3krish } \n**• Tag For :** {d3vil_men} \n**• Chat :** [{where_m}]({message_link})"
        if tagger is not None:
            await tbot.forward_messages(tagger, event.message)
            await tbot.send_message(
                entity=tagger,
                message=ammoca_message,
                link_preview=False,
                buttons=[[custom.Button.url(button_text, message_link)]],
                silent=True,
            )
        else:
            return


@d3vil_cmd(pattern="tagall(?:\s|$)([\s\S]*)")
async def _(event):
    mentions = event.text[8:]
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 50):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions)
    await event.delete()


CmdHelp("tagger").add_command(
  "tagall", "<text>", "Tags recent 100 users in the group."
).add_info(
  "Tagger."
).add_warning(
  "✅ Harmless Module."
).add()
