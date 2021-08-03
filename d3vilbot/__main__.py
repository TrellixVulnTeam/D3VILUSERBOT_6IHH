import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest

from d3vilbot import LOGS, bot, tbot
from d3vilbot.config import Config
from d3vilbot.utils import load_module
from d3vilbot.version import __d3vil__ as d3vilver
hl = Config.HANDLER
D3VIL_PIC = Config.ALIVE_PIC or "https://telegra.ph/file/5abfcff75e1930dcdfaf3.mp4"

# let's get the bot ready
async def d3vil_bot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"D3VILBOT_SESSION - {str(e)}")
        sys.exit()


# Userbot starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = TelegramClient(
                "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
            ).start(bot_token=Config.BOT_TOKEN)
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("⚡ 𝐒𝐓𝐀𝐑𝐓𝐈𝐍𝐆 𝐃3𝐕𝐈𝐋𝐁𝐎𝐓⚡")
            bot.loop.run_until_complete(d3vil_bot(Config.BOT_USERNAME))
            LOGS.info("⚔️ 𝐃3𝐕𝐈𝐋𝐁𝐎𝐓 𝐒𝐭𝐚𝐫𝐭𝐮𝐩 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝 ⚔️")
        else:
            bot.start()
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()

# imports plugins...
path = "d3vilbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

# Extra Modules...
# extra_repo = Config.EXTRA_REPO or "https://github.com/"
# if Config.EXTRA == "True":
#     try:
#         os.system(f"git clone {extra_repo}")
#     except BaseException:
#         pass
#     LOGS.info("Installing Extra Plugins")
#     path = "hellbot/plugins/*.py"
#     files = glob.glob(path)
#     for name in files:
#         with open(name) as ex:
#             path2 = Path(ex.name)
#             shortname = path2.stem
#             load_module(shortname.replace(".py", ""))

# let the party begin...
LOGS.info("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐁𝐨𝐭 𝐌𝐨𝐝𝐞 !")
tbot.start()
LOGS.info("⚡ 𝐘𝐨𝐮𝐫 𝐃3𝐯𝐢𝐥𝐁𝐨𝐭 𝐈𝐬 𝐍𝐨𝐰 𝐖𝐨𝐫𝐤𝐢𝐧𝐠 ⚡")
LOGS.info(
    "𝐇𝐞𝐚𝐝 𝐭𝐨 @D3VIL_SUPPORT 𝐟𝐨𝐫 𝐮𝐩𝐝𝐚𝐭𝐞𝐬. 𝐀𝐥𝐬𝐨 𝐣𝐨𝐢𝐧 𝐜𝐡𝐚𝐭 𝐠𝐫𝐨𝐮𝐩 to 𝐠𝐞𝐭 𝐁𝐎𝐓 𝐫𝐞𝐠𝐚𝐫𝐝𝐢𝐧𝐠 𝐭𝐨 𝐃3𝐕𝐈𝐋𝐁𝐎𝐓."
)

# that's life...
async def d3vil_is_on():
    try:
        if Config.LOGGER_ID != 0:
            await bot.send_file(
                Config.LOGGER_ID,
                D3VIL_PIC,
                caption=f"𝐃𝐞𝐩𝐥𝐨𝐲𝐞𝐝 𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲\n\n**𝔡3𝔳𝔦𝔩𝔟𝔬𝔱 - {d3vilver}**\n\n𝐓𝐲𝐩𝐞 `{hl}ping` or `{hl}alive` 𝐭𝐨 𝐜𝐡𝐞𝐜𝐤! \n\nJoin [𝔡3𝔳𝔦𝔩𝔲𝔰𝔢𝔯𝔅𝔬𝔱](t.me/D3VIL_SUPPORT) for Updates & [𝔇3𝔳𝔦𝔩𝔲𝔰𝔢𝔯𝔅𝔬𝔱 𝔠𝔥𝔞𝔱](t.me/D3VIL_BOT_SUPPORT) 𝐟𝐨𝐫 𝐚𝐧𝐲 𝐪𝐮𝐞𝐫𝐲 𝐫𝐞𝐠𝐚𝐫𝐝𝐢𝐧𝐠 𝔡3𝔳𝔦𝔩𝔅𝔬𝔱",
            )
    except Exception as e:
        LOGS.info(str(e))


    try:
        await bot(JoinChannelRequest("@D3VIL_SUPORT"))
    except BaseException:
        pass


bot.loop.create_task(d3vil_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()


