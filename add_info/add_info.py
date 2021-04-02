
import re
import hoshino
from hoshino import Service, R
import asyncio
from nonebot import *
import sys
import os
print(os.getcwd())
sys.path.append(os.getcwd())
sys.path.append('C:/HoshinoBot/hoshino/modules/add_info')
from a import *


sv = hoshino.Service('add')
_bot = get_bot()


# @sv.on_command('绑定帮助')
# async def Help(session):
#     msg = '''待更新'''
#     await session.send(msg)


@sv.on_message('group')
async def check(*params):
    bot, ctx = (_bot, params[0]) if len(params) == 1 else params
    msg = get_msg(ctx)
    if msg:
        print(msg)
        await bot.send(ctx, msg)


@sv.on_command('添加全局')
async def add_info_all(session):
    try:
        msg = add_all(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('添加个人')
async def add_info_user(session):
    try:
        msg = add_reply(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('添加群组')
async def add_info_group(session):
    try:
        msg = add_reply(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('个人词库')
async def look_user(session):
    try:
        msg = lookup_user(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('群组词库')
async def look_group(session):
    try:
        msg = lookup_group(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('全局词库')
async def look_all(session):
    try:
        msg = lookup_all(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('删除个人')
async def delete_tie_user(session):
    try:
        msg = del_reply(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('删除群组')
async def delete_tie_group(session):
    try:
        msg = del_reply(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('删除全局')
async def delete_tie_all(session):
    try:
        msg = del_all(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('绑定全局')
async def tieall(session):
    try:
        msg = tie_all(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('绑定群组')
async def tiegroup(session):
    try:
        msg = tie_group(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('绑定个人')
async def tieuser(session):
    try:
        msg = tie_user(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@sv.on_command('绑定')
async def tieurself(session):
    try:
        msg = tie_urself(session.ctx)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)
