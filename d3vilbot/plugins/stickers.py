import asyncio
import io
import math
import os
import random
import textwrap
import urllib.request

from os import remove
from PIL import Image, ImageDraw, ImageFont
from telethon import Button, events
from telethon.errors import PackShortNameOccupiedError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeSticker, InputStickerSetID, MessageMediaPhoto, InputMessagesFilterDocument
from telethon.utils import get_input_document

from d3vilbot.sql.gvar_sql import addgvar, gvarstat
from . import *

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "hehe me stel ur stikér\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pacc looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ",
    "Hey! That's my sticker. Lemme get it back...",
    "Turn around, Go straight and f*ck off...",
]


@d3vil_cmd(pattern="kang(?:\s|$)([\s\S]*)")
async def kang(event):
    user = await event.client.get_me()
    d3vilkrish, D3VIL_USER, d3vil_mention = await client_id(event)
    un = f"@{user.username}" if user.username else D3VIL_USER
    un_ = user.username if user.username else d3vilkrish
    message = await event.get_reply_message()
    d3vilbot = gvarstat("STICKER_PACKNAME")
    photo = None
    emojibypass = False
    is_anim = False
    is_vid = False
    emoji = None
    if message and message.media:
        if message.photo:
            d3vil = await eor(event, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await event.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            d3vil = await eor(event, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await event.client.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            d3vil = await eor(event, f"`{random.choice(KANGING_STR)}`")
            await event.client.download_file(message.media.document, "AnimatedSticker.tgs")

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            emojibypass = True
            is_anim = True
            photo = 1
        elif "video" in message.media.document.mime_type.split("/"):
            if message.media.document.mime_type == "video/webm":
                attributes = message.media.document.attributes
                for attribute in attributes:
                    if isinstance(attribute, DocumentAttributeSticker):
                        d3vil = await eor(event, f"Oow! A video sticker... **[ ENCODING ]**")
                        VS = await VSticker(event, message)
                        await eor(d3vil, f"`{random.choice(KANGING_STR)}`")
                        emoji = attribute.alt
                        emojibypass = True
            elif message.media.document.mime_type == "video/mp4":
                d3vil = await eor(event, "Oow! A video... **[ Converting ]**")
                VS = await VSticker(event, message)
                await eor(d3vil, f"`{random.choice(KANGING_STR)}`")
            is_vid = True
            photo = 1
        else:
            await eod(event, "`Unsupported File!`")
            return
    else:
        await eod(event, "`I can't kang that...`")
        return

    if photo:
        splat = event.text.split()
        if not emojibypass:
            emoji = "😎"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                pack = int(splat[1])
                emoji = "😎"
            else:
                pack = 1
                emoji = splat[1]

        packname = f"d3vilbot_{un_}_{pack}"
        packnick = f"{d3vilbot}" if d3vilbot else f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ Vol.{pack}"
        cmd = "/newpack"
        file = io.BytesIO()

        if not is_anim and not is_vid:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        elif is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        elif is_vid:
            packname += "_vid"
            packnick += " (Video)"
            cmd = "/newvideo"

        response = urllib.request.urlopen(urllib.request.Request(f"http://t.me/addstickers/{packname}"))
        htmlstr = response.read().decode("utf8").split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with event.client.conversation("@Stickers") as conv:
                if not is_anim and not is_vid:
                    await conv.send_message("/addsticker")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    while "120" in x.text:
                        pack += 1
                        packname = f"d3vilbot_{un_}_{pack}"
                        packnick = f"{d3vilbot}" if d3vilbot else f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ Vol.{pack}"
                        cmd = "/newpack"
                        await d3vil.edit(f"`Switching to Pack {str(pack)} due to insufficient space`")
                        await conv.send_message(packname)
                        x = await conv.get_response()
                        if x.text == "Invalid set selected.":
                            await conv.send_message(cmd)
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.send_message(packnick)
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                            await conv.get_response()
                            await conv.send_message(emoji)
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await conv.send_message("/publish")
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.send_message("/skip")
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await conv.send_message(packname)
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await d3vil.edit(f"**Sticker added in a Different Pack !**\nThis Pack is Newly created!\nYour pack can be found [here](t.me/addstickers/{packname})")
                            return
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        return await eod(d3vil, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                    await conv.send_message(emoji)
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message("/done")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)

                if is_anim:
                    packname = f"d3vilbot_{un_}_{pack}_anim"
                    packnick = f"{d3vilbot}" if d3vilbot else f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ Vol.{pack} (Animated)"
                    cmd = "/newanimated"
                    await conv.send_message("/addsticker")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    while "50" in x.text:
                        pack += 1
                        await d3vil.edit(f"`Switching to Pack {str(pack)} due to insufficient space`")
                        await conv.send_message(packname)
                        x = await conv.get_response()
                        if x.text == "Invalid set selected.":
                            await conv.send_message(cmd)
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.send_message(packnick)
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                            await conv.get_response()
                            await conv.send_message(emoji)
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await conv.send_message("/publish")
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.send_message("/skip")
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await conv.send_message(packname)
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await event.client.send_read_acknowledge(conv.chat_id)
                            await d3vil.edit(f"**Sticker added in a Different Pack !**\nThis Pack is Newly created!\nYour pack can be found [here](t.me/addstickers/{packname})")
                            return
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        return await eod(d3vil, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                    await conv.send_message(emoji)
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message("/done")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)

                elif is_vid:
                    packname = f"d3vilbot_{un_}_{pack}_vid"
                    packnick = f"{d3vilbot}" if d3vilbot else f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ (Video)"
                    cmd = "/newvideo"
                    await conv.send_message("/addsticker")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_file("VideoSticker.webm")
                    remove("VideoSticker.webm")
                    xy = await conv.get_response()
                    if "50" in xy.text:
                        pack += 1
                        return await eod(d3vil, f"This Video sticker pack is already full. Use `{hl}kang {pack}` to add new stickers.")
                    elif "Sorry, the file type is invalid." in xy.text:
                        return await eod(d3vil, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                    await conv.send_message(emoji)
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message("/done")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)

        else:
            await d3vil.edit("`Preparing a new pack....`")
            async with event.client.conversation("Stickers") as conv:
                if not is_anim and not is_vid:
                    packname = f"d3vilbot_{un_}_{pack}"
                    packnick = f"{d3vilbot}" if d3vilbot else f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ Vol.{pack}"
                    cmd = "/newpack"
                    await conv.send_message(cmd)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packnick)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        return await eod(d3vil, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                    await conv.send_message(emoji)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message("/publish")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message("/skip")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
            
                if is_anim:
                    packname = f"d3vilbot_{un_}_{pack}_anim"
                    packnick = f"{d3vilbot}" if d3vilbot else f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ Vol.{pack} (Animated)"
                    cmd = "/newanimated"
                    await conv.send_message(cmd)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packnick)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        return await eod(d3vil, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                    await conv.send_message(emoji)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message("/publish")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(f"<{packnick}>")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message("/skip")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)

                if is_vid:
                    packname = f"d3vilbot_{un_}_{pack}_vid"
                    packnick = f"{d3vilbot}" if d3vilbot else f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ (Video)"
                    cmd = "/newvideo"
                    await conv.send_message(cmd)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packnick)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_file("VideoSticker.webm")
                    remove("VideoSticker.webm")
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        return await eod(d3vil, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                    await conv.send_message(emoji)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message("/publish")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message("/skip")
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    await conv.get_response()
                    await event.client.send_read_acknowledge(conv.chat_id)

        await tbot.send_message(
            Config.LOGGER_ID,
            f"#KANG #STICKER \n\n**A sticker has been kanged into the pack of {d3vil_mention}. Click below to see the pack!**",
            buttons=[[Button.url("View Pack", f"t.me/addstickers/{packname}")]],
        )
        await eod(d3vil, f"⚡** This Sticker iz [kanged](t.me/addstickers/{packname}) successfully to your pack **⚡")


async def resize_photo(photo):
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


@d3vil_cmd(pattern="stkrinfo$")
async def get_pack_info(event):
    if not event.is_reply:
        await eod(event, "`I can't fetch info from black hole!!!`")
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await eod(event, "`Reply to a sticker to get the pack details`")
        return
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        d3vil = await eor(event, "`Fetching details of the sticker pack, please wait..`")
    except BaseException:
        await eod(event, "`This is not a sticker. Reply to a sticker.`")
        return

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await d3vil.edit("`This is not a sticker. Reply to a sticker.`")
        return

    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = (
        f"🔹 **Sticker Title :** `{get_stickerset.set.title}\n`"
        f"🔸 **Sticker Short Name :** `{get_stickerset.set.short_name}`\n"
        f"🔹 **Official :** `{get_stickerset.set.official}`\n"
        f"🔸 **Archived :** `{get_stickerset.set.archived}`\n"
        f"🔹 **Stickers In Pack :** `{len(get_stickerset.packs)}`\n"
        f"🔸 **Emojis In Pack :**\n{' '.join(pack_emojis)}"
    )

    await d3vil.edit(OUTPUT)


@d3vil_cmd(pattern="delst(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        await eod(event, "`Reply to any user's message.`")
        return
    reply_message = await event.get_reply_message()
    chat = "@Stickers"
    reply_message.sender
    d3vil = await eor(event, "🥴 `Deleting sticker...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=429000)
            )
            await conv.send_message("/delsticker")
            await conv.get_response()
            await asyncio.sleep(1)
            await event.client.forward_messages(chat, reply_message)
            response = await conv.get_response()
        except YouBlockedUserError:
            await d3vil.edit("Please unblock @Stickers and try again")
            return
        await d3vil.edit(response.text)


@d3vil_cmd(pattern="editst(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        await eod(event, "`Reply to any user's message.`")
        return
    reply_message = await event.get_reply_message()
    d3bot_ = event.pattern_match.group(1)
    chat = "@Stickers"
    d3vil = await eor(event, "📝 `Editing sticker emoji...`")
    if d3bot_ == "":
        await d3vil.edit("**🤧 Nashe me hai kya lawde**")
    else:
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=429000)
                )
                await conv.send_message(f"/editsticker")
                await conv.get_response()
                await asyncio.sleep(2)
                await event.client.forward_messages(chat, reply_message)
                await conv.get_response()
                await asyncio.sleep(2)
                await conv.send_message(f"{d3bot_}")
                response = await conv.get_response()
            except YouBlockedUserError:
                await d3vil.edit("Please unblock @Stickers and try again")
                return
            await d3vil.edit(f"{response.text}")


@d3vil_cmd(pattern="pkang(?:\s|$)([\s\S]*)")
async def _(event):
    d3bot_ = await eor(event, "`Preparing pack kang...`")
    rply = await event.get_reply_message()
    d3vilkrish, D3VIL_USER, d3vil_mention = await client_id(event)
    d3vil = event.text[7:]
    bot_ = Config.BOT_USERNAME
    bot_un = bot_.replace("@", "")
    user = await event.client.get_me()
    un = f"@{user.username}" if user.username else user.first_name
    un_ = user.username if user.username else d3vilkrish
    if not rply:
        return await eod(d3bot_, "`Reply to a stciker to kang that pack.`")
    if d3vil == "":
        pname = f"{un}'s ᗪ3ᏉᎥᏝᏰᎧᏖ Pack"
    else:
        pname = d3vil
    if rply and rply.media and rply.media.document.mime_type == "image/webp":
        d3vil_id = rply.media.document.attributes[1].stickerset.id
        d3vil_hash = rply.media.document.attributes[1].stickerset.access_hash
        got_stcr = await event.client(
            functions.messages.GetStickerSetRequest(
                stickerset=types.InputStickerSetID(id=d3vil_id, access_hash=d3vil_hash)
            )
        )
        stcrs = []
        for sti in got_stcr.documents:
            inp = get_input_document(sti)
            stcrs.append(
                types.InputStickerSetItem(
                    document=inp,
                    emoji=(sti.attributes[1]).alt,
                )
            )
        x = gvarstat("PKANG")
        if x is None:
            y = addgvar("PKANG", "0")
            pack = int(y) + 1
        else:
            pack = int(x) + 1
        await d3bot_.edit("`Starting kang process...`")
        try:
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=d3vilkrish,
                    title=pname,
                    short_name=f"d3vil_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        except PackShortNameOccupiedError:
            await asyncio.sleep(1)
            await d3bot_.edit("`Pack name already occupied... making new pack`")
            pack = int(pack) + 1
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=d3vilkrish,
                    title=pname,
                    short_name=f"d3vil_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        await tbot.send_message(Config.LOGGER_ID,
                                f"#PKANG #STICKER \n\n**A sticker pack has been kanged by {d3vil_mention}. Click below to see the pack!**",
                                buttons=[[Button.url("View Pack", f"t.me/addstickers/{create_st.set.short_name}")]],
                            )
        await eod(d3bot_, f"⚡** This Sticker Pack iz [kanged](t.me/addstickers/{create_st.set.short_name}) successfully **⚡")
    else:
        await d3bot_.edit("Unsupported File. Please Reply to a sticker only.")


