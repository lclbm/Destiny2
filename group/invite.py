import nonebot
from nonebot import RequestSession, on_request, on_command, CommandSession, on_notice, NoticeSession, MessageSegment
from hoshino import Service, priv
import aiocqhttp
import re
from hoshino.service import sucmd
import hoshino
import asyncio

sv = Service('群组')

#
# @sv.on_message('group')
# async def handle_group_message(bot, event: aiocqhttp.Event):
#     print(event)
#     if event.raw_message == '测试测试':
#         await bot.send_group_msg(self_id=event.self_id, group_id=827529117, message=绑定帮助)


group_list = {}
group_add = {}

# @on_notice('group_decrease')
# async def group_member_decrease(session:NoticeSession):
#     ev=session.event
#     user_id = ev.user_id
#     try:
#         await session.send(f'（{user_id}）走了...')
#     except:
#         pass



@on_request('group.add')
async def handle_group_add(session: RequestSession):
    ev = session.event
    user_id = ev.user_id
    print('进入')
    try:
        user_info = await session.bot.get_stranger_info(user_id=user_id,self_id=ev.self_id)
        print('成功：',user_info)
        nickname = user_info['nickname']
    except Exception as e:
        nickname = f'{e}'
    at = MessageSegment.at(614867321)
    await session.send(f'{at}\n👉收到1条加群请求\nQQ：{user_id}\n昵称：{nickname}\n{ev.comment}')


@on_notice('group_increase')
async def group_member_add(session:NoticeSession):
    ev = session.event
    user_id = ev.user_id
    at=MessageSegment.at(user_id)
    try:
        if user_id == ev.self_id:
            await session.send(f'大家好，我是何志武223开发的小日向机器人，回复d2可以看看我有什么功能噢🤞')
        else:
            await session.send(f'{at}，欢迎噶点进群吼，我是群内的小日向机器人，回复d2可以看看我有什么功能噢🤞')
    except:
        pass


@on_request('group.invite')
async def handle_group_invite(session: RequestSession):
    ev = session.event
    try:
        try:
            group_info = await session.bot.get_group_info(group_id=ev.group_id,self_id=ev.self_id)
            group_name = group_info["group_name"]
        except Exception as err:
            group_name = f'[获取失败]'
        group_list[ev.group_id]={'flag': f'{ev.flag}',
                                'sub_type': f'{ev.sub_type}',
                                'group_name': f'{group_name}',
                                'user_id':f'{ev.user_id}'
                                }
        # comment = ev.comment
        length = len(group_list)
        # await session.bot.send_private_msg(self_id=ev.self_id, user_id=614867321,
        #                                    message=f'收到group_request\n{comment}\n剩余{length}条请求未处理')
        at = MessageSegment.at(614867321)
        at2 = MessageSegment.at(ev.user_id)
        # user_id = ev.user_id
        # user_info = await session.bot.get_stranger_info(user_id=user_id)
        # nickname = user_info['nickname']
        await session.bot.send_group_msg(self_id=ev.self_id, group_id=827529117,
                                        message=f'{at}\n👉收到1条群组请求\n群号：{ev.group_id}\n群名：{group_name}\n方式：{ev.sub_type}\n邀请人：{at2}\n目前剩余{length}条请求未处理')
    except Exception as e:
        await session.bot.send_group_msg(self_id=ev.self_id, group_id=827529117,
                                        message=f'{at}\n👉收到1条群组请求\n❗异常：{e}\n群号：{ev.group_id}\n')


@sucmd('quit', aliases=('退群',),force_private=False)
async def quit_group(session: CommandSession):
    args = session.current_arg_text.split()
    failed = []
    succ = []
    for arg in args:
        if not re.fullmatch(r'^\d+$', arg):
            failed.append(arg)
            continue
        try:
            await session.bot.set_group_leave(self_id=session.event.self_id, group_id=arg)
            succ.append(arg)
        except:
            failed.append(arg)
    msg = f'已尝试退出{len(succ)}个群'
    if failed:
        msg += f"\n失败{len(failed)}个群：{failed}"
    await session.send(msg,at_sender=True)


@sucmd('处理加群', force_private=False)
async def chuli(session: CommandSession):
    try:
        ev = session.event
        if ev.user_id != 614867321:
            raise Exception('只有管理员才有权限处理加群')
        if session.current_arg:
            res = re.match(r'(\d+) *([01]) *(.+)?', session.current_arg)
            group_id = int(res.group(1))
            approve = True if int(res.group(2)) == 1 else False
            flag = group_list[group_id]['flag']
            sub_type = group_list[group_id]['sub_type']
            group_name = group_list[group_id]['group_name']
            del group_list[group_id]
            comment = res.group(3)
            try:
                await session.bot.set_group_add_request(flag=flag, sub_type=sub_type, approve=approve,reason=comment)
                at2 = MessageSegment.at(group_list[group_id]['user_id'])
                if approve:
                    await session.send(f'{at2}已同意\n✅群号：{group_id}\n✅群名：{group_name}')
                else:
                    await session.send(f'{at2}已拒绝\n❌群号：{group_id}\n❌群名：{group_name}\n拒绝理由：{comment}')
            except Exception as e:
                await session.send(f'❗群号：{group_id}\n❗群名：{group_name}\n{e}')
        else:
            for key,value in group_list.items():
                await asyncio.sleep(1)
                flag = value['flag']
                sub_type = value['sub_type']
                group_name = value['group_name']
                at2 = MessageSegment.at(value['user_id'])
                try:
                    await session.bot.set_group_add_request(flag=flag, sub_type=sub_type,approve=True)
                    await session.send(f'{at2}已同意\n✅群号：{key}\n✅群名：{group_name}')
                except Exception as e:
                    await session.send(f'{at2}处理失败❗群号：{key}\n❗群名：{group_name}\n{e}')
            group_list.clear()
    except Exception as e:
        await session.send(f'{e}')


@sucmd('查询加群', force_private=False)
async def chaxun(session: CommandSession):
    try:
        print(group_list)
        ev = session.event
        num = 0
        msg = ''
        for key,value in group_list.items():
            group_name = value['group_name']
            sub_type = value['sub_type']
            user_id = value['user_id']
            msg += f'👉{key}\n{group_name}\n邀请人：{user_id}\n'
            num += 1
        await session.send(message=f'{msg}处理加群 [群号] [01]')
    except Exception as e:
        await session.send(f'{e}')


#
#
# @on_request('group.add')
# async def handle_group_invite(session: RequestSession):
#     if session.ctx['user_id'] in nonebot.get_bot().config.SUPERUSERS:
#         await session.approve()
#     else:
#         await session.reject(reason='邀请入群请联系维护组')
