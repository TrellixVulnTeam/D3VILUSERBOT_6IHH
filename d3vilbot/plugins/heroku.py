import asyncio
import math
import os
import heroku3
import requests
import urllib3
import sys

from os import execl
from time import sleep
from asyncio.exceptions import CancelledError

from ..sql.gvar_sql import addgvar, delgvar, gvarstat
from . import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY


async def restart(event):
    if HEROKU_APP_NAME and HEROKU_API_KEY:
        try:
            Heroku
        except BaseException:
            return await eor(event, "`HEROKU_API_KEY` is wrong. Re-Check in config vars.")
        await eor(event, f"✅ **Restarted Dynos** \n**Type** `{hl}ping` **after 1 minute to check if I am working !**")
        app = Heroku.apps()[HEROKU_APP_NAME]
        app.restart()
    else:
        await eor(event, f"✅ **Restarted ᗪ3ᏉᎥᏝᏰᎧᏖ** \n**Type** `{hl}ping` **after 1 minute to check if I am working !**")
        await event.client.disconnect()


@d3vil_cmd(pattern="restart$")
async def re(d3vil):
    event = await eor(d3vil, "Restarting ᗪ3ᏉᎥᏝᏰᎧᏖ ...")
    try:
        await restart(event)
    except CancelledError:
        pass
    except Exception as e:
        LOGS.info(e)


@d3vil_cmd(pattern="reload$")
async def rel(event):
    await eor(event, "Reloading ᗪ3ᏉᎥᏝᏰᎧᏖ... Wait for few seconds...")
    await reload_d3vilbot()


