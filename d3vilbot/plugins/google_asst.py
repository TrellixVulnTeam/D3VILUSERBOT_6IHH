import asyncio
import datetime
import emoji
import os
import subprocess

from googletrans import Translator
from gtts import gTTS

from . import *


@d3vil_cmd(pattern="trt(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[5:]
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif "-" in input_str:
        lan, text = input_str.split("-")
    else:
        await eod(event, f"`{hl}trt LanguageCode - message`  or  `{hl}trt LanguageCode as reply to a message.`\n\nTry `{hl}trc` to get all language codes")
        return
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = "**Translated From** __{}__ **to** __{}__\n\n`{}`".format(translated.src, lan, after_tr_text)
        await eor(event, output_str)
    except Exception as exc:
        await eor(event, str(exc))

@d3vil_cmd(pattern="trc$")
async def _(d3vil):
    await eor(d3vil, "**All The Language Codes Can Be Found** ⚡ [Here](https://telegra.ph/3-𝗗3𝗩𝗜𝗟𖤍𓆩𝙠𝙧𝙞𝙨𝙝𓆪---Ɇ-D3VIL-07-07) ⚡", link_preview=False)


@d3vil_cmd(pattern="voice(?:\s|$)([\s\S]*)")
async def _(event):
    d3vil = await eor(event, "Preparing Voice....")
    input_str = event.pattern_match.group(1)
    start = datetime.datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "-" in input_str:
        lan, text = input_str.split("-")
    else:
        await eod(d3vil, f"Invalid Syntax. Module stopping. Check out `{hl}plinfo google_asst` for help.")
        return
    text = text.strip()
    lan = lan.strip()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + "voice.ogg"
    try:
        tts = gTTS(text, lang=lan)
        tts.save(required_file_name)
        command_to_execute = [
            "ffmpeg",
            "-i",
            required_file_name,
            "-map",
            "0:a",
            "-codec:a",
            "libopus",
            "-b:a",
            "100k",
            "-vbr",
            "on",
            required_file_name + ".opus",
        ]
        try:
            t_response = subprocess.check_output(
                command_to_execute, stderr=subprocess.STDOUT
            )
        except (subprocess.CalledProcessError, NameError, FileNotFoundError) as exc:
            await d3vil.edit(str(exc))
        else:
            os.remove(required_file_name)
            required_file_name = required_file_name + ".opus"
        end = datetime.datetime.now()
        ms = (end - start).seconds
        await event.client.send_file(
            event.chat_id,
            required_file_name,
            caption=f"**• Voiced :** `{text[0:97]}....` \n**• Language :** `{lan}` \n**• Time Taken :** `{ms} seconds`",
            reply_to=event.message.reply_to_msg_id,
            allow_cache=False,
            voice_note=True,
        )
        os.remove(required_file_name)
        await d3vil.delete()
    except Exception as e:
        await eod(d3vil, str(e))


CmdHelp("google_asst").add_command(
  "voice", "<reply to a msg> <lang code>", "Sends the replied msg content in audio format."
).add_command(
    "trt", "<lang code> <reply to msg>", "Translates the replied message to desired language code. Type '.trc' to get all the language codes", f"trt en - hello | {hl}trt en <reply to msg>"
).add_command(
  "trc", None, "Gets all the possible language codes for google translate module"
).add_info(
  "Google Assistant"
).add_warning(
  "✅ Harmless Module."
).add()
