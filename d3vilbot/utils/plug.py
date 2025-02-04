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
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from d3vilbot import *
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
        LOGS.info("𝚃𝙴𝙰𝙼 𝙳3𝚅𝙸𝙻 - 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙸𝙼𝙿𝙾𝚁𝚃𝙴𝙳 " + shortname)
    else:
        import d3vilbot.utils

        path = Path(f"d3vilbot/plugins/{shortname}.py")
        name = "d3vilbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.tgbot = bot.tgbot
        mod.command = command
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
        mod.admin_cmd = d3vil_cmd
        mod.d3vil_cmd = d3vil_cmd
        # support for other userbots
        sys.modules["userbot.utils"] = d3vilbot.utils
        sys.modules["userbot"] = d3vilbot
        # support for paperplaneextended
        sys.modules["userbot.events"] = d3vilbot
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["d3vilbot.plugins." + shortname] = mod
        LOGS.info("✘ 𝚃𝙴𝙰𝙼 𝐃3𝚅𝙸𝙻 ✘  - 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙸𝙼𝙿𝙾𝚁𝚃𝙴𝙳 " + shortname)


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

#Addons...

def load_addons(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"D3VILADDONS/{shortname}.py")
        name = "D3VILADDONS.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("♦️Extra Plugin♦️ ~ " + shortname)
    else:
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"D3VILADDONS/{shortname}.py")
        name = "D3VILADDONS.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
#        mod.d3vil = d3vil
        mod.bot = bot
        mod.bot = bot
        mod.command = command
        mod.borg = bot
        mod.d3vilbot = bot
        mod.tgbot = bot.tgbot
        mod.Var = Config
        mod.Config = Config
        mod.edit_or_reply = edit_or_reply
        mod.delete_d3vil = delete_d3vil
        mod.eod = delete_d3vil
        mod.admin_cmd = d3vil_cmd
        mod.logger = logging.getLogger(shortname)
        # support for D3VILBOT originals
#        sys.modules["userbot.utils"] = d3vilbot.utils
#        sys.modules["userbot"] = d3vilbot
        # support for paperplaneextended
#        sys.modules["userbot.events"] = d3vilbot
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["D3VILADDONS." + shortname] = mod
        LOGS.info("🔱Extra Plugin🔱 ~ " + shortname)
#d3vilbot

# TGBot


def start_assistant(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Initialising TGBot.")
        print("TGBot - Imported " + shortname)
    else:
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = bot.tgbot
        spec.loader.exec_module(mod)
        sys.modules["d3vilbot.assistant" + shortname] = mod
        print("TGBot Has imported " + shortname)


def load_pmbot(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.pmbot.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Initialising PMBot.")
        print("PMBot - Imported " + shortname)
    else:
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.pmbot.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = bot.tgbot
        spec.loader.exec_module(mod)
        sys.modules["d3vilbot.assistant.pmbot." + shortname] = mod
        print("PMBot Has imported " + shortname)


