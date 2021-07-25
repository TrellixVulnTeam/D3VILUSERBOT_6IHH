import time

from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User

from . import *


@bot.on(d3vil_cmd(pattern="stats$"))
@bot.on(sudo_cmd(pattern="stats$", allow_sudo=True))
async def stats(
    event: NewMessage.Event,
) -> None:  # pylint: disable = R0912, R0914, R0915
    if event.fwd_from:
        return
    d3vil = await edit_or_reply(event, "`Collecting stats...`")
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel):
            # participants_count = (await event.get_participants(dialog,
            # limit=0)).total
            if entity.broadcast:
                broadcast_channels += 1
                if entity.creator or entity.admin_rights:
                    admin_in_broadcast_channels += 1
                if entity.creator:
                    creator_in_channels += 1
            elif entity.megagroup:
                groups += 1
                # if participants_count > largest_group_member_count:
                #     largest_group_member_count = participants_count
                if entity.creator or entity.admin_rights:
                    # if participants_count > largest_group_with_admin:
                    #     largest_group_with_admin = participants_count
                    admin_in_groups += 1
                if entity.creator:
                    creator_in_groups += 1
        elif isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        elif isinstance(entity, Chat):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"🔰**𝖲𝗍𝖺𝗍𝗌 𝖿𝗈𝗋 {full_name}**🔰\n\n"
    response += f"🔱 **𝖯𝗋𝗂𝗏𝖺𝗍𝖾 𝖢𝗁𝖺𝗍𝗌:** {private_chats} \n"
    response += f"🔸   `𝖴𝗌𝖾𝗋𝗌: {private_chats - bots}` \n"
    response += f"🔹   `𝖡𝗈𝗍𝗌: {bots}` \n"
    response += f"🔱 **𝖦𝗋𝗈𝗎𝗉𝗌:** {groups} \n"
    response += f"🔱 **𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌:** {broadcast_channels} \n"
    response += f"☣️  **𝖠𝖽𝗆𝗂𝗇 in Groups:** {admin_in_groups} \n"
    response += f"🔹   `𝖢𝗋𝖾𝖺𝗍𝗈𝗋: {creator_in_groups}` \n"
    response += f"🔸   `𝖠𝖽𝗆𝗂𝗇 𝖱𝗂𝗀𝗁𝗍𝗌: {admin_in_groups - creator_in_groups}` \n"
    response += f"☣️  **𝖠𝖽𝗆𝗂𝗇 𝗂𝗇 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌:** {admin_in_broadcast_channels} \n"
    response += f"🔸   `𝖢𝗋𝖾𝖺𝗍𝗈𝗋: {creator_in_channels}` \n"
    response += (
        f"🔹   `Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    )
    response += f"🔱 **𝖴𝗇𝗋𝖾𝖺𝖽:** {unread} \n"
    response += f"🔱 **𝖴𝗇𝗋𝖾𝖺𝖽 𝖬𝖾𝗇𝗍𝗂𝗈𝗇𝗌:** {unread_mentions} \n\n"
    response += f"☣️   __𝖨𝗍 𝖳𝗈𝗈𝗄:__ {stop_time:.02f}s \n"
    response += (
        f"📌 **𝖥𝗋𝗈𝗆 𝖳𝗁𝖾 𝖣𝖺𝗍𝖺𝖡𝖺𝗌𝖾 𝖮𝖿** :- {d3vil_channel}"
    )
    await d3vil.edit(response)


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "D3vil"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


CmdHelp("stats").add_command(
  'stats', None, 'Shows you the count of your groups, channels, private chats, etc.'
).add()
