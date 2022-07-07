import asyncio
import os
import cv2
import io
import lottie
import random
import re
import shutil
import textwrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

from . import *


path = "./d3vilmify/"
if not os.path.isdir(path):
    os.makedirs(path)


@d3vil_cmd(pattern="mmf(?:\s|$)([\s\S]*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    d3vilbot_ = await eor(event, "**Memifying 🌚🌝**")
    d3vil = await _reply.download_media()
    if d3vil and d3vil.endswith((".tgs")):
        await d3vilbot_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", d3vil, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif d3vil and d3vil.endswith((".webp", ".png")):
        pics = Image.open(d3vil)
        pics.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    elif d3vil:
        img = cv2.VideoCapture(d3vil)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    else:
        return await eod(d3vilbot_, "Unable to memify this!")
    output = await draw_meme_text(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await d3vilbot_.delete()
    try:
        os.remove(d3vil)
        os.remove(file)
        os.remove(output)
    except BaseException:
        pass


@d3vil_cmd(pattern="mms(?:\s|$)([\s\S]*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    d3vilbot_ = await eor(event, "**Memifying 🌚🌝**")
    d3vil = await _reply.download_media()
    if d3vil and d3vil.endswith((".tgs")):
        await d3vilbot_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", d3vil, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif d3vil and d3vil.endswith((".webp", ".png")):
        pic = Image.open(d3vil)
        pic.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    elif d3vil:
        img = cv2.VideoCapture(d3vil)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    else:
        return await eod(d3vilbot_, "Unable to memify this!")
    output = await draw_meme(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await d3vilbot_.delete()
    try:
        os.remove(d3vil)
        os.remove(file)
    except BaseException:
        pass
    os.remove(pic)


@d3vil_cmd(pattern="doge(?:\s|$)([\s\S]*)")
async def nope(event):
    d3vil = event.text[6:]
    if not d3vil:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Doge need some text to make sticker.")

    troll = await event.client.inline_query("DogeStickerBot", f"{(deEmojify(d3vil))}")
    if troll:
        await event.delete()
        d3vilbot_ = await troll[0].click(Config.LOGGER_ID)
        if d3vilbot_:
            await event.client.send_file(
                event.chat_id,
                d3vilbot_,
                caption="",
            )
        await d3vilbot_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


@d3vil_cmd(pattern="gg(?:\s|$)([\s\S]*)")
async def nope(event):
    d3vil = event.text[4:]
    if not d3vil:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Googlax need some text to make sticker.")

    troll = await event.client.inline_query("GooglaxBot", f"{(deEmojify(d3vil))}")
    if troll:
        await event.delete()
        d3vilbot_ = await troll[0].click(Config.LOGGER_ID)
        if d3vilbot_:
            await event.client.send_file(
                event.chat_id,
                d3vilbot_,
                caption="",
            )
        await d3vilbot_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


@d3vil_cmd(pattern="honk(?:\s|$)([\s\S]*)")
async def nope(event):
    d3vil = event.text[6:]
    if not d3vil:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Honka need some text to make sticker.")

    troll = await event.client.inline_query("honka_says_bot", f"{(deEmojify(d3vil))}.")
    if troll:
        await event.delete()
        d3vilbot_ = await troll[0].click(Config.LOGGER_ID)
        if d3vilbot_:
            await event.client.send_file(
                event.chat_id,
                d3vilbot_,
                caption="",
            )
        await d3vilbot_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


@d3vil_cmd(pattern="gogl(?:\s|$)([\s\S]*)")
async def nope(event):
    d3vil = event.text[6:]
    if not d3vil:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Need some text...")

    troll = await event.client.inline_query("stickerizerbot", f"#12{(deEmojify(d3vil))}")
    if troll:
        await event.delete()
        d3vilbot_ = await troll[0].click(Config.LOGGER_ID)
        if d3vilbot_:
            await event.client.send_file(
                event.chat_id,
                d3vilbot_,
                caption="",
            )
        await d3vilbot_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


Cmdd3vilbotp("memify").add_command(
  "mmf", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in sticker format.", "mmf <reply to a img/stcr/gif> hii ; Hello  "
).add_command(
  "mms", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in image format.", "mms <reply to a img/stcr/gif> hii ; Hello  "
).add_command(
  "doge", "<text>", "Makes A Sticker of Doge with given text.", "doge Hello  "
).add_command(
  "gogl", "<text>", "Makes google search sticker.", "gogl Hello "
).add_command(
  "gg", "<text>", "Makes google search sticker.", "gg Hello "
).add_command(
  "honk", "<text>", "Makes a sticker with honka revealing given text.", "honk Hello "
).add_info(
  "Make Memes on telegram 😉"
).add_warning(
  "✅ Harmless Module."
).add()
