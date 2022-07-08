import glob
import os
import sys

from pathlib import Path
from telethon import Button, TelegramClient
from telethon.utils import get_peer_id

from d3vilbot import LOGS, bot, tbot
from d3vilbot.clients.session import D3vil, D2, D3, D4, D5
from d3vilbot.config import Config
from d3vilbot.utils import join_it, load_module, logger_check, start_msg, update_sudo, plug_channel
from d3vilbot.version import __d3vil__ as d3vilver
from d3vilbot import CMD_LIST
from __init__ import CMD_LIST
hl = Config.HANDLER

D3VIL_PIC = "https://telegra.ph/file/5abfcff75e1930dcdfaf3.mp4"


# Client Starter
async def d3vils(session=None, client=None, session_name="Main"):
    if session:
        LOGS.info(f"••• Starting Client [{session_name}] •••")
        try:
            await client.start()
            return 1
        except:
            LOGS.error(f"Error in {session_name}!! Check & try again!")
            return 0
    else:
        return 0


# Load plugins based on config UNLOAD
async def plug_load(path):
    files = glob.glob(path)
    for name in files:
        with open(name) as d3vil:
            path1 = Path(d3vil.name)
            shortname = path1.stem
            if shortname.replace(".py", "") in Config.UNLOAD:
                os.remove(Path(f"d3vilbot/plugins/{shortname}.py"))
            else:
                load_module(shortname.replace(".py", ""))      

# Assistant.....
assistant = os.environ.get("ASSISTANT", None)
async def assistants():
    if assistant == "ON":
        path = "d3vilbot/assistant/*.py"
        files = glob.glob(path)
        for name in files:
            with open(name) as f:
                path1 = Path(f.name)
                shortname = path1.stem
                start_assistant(shortname.replace(".py", ""))


bot.loop.run_until_complete(assistants())

# Final checks after startup
async def d3vil_is_on(total):
    await update_sudo()
    await logger_check(bot)
    await start_msg(tbot, D3VIL_PIC, d3vilver, total)
    await join_it(bot)
    await join_it(D2)
    await join_it(D3)
    await join_it(D4)
    await join_it(D5)


# d3vilbot starter...
async def start_d3vilbot():
    try:
        tbot_id = await tbot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"
        bot.tgbot = tbot
        LOGS.info("••• Starting d3vilBot •••")
        C1 = await d3vils(Config.d3vilBOT_SESSION, bot, "D3VILBOT_SESSION")
        C2 = await d3vils(Config.SESSION_2, D2, "SESSION_2")
        C3 = await d3vils(Config.SESSION_3, D3, "SESSION_3")
        C4 = await d3vils(Config.SESSION_4, D4, "SESSION_4")
        C5 = await d3vils(Config.SESSION_5, D5, "SESSION_5")
        await tbot.start()
        total = C1 + C2 + C3 + C4 + C5
        LOGS.info("••• d3vilBot Startup Completed •••")
        LOGS.info("••• Starting to load Plugins •••")
        await plug_load("d3vilbot/plugins/*.py")
        await plug_channel(bot, Config.PLUGIN_CHANNEL)
        LOGS.info("⚡ Your d3vilBot Is Now Working ⚡")
        LOGS.info("Head to @D3VIL_BOT_SUPPORT for Updates. Also join chat group to get help regarding to D3vilBot.")
        LOGS.info(f"» Total Clients = {str(total)} «")
        await d3vil_is_on(total)
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


bot.loop.run_until_complete(start_d3vilbot())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    try:
        bot.run_until_disconnected()
    except ConnectionError:
        pass