@d3vil_cmd(pattern="shutdown$")
async def down(d3vil):
    event = await eor(d3vil, "`Turing Off ᗪ3ᏉᎥᏝᏰᎧᏖ...`")
    await asyncio.sleep(2)
    await event.edit("**[ ⚠️ ]** \n**ᗪ3ᏉᎥᏝᏰᎧᏖ is now turned off. Manually turn it on to start again.**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@d3vil_cmd(pattern="svar(?:\s|$)([\s\S]*)")
async def sett(event):
    d3vilbot_ = event.pattern_match.group(1)
    var_ = d3vilbot_.split(" ")[0].upper()
    val_ = d3vilbot_.split(" ")[1:]
    valu = " ".join(val_)
    d3vil = await eor(event, f"**Setting variable** `{var_}` **as** `{valu}`")
    if var_ == "":
        return await eod(d3vil, f"**Invalid Syntax !!** \n\nTry: `{hl}svar VARIABLE_NAME variable_value`")
    elif valu == "":
        return await eod(d3vil, f"**Invalid Syntax !!** \n\nTry: `{hl}svar VARIABLE_NAME variable_value`")
    if var_ not in db_config:
        return await eod(d3vil, f"__There isn't any DB variable named__ `{var_}`. __Check spelling or get full list by__ `{hl}vars`")
    try:
        addgvar(var_, valu)
    except Exception as e:
        return await eod(d3vil, f"**ERROR !!** \n\n`{e}`")
    await eod(d3vil, f"**Variable Added Successfully!!** \n\n**• Variable:** `{var_}` \n**» Value:** `{valu}`")


@d3vil_cmd(pattern="gvar(?:\s|$)([\s\S]*)")
async def gett(event):
    var_ = event.pattern_match.group(1).upper()
    d3vil = await eor(event, f"**Getting variable** `{var_}`")
    if var_ == "":
        return await eod(d3vil, f"**Invalid Syntax !!** \n\nTry: `{hl}gvar VARIABLE_NAME`")
    if var_ not in db_config:
        return await eod(d3vil, f"__There isn't any variable named__ `{var_}`. __Check spelling or get full list by `{hl}vars`")
    try:
        sql_v = gvarstat(var_)
        os_v = os.environ.get(var_) or "None"
    except Exception as e:
        return await eod(d3vil, f"**ERROR !!** \n\n`{e}`")
    await d3vil.edit(f"**• OS VARIABLE:** `{var_}`\n**» OS VALUE :** `{os_v}`\n------------------\n**• DB VARIABLE:** `{var_}`\n**» DB VALUE :** `{sql_v}`\n")


@d3vil_cmd(pattern="dvar(?:\s|$)([\s\S]*)")
async def dell(event):
    var_ = event.pattern_match.group(1).upper()
    d3vil = await eor(event, f"**Deleting Variable** `{var_}`")
    if var_ == "":
        return await eod(d3vil, f"**Invalid Syntax !!** \n\nTry: `{hl}dvar VARIABLE_NAME`")
    if var_ not in db_config:
        return await eod(d3vil, f"__There isn't any variable named__ `{var_}`. Check spelling or get full list by `{hl}vars`")
    if gvarstat(var_):
        try:
            x = gvarstat(var_)
            delgvar(var_)
            await eod(d3vil, f"**Deleted Variable Successfully!!** \n\n**• Variable:** `{var_}` \n**» Value:** `{x}`")
        except Exception as e:
            await eod(d3vil, f"**ERROR !!** \n\n`{e}`")
    else:
        await eod(d3vil, f"**No variable named** `{var_}`")
   

@d3vil_cmd(pattern="(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)")
async def variable(d3vil):
    lg_id = Config.LOGGER_ID
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await eor(d3vil, "**[ HEROKU ]:**\n__Please setup your__ `HEROKU_APP_NAME`")
    exe = d3vil.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        event = await eor(d3vil, "Getting Variable Info...")
        cap = "Logger me chala jaa bsdk."
        capn = "Saved in LOGGER_ID !!"
        try:
            xvar = d3vil.pattern_match.group(2).split()[0]
            variable = xvar.upper()
            if variable in db_config:
                return await eod(event, f"This is a SQL based variable. Do `{hl}gvar {variable}` to get variable info.")
            if variable in ("D3VILBOT_SESSION", "BOT_TOKEN", "HEROKU_API_KEY"):
                if Config.ABUSE == "ON":
                    await event.client.send_file(d3vil.chat_id, cjb, caption=cap)
                    await event.delete()
                    await event.client.send_message(lg_id, f"#HEROKU_VAR \n\n`{heroku_var[variable]}`")
                    return
                else:
                    await event.edit(f"**{capn}**")
                    await event.client.send_message(lg_id, f"#HEROKU_VAR \n\n`{heroku_var[variable]}`")
                    return
            if variable in heroku_var:
                return await event.edit(f"**Heroku Var:** \n\n`{variable}` = `{heroku_var[variable]}`\n")
            else:
                return await eod(event, "**Heroku Var:** \n\n__Error:__\n-> I doubt `{variable}` exists!")
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await d3vil.client.send_file(
                        d3vil.chat_id,
                        "configs.json",
                        reply_to=d3vil.id,
                        caption="`Output too large, sending it as a file`",
                    )
                    await event.delete()
                else:
                    await event.edit(
                        "**Heroku Var :**\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================"
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        event = await eor(d3vil, "Setting Heroku Variable...")
        xvar = d3vil.pattern_match.group(2)
        if not xvar:
            return await eod(event, f"`{hl}set var <Var Name> <Value>`")
        variable = xvar.upper()
        value = d3vil.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = d3vil.pattern_match.group(2).split()[1]
            except IndexError:
                return await eod(event, f"`{hl}set var <Var Name> <Value>`")
        if variable in db_config:
            return await eod(event, f"This is a SQL based variable. Do `{hl}svar {variable} {value}` to set this.")
        if variable in heroku_var:
            await event.edit(f"`{variable}` **successfully changed to**  ->  `{value}`")
        else:
            await event.edit(f"`{variable}` **successfully added with value**  ->  `{value}`")
        heroku_var[variable] = value
    elif exe == "del":
        event = await eor(d3vil, "Getting info to delete Variable")
        try:
            xvar = d3vil.pattern_match.group(2).split()[0]
        except IndexError:
            return await eod(event, "`Please specify ConfigVars you want to delete`")
        variable = xvar.upper()
        if variable in db_config:
            return await eod(event, f"This is a SQL based variable. Do `{hl}dvar {variable}` to delete it.")
        if variable in heroku_var:
            await event.edit(f"**Successfully Deleted** \n`{variable}`")
            del heroku_var[variable]
        else:
            return await eod(event, f"`{variable}`  **does not exists**")


@d3vil_cmd(pattern="usage$")
async def dyno_usage(d3vil):
    event = await eor(d3vil, "`Processing...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await eod(event, "`Error: something bad happened`\n\n" f">.`{r.reason}`\n")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    cid = await client_id(event)
    d3vil_mention = cid[2]

    return await event.edit(
        "⚡ **Dyno Usage** ⚡:\n\n"
        f" ➠ __Dyno usage for__ • **{Config.HEROKU_APP_NAME}** • :\n"
        f"     ★  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  `{AppPercentage}`**%**"
        "\n\n"
        " ➠ __Dyno hours remaining this month__ :\n"
        f"     ★  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  `{percentage}`**%**"
        f"\n\n**Owner :** {d3vil_mention}"
    )


@d3vil_cmd(pattern="logs$")
async def _(event):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        return await eor(event, f"Make Sure Your HEROKU_APP_NAME & HEROKU_API_KEY are filled correct. Visit {d3vil_grp} for help.", link_preview=False)
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await event.reply(f"Make Sure Your Heroku AppName & API Key are filled correct. Visit {d3vil_grp} for help.", link_preview=False)
    cid = await client_id(event)
    d3vil_mention = cid[2]
    d3vil_data = app.get_log()
    await eor(event, d3vil_data, deflink=True, linktext=f"**🗒️ Heroku Logs of 💯 lines. 🗒️**\n\n🌟 **Bot Of :**  {d3vil_mention}\n\n🚀** Pasted**  ")


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""
    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


CmdHelp("power").add_command(
  "restart", None, "Restarts your userbot. Redtarting Bot may result in better functioning of bot when its laggy"
).add_command(
  "reload", None, "Reloads the bot DB and SQL variables without deleting any external plugins if installed."
).add_command(
  "shutdown", None, "Turns off ᗪ3ᏉᎥᏝᏰᎧᏖ. Userbot will stop working unless you manually turn it on."
).add_command(
  "svar", "<variable name> <variable value>", "Sets the variable to SQL variables without restarting the bot.", "svar ALIVE_PIC https://telegra.ph/file/2df70247b6a521437ff55.mp4"
).add_command(
  "gvar", "<variable name>", "Gets the info of mentioned variable from both SQL & OS.", "gvar ALIVE_PIC"
).add_command(
  "dvar", "<variable name>", "Deletes the mentioned variable from SQL variables without restarting the bot.", "dvar ALIVE_PIC"
).add_info(
  "Power Switch For Bot"
).add_warning(
  "✅ Harmless Module"
).add()

CmdHelp("heroku").add_command(
  "usage", None, "Check your heroku dyno hours status."
).add_command(
  "set var", "<Var Name> <value>", "Add new variable or update existing value/variable\nAfter setting a variable bot will restart so stay calm for 1 minute."
).add_command(
  "get var", "<Var Name>", "Gets the variable and its value (if any) from heroku."
).add_command(
  "del var", "<Var Name>", "Deletes the variable from heroku. Bot will restart after deleting the variable. So be calm for a minute 😃"
).add_command(
  "logs", None, "Gets the app log of 100 lines of your bot directly from heroku."
).add_info(
  "Heroku Stuffs"
).add_warning(
  "✅ Harmless Module"
).add()
