from telethon.utils import get_peer_id
from telethon.tl.functions.users import GetFullUserRequest

from .session import D3vil, D2, D3, D4, D5
from d3vilbot.sql.gvar_sql import gvarstat


async def clients_list():
    user_ids = []
    if gvarstat("SUDO_USERS"):
        a = gvarstat("SUDO_USERS").split(" ")
        for b in a:
            c = int(b)
            user_ids.append(c)
    main_id = await D3vil.get_me()
    user_ids.append(main_id.id)

    try:
        if D2 is not None:
            id2 = await D2.get_me()
            user_ids.append(id2.id)
    except:
        pass

    try:
        if D3 is not None:
            id3 = await D3.get_me()
            user_ids.append(id3.id)
    except:
        pass

    try:
        if D4 is not None:
            id4 = await D4.get_me()
            user_ids.append(id4.id)
    except:
        pass

    try:
        if D5 is not None:
            id5 = await D5.get_me()
            user_ids.append(id5.id)
    except:
        pass

    return user_ids


async def client_id(event, botid=None):
    if botid is not None:
        uid = await event.client(GetFullUserRequest(botid))
        d3vilkrish  = uid.user.id
        D3vil_USER = uid.user.first_name
        d3vil_mention = f"[{D3vil_USER}](tg://user?id={d3vilkrish })"
    else:
        client = await event.client.get_me()
        uid = get_peer_id(client)
        D3VIL_USER = uid.user.first_name
        d3krish = uid.user.id
        d3vil_mention = f"[{D3VIL_USER}](tg://user?id={d3krish})"
            return d3vilkrish , D3VIL_USER, d3vil_mention
