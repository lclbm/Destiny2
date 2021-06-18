from nonebot import on_command, CommandSession
import asyncio
from .user import abc


@on_command('吉林大学疫情打卡', only_to_me=False)
async def jldx(session: CommandSession):
    try:
        ev = session.event
        if ev.user_id not in [1227550214, 1123055129, 614867321]:
            return None
        msg = abc()
        await session.send(f'{msg}', at_sender=True)

    except Exception as e:
        await session.send(f'{e}', at_sender=True)
