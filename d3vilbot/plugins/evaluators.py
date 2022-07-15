import asyncio
import io
import time
import os
import sys
import traceback

from . import *
from ..sql.gvar_sql import gvarstat

lg_id = Config.LOGGER_ID

@bot.on(d3vil_cmd(pattern="exec(?: |$|\n)(.*)", command="exec"))
@bot.on(sudo_cmd(pattern="exec(?: |$|\n)(.*)", command="exec", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "".join(event.text.split(maxsplit=1)[1:])
    if not cmd:
        return await eod(event, "`What should i execute?..`")
    d3vilevent = await eor(event, "`Executing.....`")
    process = await asyncio.create_subprocess_sd3vil(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    d3viluser = await event.client.get_me()
    if d3viluser.username:
        curruser = d3viluser.username
    else:
        curruser = "d3vilbot"
    uid = os.geteuid()
    if uid == 0:
        cresult = f"`{curruser}:~#` `{cmd}`\n`{result}`"
    else:
        cresult = f"`{curruser}:~$` `{cmd}`\n`{result}`"
    await eor(event, "**Terminal Command Was Executed Successfully. Check LOGGER for Output.**")
    await event.client.send_message(
        lg_id,
        f"#EXEC \n\nTerminal command was executed sucessfully.\n\n**Command :**  `{cmd}`\n**Result :** \n{cresult}",
    )


@bot.on(d3vil_cmd(pattern="eval(?: |$|\n)(.*)", command="eval"))
@bot.on(sudo_cmd(pattern="eval(?: |$|\n)(.*)", command="eval", allow_sudo=True))
async def _(event):
#    if gvarstat("USE_EVAL") == "TRUE":
        cmd = "".join(event.text.split(maxsplit=1)[1:])
        if not cmd:
            return await eod(event, "`What should i run ?..`")
        d3vilevent = await eor(event, "`Running ...`")
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None
        try:
            await aexec(cmd, event)
        except Exception:
            exc = traceback.format_exc()
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"
        final_output = f"•  Eval : \n`{cmd}` \n\n•  Result : \n`{evaluation}` \n"
        final_output2 = f"**•  Eval :** \n`{cmd}` \n\n**•  Result :** \n`{evaluation}` \n"
        if len(final_output2) > 4092:
            await eor(d3vilevent, final_output, deflink=True, linktext=f"**•  Eval :** \n`{cmd}` \n\n**Pasted:** ")
        else:
            await eor(d3vilevent, final_output, deflink=True, linktext=f"{final_output2} \n\n**Also Pasted** ")
    else:
        await eod(event, f"**Eval Is Disbaled !!** \n\n__Do__ `{hl}svar USE_EVAL TRUE` __to enable eval commands.__")



@bot.on(d3vil_cmd(pattern="bash ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="bash ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_sd3vil(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"
    if len(OUTPUT) > 4095:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )
            await event.delete()
    await eor(event, "**Check out logger for result..**")
    await event.client.send_message(
        lg_id, 
        f"#BASH \n\n{output}"
    )
    

CmdHelp("evaluators").add_command(
  "eval", "<expr>", "Execute python script"
).add_command(
  "exec", "<command>", "Execute a Terminal command on D3vilBot server and shows details"
).add_command(
  "bash", "<query>", "Bash your codes on linux and gives the output in current chat"
).add()
