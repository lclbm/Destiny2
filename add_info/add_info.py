import sys
import os
print(os.getcwd())
sys.path.append(os.getcwd())
sys.path.append('C:/HoshinoBot/hoshino/modules/add_info')
from a import add_josn,get_msg,lookup,del_tie_user
from nonebot import *
import asyncio
from hoshino import Service, R
import hoshino
import re



sv = hoshino.Service('add')
_bot = get_bot()


@sv.on_command('绑定帮助')
async def Help(session):
    msg = '''❗现在需要加入【 】作为标识符
❗绑定/添加后面需要有一个空格
🚀绑定自己的队伍码
指令：绑定 【7656xxx16】
例子：绑定 【7656119xx】
🚀绑定朋友的队伍码
指令：绑定 【昵称】【7656xxx16】
例子：绑定 【菠萝】【7656xxx16】
🎐自定义问答
指令：添加 【问题】【回答】
例子：添加 【快进哥】【块茎哥】
🎐绑定查询
指令1：绑定查询
指令2：绑定查询 All
🎐绑定删除
指令：绑定删除 【文本】
例子：绑定删除 【快进哥】'''
    await session.send(msg)



@sv.on_message('group')
async def check(*params):
    bot, ctx = (_bot, params[0]) if len(params) == 1 else params
    msg = get_msg(ctx)
    if msg:
        await bot.send(ctx,msg)



@sv.on_command('AddAll')
async def add_info_all(session):
    try:
        if not add_josn(session.ctx, 0):
            await session.send('你是不是管理员先就在这里AddAll',at_sender=True)
        else:
            await session.send('成功',at_sender=True)
    except Exception as e:
        await session.send(f'{e}')

@sv.on_command('添加')
async def add_info_user(session):
    try:
        if not add_josn(session.ctx, 2):
            await session.send('添加失败，输入绑定帮助以查看帮助',at_sender=True)
        else:
            await session.send('成功',at_sender=True)
    except Exception as e:
        await session.send(f'{e}')

@sv.on_command('绑定')
async def add_tie(session):
    try:
        if not add_josn(session.ctx, 1):
            res = re.match(r'(7656\d{13}$)', session.current_arg_text.strip())
            if res:
                id = res.group(1)
                await session.send('绑定失败，小日向发现你没有添加【】符号，小日向给你提供了正确的绑定指令，复制粘贴试试哦', at_sender=True)
                await session.send(f'绑定 【{id}】')
            else:
                await session.send('绑定失败，绑定帮助有新的更新了，绑定失败不妨来试试看哦，输入绑定帮助即可',at_sender=True)
        else:
            await session.send('绑定成功',at_sender=True)
    except Exception as e:
        await session.send(f'{e}')

@sv.on_command('绑定查询')
async def look_tie(session):
    try:
        msg = lookup(session.ctx)
        await session.send(msg)
    except Exception as e:
        await session.send(f'{e}')

@sv.on_command('绑定删除')
async def delete_tie(session):
    try:
        msg = del_tie_user(session.ctx)
        await session.send(msg)
    except Exception as e:
        await session.send(f'{e}')