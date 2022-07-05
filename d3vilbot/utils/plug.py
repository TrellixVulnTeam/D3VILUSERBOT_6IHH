import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, InputMessagesFilterDocument

from d3vilbot import *
from d3vilbot.clients import *
from d3vilbot.helpers import *
from d3vilbot.config import *
from d3vilbot.utils import *


# ENV
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from d3vilbot.config import Config
else:
    if os.path.exists("Config.py"):
        from Config import Development as Config


# load plugins
def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import d3vilbot.utils

        path = Path(f"d3vilbot/plugins/{shortname}.py")
        name = "d3vilbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("ᗪ3ʋɨʟɮօȶ - Successfully imported " + shortname)
    else:
        import d3vilbot.utils

        path = Path(f"d3vilbot/plugins/{shortname}.py")
        name = "d3vilbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = d3vil
        mod.D1 = d3vil
        mod.D2 = D2
        mod.D3 = D3
        mod.D4 = D4
        mod.D5 = D5
        mod.d3vil = d3vil
        mod.d3vilbot = d3vilbot
        mod.tbot = d3vilbot
        mod.tgbot = bot.tgbot
        mod.command = command
        mod.CmdHelp = CmdHelp
        mod.client_id = client_id
        mod.logger = logging.getLogger(shortname)
        # support for uniborg
        sys.modules["uniborg.util"] = d3vilbot.utils
        mod.Config = Config
        mod.borg = bot
        mod.d3vilbot = bot
        mod.edit_or_reply = edit_or_reply
        mod.eor = edit_or_reply
        mod.delete_d3vil = delete_d3vil
        mod.eod = delete_d3vil
        mod.Var = Config
        mod.admin_cmd = admin_cmd
        mod.d3vil_cmd = d3vil_cmd
        mod.sudo_cmd = sudo_cmd
        # support for other userbots
        sys.modules["userbot.utils"] = d3vilbot.utils
        sys.modules["userbot"] = d3vilbot
        # support for paperplaneextended
        sys.modules["userbot.events"] = d3vilbot
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["d3vilbot.plugins." + shortname] = mod
        LOGS.info("⚡ ᗪ3ʋɨʟɮօȶ ⚡ - Successfully Imported " + shortname)


# remove plugins
def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                bot.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except BaseException:
            name = f"d3vilbot.plugins.{shortname}"

            for i in reversed(range(len(bot._event_builders))):
                ev, cb = bot._event_builders[i]
                if cb.__module__ == name:
                    del bot._event_builders[i]
    except BaseException:
        raise ValueError


async def plug_channel(client, channel):
    if channel:
        LOGS.info("⚡ D3VILBOT ⚡ - PLUGIN CHANNEL DETECTED.")
        LOGS.info("⚡ D3VILBOT ⚡ - Starting to load extra plugins.")
        plugs = await client.get_messages(channel, None, filter=InputMessagesFilterDocument)
        total = int(plugs.total)
        for plugins in range(total):
            plug_id = plugs[plugins].id
            plug_name = plugs[plugins].file.name
            if os.path.exists(f"d3vilbot/plugins/{plug_name}"):
                return
            downloaded_file_name = await client.download_media(
                await client.get_messages(channel, ids=plug_id),
                "d3vilbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            try:
                load_module(shortname.replace(".py", ""))
            except Exception as e:
                LOGS.error(str(e))


# d3vilbot