@d3vil_cmd(pattern="text(?:\s|$)([\s\S]*)")
async def sticklet(event):
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)

    sticktext = event.pattern_match.group(1)
    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = "\n".join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = await get_font_file(event.client, "@D3VIL_FONTSS")

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )

    image_stream = io.BytesIO()
    image_stream.name = "d3vilbot.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)


    await event.client.send_message(
        event.chat_id,
        "{}".format(sticktext),
        file=image_stream,
        reply_to=event.message.reply_to_msg_id,
    )
    try:
        os.remove(FONT_FILE)
    except:
        pass


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)


@d3vil_cmd(pattern="waifu(?:\s|$)([\s\S]*)")
async def waifu(event):
    text = event.pattern_match.group(1)
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            await eod(event, "Give some text... **PRO !!**")
            return
    animus = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
    sticcers = await event.client.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        event.chat_id,
        reply_to=event.reply_to_msg_id,
        silent=True if event.is_reply else False,
        hide_via=True,
    )
    await event.delete()


CmdHelp("stickers").add_command(
  "kang", "<emoji> <number>", "Adds the sticker to desired pack with a custom emoji of your choice. If emoji is not mentioned then default is 😎. And if number is not mentioned then Pack will go on serial wise. \n  ✓(1 pack = 120 static stickers)\n  ✓(1 pack = 50 animated & video stickers)"
).add_command(
  "stkrinfo", "<reply to sticker>", "Gets all the infos of the sticker pack"
).add_command(
  "delst", "<reply to sticker>", "Deletes The Replied Sticker from your pack."
).add_command(
  "editst", "<reply to sticker> <new emoji>", "Edits the emoji of replied sticker of your pack."
).add_command(
  "text", "<word>", "Sends the written text in sticker format."
).add_command(
  "waifu", "<word>", "Waifu writes the word for you."
).add_command(
  "pkang", "<reply to a sticker> <pack name>", "Kangs all the stickers in replied pack to your pack. Also supports custom pack name. Just give name after command.", "pkang My kang pack"
).add_info(
  "Everything about Sticker."
).add_warning(
  "✅ Harmless Module."
).add()
