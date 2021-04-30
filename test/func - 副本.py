import os
from nonebot import on_command, CommandSession
import aiohttp
import asyncio
import requests
import pydest
from hoshino import Service, R
from hoshino.typing import CQEvent
from nonebot import *
import json
import datetime
import hoshino
from PIL import Image, ImageDraw, ImageFont
import sys
import re
import time
import numpy as np
sys.path.append('C:/HoshinoBot/hoshino/modules/test')
from data.tie import gethardlink
from daily.report import getdailyreport
from data.checklist import PenguinSouvenirs, egg, 增幅, bones, cats, 称号, Exo, 暗熵碎片, 证章, 赛季挑战, 前兆, DSC, 巅峰, 宗师, 机灵, 玉兔, 赛季, 线索



HEADERS = {"X-API-Key": '19a8efe4509a4570bee47bd9883f7d93'}
API_KEY = '19a8efe4509a4570bee47bd9883f7d93'
ROOT = 'https://www.bungie.net/Platform'

destiny = pydest.Pydest(API_KEY)

with open("record.json", 'r') as load_f:
    load_dict = json.load(load_f)
    count = load_dict['counts']


def savedata():
    with open("record.json", "w") as f:
        new_dict = {'counts': count}
        json.dump(new_dict, f)


Fail = 0
args = ''
AppendInfo = ''  # '\n❗小日向将继续免费使用至18号，具体收费请回复收费以查询'

sv = hoshino.Service('命运2')


# ⚪生涯查询 [队伍码/用户名]
# 查询玩家生涯数据
# @sv.on_fullmatch(('功能', 'd2', 'D2', '喵内嘎', '喵内', '日向', '小日向', '喵内噶'))
# async def D2Help(bot, ev):
#     global count
#     count += 1
#     await bot.send(ev, HELP_MSG)


@sv.on_fullmatch('日报')
async def daily(bot, ev, only_to_me=False):
    try:
        filename = await getdailyreport()
        if filename != False:
            png_file = os.path.join(
                os.getcwd(), 'res', 'destiny2', 'img', filename)
            cqcode = f'[CQ:image,file=file:///{png_file}]'
            await bot.send(ev, cqcode)
        else:
            await bot.send(ev, '日报已更新完毕，可以再次获取啦！', at_sender=True)
    except Exception as e:
        print(e)
        await bot.send(ev, 'Bungie正在进行维护，服务器连接失败，日报更新可能需要延后')


# @sv.on_fullmatch(('收费'))
# async def D2_say(bot, ev):
#     info = f'''⚪收费标准如下：
# 6元/月 35/半年 60/年
# 群人数≤20价格半价且后续不另收费
# 如果需要购买请加QQ群827529117'''
#     await bot.send(ev, info)


class FailToGet(Exception):
    '''当输出有误时，抛出此异常'''

    # 自定义异常类型的初始化

    def __init__(self, value, msg):
        global Fail
        self.value = value
        self.msg = msg

    # 返回异常类对象的说明信息

    def __str__(self):
        return f" {self.value} 查询失败\n错误原因：{self.msg}"


class Error_Privacy(Exception):
    '''当输出有误时，抛出此异常'''

    # 自定义异常类型的初始化

    def __init__(self, value):
        self.value = value
        global Fail

    # 返回异常类对象的说明信息

    def __str__(self):
        return f" {self.value} 查询失败\n错误原因：玩家命运2数据设置为隐私不可见"


def get_success(result, name):
    print(type(result))
    if result['ErrorCode'] != 1:
        raise FailToGet(name, '未找到玩家信息，请检查是否输入了正确的id')
    else:
        return True


async def GetMembershipidAndTypeFromSteam64(credential, crType='SteamId'):
    checklist = {3: 'steam', 2: 'psn', 1: 'xbl'}
    url = ROOT + \
        f'/User/GetMembershipFromHardLinkedCredential/{crType}/{credential}'
    response = await destiny.api._get_request(url=url)
    if get_success(response, credential):
        dict = {}
        dict['membershipid'] = response['Response']['membershipId']
        dict['membershiptype_num'] = response['Response']['membershipType']
        dict['membershiptype_char'] = checklist[response['Response']
                                                ['membershipType']]
        return dict
    else:
        raise FailToGet(credential, f'无法找到该玩家信息，请检查是否输入了正确的队伍码/用户名')


async def GetMembershipidAndTypeFromSteamid(name):
    checklist = {3: 'steam', 2: 'psn', 1: 'xbl'}
    response = await destiny.api.search_destiny_player(-1, name)
    length = len(response['Response'])
    if get_success(response, name) == True:
        if length > 2:
            raise FailToGet(name, f'有{length}名玩家重名，请尝试用队伍码查询')
        else:
            if length != 0:
                if length == 1 or (length == 2 and response['Response'][0]['membershipId'] == response['Response'][1][
                        'membershipId']):
                    dict = {}
                    dict['membershipid'] = response['Response'][0]['membershipId']
                    dict['membershiptype_num'] = response['Response'][0]['membershipType']
                    dict['membershiptype_char'] = checklist[response['Response']
                                                            [0]['membershipType']]
                    return dict
                else:
                    raise FailToGet(name, f'有{length}名玩家重名，请尝试用队伍码查询')
            else:
                raise FailToGet(name, f'无法找到该玩家信息，请检查是否输入了正确的队伍码/用户名')


async def GetMembershipidAndMembershiptype(args):
    global count
    count += 1
    if args.isdigit() == True and len(args) == 17:
        # 提供的是steam64位id
        result = await GetMembershipidAndTypeFromSteam64(args)
    else:
        # 提供的是steam用户名
        result = await GetMembershipidAndTypeFromSteamid(args)
    savedata()
    return result


@on_command('pve', aliases=('PVE', 'Pve'), only_to_me=False)
async def pve(session):
    msg = '该功能已被替换，请输入 d2 查看更新菜单'
    await session.send(msg, at_sender=True)


@on_command('调试', aliases=('测试'), only_to_me=False)
async def test(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        result = await GetMembershipidAndMembershiptype(args)
        await session.send(str(result))
    except Exception as e:
        await session.send(f'{e}', at_sender=True)
        return


async def GetInfo(args, components: list) -> dict:
    components.extend([100])
    print(components)
    global count
    count += 1
    result = await GetMembershipidAndMembershiptype(args)
    membershipid = result['membershipid']
    membershiptype = result['membershiptype_num']
    response = await destiny.api.get_profile(membershiptype, membershipid, components)
    get_success(response, args)
    # TODO：在这里修复好检测玩家数据是不是隐私
    # TODO：添加玩家的绑定删除的消息提示
    # TODO：巅峰球查询有点简陋
    # TODO：群内抽奖
    # TODO：完成战绩查询的成败显示
    # TODO：蛋/骨头过多自动撤回
    # TODO：手机添加词库的时候插入图片比较困难
    # TODO：优化词库查询的显示
    # TODO：优化添加问答的正则表达式
    # TODO：优化raid查询的keyerror
    # if len(response['Response']['metrics']) == 1:
    #     raise Error_Privacy(args)
    for data in response['Response']:
        if 'data' not in response['Response'][data] and data != 'profileTransitoryData':
            raise Exception('🤔啊这...当前玩家命运2数据设置为隐私不可见')
    response['Response']['membershipid'] = membershipid
    response['Response']['membershiptype_num'] = membershiptype
    response['Response']['membershiptype_char'] = result['membershiptype_char']
    return response['Response']


# @ on_command('突袭', aliases=('raid', 'RAID', 'Raid'), only_to_me=False)
# async def GetPlayerProfile(session):
#     try:
#         hardlink = gethardlink(session)
#         if hardlink:
#             args = hardlink
#         else:
#             args = session.current_arg
#         info = await GetInfo(args, [900])
#         args = info['profile']['data']['userInfo']['displayName']
#         membershipid = info['profile']['data']['userInfo']['membershipId']
#         url = f'https://b9bv2wd97h.execute-api.us-west-2.amazonaws.com/prod/api/player/{membershipid}'
#         async with aiohttp.request("GET", url) as r:
#             # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
#             response = await r.text(encoding="utf-8")
#         raid = json.loads(response)
#         raid = raid['response']
#         clears_value = raid['clearsRank']['value']
#         if 'subtier' in raid['clearsRank']:
#             clears_rank = raid['clearsRank']['tier'] + \
#                 ' ' + raid['clearsRank']['subtier']
#         else:
#             clears_rank = raid['clearsRank']['tier']
#         speed_value = raid['speedRank']['value']
#         if 'subtier' in raid['speedRank']:
#             speed_rank = raid['speedRank']['tier'] + \
#                 ' ' + raid['speedRank']['subtier']
#         else:
#             speed_rank = raid['speedRank']['tier']
#         time = get_time_text(speed_value)
#         msg = f'''{args}
# 🎉【完成】{clears_value}次 📍{clears_rank}
# ✨【时间】{time} 🚀{speed_rank}\n'''
# # 针对小日向做了较大的更新，输入 d2 返回菜单以查看更新
# # 如果数据异常请尝试用队伍码查询'''
#         raiddict = {}
#         for i in raid['activities']:
#             raidname = await destiny.decode_hash(i['activityHash'], 'DestinyActivityDefinition')
#             raidname = raidname['displayProperties']['name']
#             clears = i['values']['clears']
#             full_clears = i['values']['fullClears']
#             sherpaCount = i['values']['sherpaCount']
#             if 'fastestFullClear' in i['values']:
#                 time = i['values']['fastestFullClear']['value']
#             else:
#                 time = 0
#             if raidname in raiddict.keys():
#                 raiddict[raidname]['clears'] += clears
#                 raiddict[raidname]['full_clears'] += full_clears
#                 raiddict[raidname]['sherpaCount'] += sherpaCount
#                 if raiddict[raidname]['time'] > time:
#                     raiddict[raidname]['time'] = time
#             else:
#                 raiddict[raidname] = {
#                     'clears': clears,
#                     'full_clears': full_clears,
#                     'sherpaCount': sherpaCount,
#                     'time': time}
#         raid_order = sorted(
#             raiddict.items(), key=lambda x: x[1]['clears'], reverse=True)
#         namedict = {
#             '世界吞噬者，利维坦: 巅峰': '世界吞噬者: 巅峰',
#             '世界吞噬者，利维坦: 普通': '世界吞噬者: 普通',
#             '忧愁王冠: 普通': '忧愁王冠',
#             '最后一愿: 等级55': '最后一愿',
#             '最后一愿: 普通': '最后一愿',
#             '利维坦，星之塔: 普通': '星之塔: 普通',
#             '利维坦，星之塔: 巅峰': '星之塔: 巅峰'
#         }
#         for i in raid_order:
#             raidname = i[0]
#             if raidname in namedict.keys():
#                 raidname = namedict[raidname]
#             clears = i[1]['clears']
#             # 利维坦，星之塔: 普通
#             full_clears = i[1]['full_clears']
#             sherpaCount = i[1]['sherpaCount']
#             time = get_time_text(i[1]['time'])
#             if get_flawless(i, info):
#                 head = f'💎{raidname}'
#             else:
#                 head = f'⚪{raidname}'
#             msg += \
#                 f'''{head}🚀{time}
#       🎐{full_clears:^3}/🎯{clears:^3}🎓{sherpaCount:^3}
# '''
#         msg += f'#回复d2以查看其他功能\n💎无暇🎐全程🎯通关🎓导师🚀最快{AppendInfo}\n❗王冠和往日无暇暂时无法查询'
#         await session.send(msg, at_sender=True)
#     except Exception as err:
#         await session.send(f'{err}', at_sender=True)


# @on_command('PVP', aliases=('pvp', 'Pvp'), only_to_me=False)
async def GetPlayerpvp(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900, 1100])
        record = info['profileRecords']['data']['records']
        metrics = info['metrics']['data']['metrics']
        args = info['profile']['data']['userInfo']['displayName']

        kill = metrics['811894228']['objectiveProgress']['progress']
        reset = metrics['3626149776']['objectiveProgress']['progress']
        kda = int(metrics['871184140']['objectiveProgress']['progress']) / 100
        valor_now = metrics['2872213304']['objectiveProgress']['progress']
        kill_this_season = metrics['2935221077']['objectiveProgress']['progress']
        Glory = metrics['268448617']['objectiveProgress']['progress']
        第七砥柱 = record['1110690562']['objectives'][0]['progress']
        万夫莫敌 = record['1582949833']['objectives'][0]['progress']
        黑夜鬼魂 = record['3354992513']['objectives'][0]['progress']
        为你而做 = record['380324143']['objectives'][0]['progress']
        msg = f'''{args}
🤞【职业生涯】
     🎯击败对手：{kill}人
     🎉英勇重置：{reset}次\n'''
        msg += f'     🙏为你而做🙏：{为你而做}次\n' if 为你而做 != 0 else ''
        msg += f'     💎第七砥柱💎：{第七砥柱}次\n' if 第七砥柱 != 0 else ''
        msg += f'     💎万夫莫敌💎：{万夫莫敌}次\n' if 万夫莫敌 != 0 else ''
        msg += f'     💎黑夜鬼魂💎：{黑夜鬼魂}次\n' if 黑夜鬼魂 != 0 else ''
        msg += f'''🤞【当前赛季】
     🎐KDA：{kda}
     🧨生存分：{Glory}
     ✨赛季击杀：{kill_this_season}
     ⚔英勇总分：{valor_now}{AppendInfo}
#回复d2以查看其他功能'''
        print(msg)
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}',at_sender=True)


def get_drop(now, localtime):
    temp = now - localtime
    if temp.days >= 365:
        return str(round(temp.days / 365)) + '年前'
    elif temp.days >= 30:
        return str(round(temp.days / 30)) + '月前'
    elif temp.days >= 7:
        return str(round(temp.days / 7)) + '周前'
    elif temp.days >= 1:
        return str(round(temp.days)) + '天前'
    elif temp.seconds >= 3600:
        return str(round(temp.seconds / 3600)) + '小时前'
    else:
        return str(round(temp.seconds / 60)) + '分钟前'


def get_kda(times):
    return str(round(times['values']['killsDeathsAssists']['basic']['value'], 1))


async def GetRaidReport(membershipid):
    try:
        url = f'https://b9bv2wd97h.execute-api.us-west-2.amazonaws.com/prod/api/player/{membershipid}'
        async with aiohttp.request("GET", url) as r:
            # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
            response = await r.text(encoding="utf-8")
        raid = json.loads(response)
        raid = raid['response']
        clears_value = raid['clearsRank']['value']
        if 'subtier' in raid['clearsRank']:
            clears_rank = raid['clearsRank']['tier'] + \
                ' ' + raid['clearsRank']['subtier']
        else:
            clears_rank = raid['clearsRank']['tier']
        speed_value = raid['speedRank']['value']
        if 'subtier' in raid['speedRank']:
            speed_rank = raid['speedRank']['tier'] + \
                ' ' + raid['speedRank']['subtier']
        else:
            speed_rank = raid['speedRank']['tier']
        if speed_value > 0:
            m, s = divmod(speed_value, 60)
            h, m = divmod(m, 60)
            if h == 0:
                time = f'{m}m{s}s'
            else:
                time = f'{h}h{m}m{s}s'
        msg = f'''完成：{clears_value}次  Speed：{time}\n'''
        return msg
    except Exception as e:
        raise FailToGet(membershipid, '获取队伍信息失败')


# @ on_command('战绩', aliases=('查询战绩', '战绩查询'), only_to_me=False)
# async def d2_activity(session):
#     try:
#         hardlink = gethardlink(session)
#         if hardlink:
#             args = hardlink
#         else:
#             args = session.current_arg
#         res = await GetInfo(args, [200])
#         args = res['profile']['data']['userInfo']['displayName']
#         msg = args + '\n'
#         for characterid in res['characters']['data']:
#             json = await destiny.decode_hash(res['characters']['data'][characterid]['classHash'], 'DestinyClassDefinition')
#             _class = json['displayProperties']['name']
#             re = await destiny.api.get_activity_history(res['profile']['data']['userInfo']['membershipType'], res['profile']['data']['userInfo']['membershipId'], characterid, count=4)
#             msg += '⚪' + _class + '⚪' + '\n'
#             for times in re['Response']['activities']:
#                 activityid = times['activityDetails']['directorActivityHash']
#                 utc = times['period']
#                 UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
#                 utcTime = datetime.datetime.strptime(utc, UTC_FORMAT)
#                 localtime = utcTime + datetime.timedelta(hours=8)
#                 now = datetime.datetime.now()
#                 time = get_drop(now, localtime)
#                 json = await destiny.decode_hash(activityid, 'DestinyActivityDefinition')
#                 activity = json['displayProperties']['name']
#                 msg += activity + ' ' + time + ' '
#                 msg += 'KDA：' + get_kda(times) + '\n'
#         msg += f'#回复d2以查看其他功能{AppendInfo}'
#         await session.send(msg, at_sender=True)
#     except Exception as e:
#         await session.send(f'{e}')


@sv.on_fullmatch(('echo'))
async def D2_condition(bot, ev):
    text = "{:,}".format(count)
    msg = f'调用次数：{text}'
    await bot.send(ev, msg)


# @sv.on_prefix(('ELO', 'Elo', 'elo'))
# async def Elo(bot, ev):
#     try:
#         args = ev.message.extract_plain_text()
#         if args.isdigit() == True and len(args) == 17:
#             # 提供的是steam64位id
#             membershipid = await GetMembershipidFromSteam64(args)
#         else:
#             # 提供的是steam用户名
#             membershipid = await GetMembershipidFromSteamid(args)


# @ on_command('ELO', aliases=('Elo', 'elo'), only_to_me=False)
# async def Elo(session):
#     try:
#         hardlink = gethardlink(session)
#         if hardlink:
#             args = hardlink
#         else:
#             args = session.current_arg
#         info = await GetMembershipidAndMembershiptype(args)
#         membershipid = info['membershipid']
#         membershiptype = info['membershiptype_num']
#         url = f'https://api.tracker.gg/api/v2/destiny-2/standard/profile/{membershiptype}/{membershipid}/segments/playlist?season=13'
#         async with aiohttp.request("GET", url) as r:
#             # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
#             response = await r.text(encoding="utf-8")
#         info = json.loads(response)
#         info = info['data']
#         msg = args+'\n'
#         checkdict = {"control": "占领",
#                      "iron-banner": "铁骑",
#                      "pvecomp_gambit": "智谋",
#                      "allMayhem": "鏖战",
#                      "trials_of_osiris": "试炼",
#                      "elimination": "灭绝",
#                      "survival": "生存",
#                      "clash": "死斗",
#                      "rumble": "混战"}
#         for i in info:
#             mode = checkdict[i['attributes']['playlist']]
#             elo = i['stats']['elo']['value']
#             # rank = round(100 - i['stats']['elo']['percentile'], 1)
#             rank = i['stats']['elo']['percentile']
#             if int(rank) <= 60:
#                 rank = f'👇后{rank:<4}%'
#             else:
#                 rank = round(100 - rank, 1)
#                 rank = f'👆前{rank:<4}%'
#             kd = float(i['stats']['kd']['displayValue'])
#             if kd > 10:
#                 kd = round(kd, 1)
#             msg += f'🎉{mode}📕 Elo:{elo:<4}\n      📏Kd:{kd:^5} {rank:\u3000<11}\n'
#         msg += f'#回复d2以查看其他功能{AppendInfo}'
#         await session.send(msg, at_sender=True)
#     except TypeError:
#         await session.send('Tracker服务器繁忙，请两分钟后再试', at_sender=True)
#     except KeyError:
#         await session.send('Tracker服务器繁忙，请两分钟后再试', at_sender=True)
#     except Exception as e:
#         await session.send(f'{e}', at_sender=True)


# @on_command('队伍', aliases=('队伍查询', '火力战队', '找内鬼'), only_to_me=False)
async def getDataFireteam(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [1000])
        args = info['profile']['data']['userInfo']['displayName']
        if len(info['profileTransitoryData']) == 1:
            raise FailToGet(args, '玩家目前不在线')
        else:
            partyMembers = info['profileTransitoryData']['data']['partyMembers']
        msg = '【火力战队查询】\n'
        for i in partyMembers:
            name = i['displayName']
            membershipid = i['membershipId']
            if i['status'] == 11:
                msg += f'🦄『{name}』\n'
            else:
                msg += f'🐴『{name}』\n'
            msg += await GetRaidReport(membershipid)
        msg += f'#回复d2以查看其他功能{AppendInfo}'
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@on_command('保存数据', aliases=('保存'), only_to_me=False)
async def savedata_hand(session):
    savedata()
    await session.send('写入成功')


def get_icon_kills(num):
    if num >= 5000:
        return '🙏'
    elif num >= 2000:
        return '😍'
    elif num >= 1000:
        return '🎉'
    else:
        return '⚪'


# @on_command('击杀数据', aliases=('击杀', '击杀查询'), only_to_me=False)
async def KillWeaponData(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        res1 = re.match(r'(7656\d{13}) +(术士|猎人|泰坦)', args)
        if res1:
            res = res1
        else:
            res = re.match(r'(.+) +(术士|猎人|泰坦)', args)
        if res:
            id = res.group(1)
            classtype = res.group(2)
            info = await GetInfo(id, [200])
            args = info['profile']['data']['userInfo']['displayName']
            membershipid = info['membershipid']
            membershiptype = info['membershiptype_char']
            classdict = {'泰坦': 3655393761, '猎人': 671679327, '术士': 2271682572}
            classhash = classdict[classtype]
            characterid = ''
            for i in info['characters']['data']:
                if classhash == info['characters']['data'][i]['classHash']:
                    characterid = info['characters']['data'][i]['characterId']
                    break
            # args = info['profile']['data']['userInfo']['displayName']
            url = f'https://api.tracker.gg/api/v2/destiny-2/standard/profile/{membershiptype}/{membershipid}/segments/detailedStat?characterId={characterid}&modeType=AllPvP'
            async with aiohttp.request("GET", url) as r:
                # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
                response = await r.text(encoding="utf-8")
            info1 = json.loads(response)
            info1 = info1['data']
            msg = args + '\n'
            weponlist = {'Shotgun': '霰弹',
                         'Melee': '近战',
                         'HandCannon': '手炮',
                         'Super': '超能',
                         'AutoRifle': '自动',
                         'Sniper': '狙击',
                         'Grenade': '手雷',
                         'PulseRifle': '脉冲',
                         'GrenadeLauncher': '榴弹',
                         'FusionRifle': '融合',
                         'TraceRifle': '追踪',
                         'RocketLauncher': '火箭',
                         'MachineGun': '机枪',
                         'SideArm': '手枪',
                         'Bow': '弓箭',
                         'Relic': '圣物',
                         'Sword': '刀剑',
                         'Submachinegun': '微冲',
                         'ScoutRifle': '斥候',
                         'Ability': '技能',
                         'BeamRifle': '追踪'}
            stata = {}
            for i in info1:
                if 'weapon' in i['attributes'].keys():
                    weapon = weponlist[i['attributes']['weapon']]
                    kills = int(i['stats']['weaponKills']['value'])
                    precisionkills = 0
                    if 'precisionKills' in i['stats']:
                        precisionkills = int(
                            i['stats']['precisionKills']['value'])
                    # if 'killsPrecisionKills' in i['stats']:
                    #     #str
                    #     accuracy = i['stats']['killsPrecisionKills']['displayValue']
                    # if 'earnedMedals' in i['stats']:
                    #     medals = int(i['stats']['earnedMedals']['value'])
                    # stata = {weapon: {'kills': kills,'precisionKills': precisionkills, 'accuracy': round(precisionkills/kills, 3)}}
                    if kills == 0:
                        acc = 0
                    else:
                        # {precisionkills:^5}📏
                        acc = round(precisionkills / kills * 100, 1)
                    stata[weapon] = {'kills': kills,
                                     'precisionkills': precisionkills, 'acc': acc}
            msg = f'{args}\n【熔炉枪械击杀数据】{classtype}\n'
            kills_order = sorted(
                stata.items(), key=lambda x: x[1]['kills'], reverse=True)
            if len(kills_order) >= 10:
                weapon_len = 10
            else:
                weapon_len = len(kills_order)
            if len(kills_order) == 0:
                raise Exception('❗连接Bungie服务器失败，请检查用户名/队伍码是否输入正确')
            for i in range(weapon_len):
                weapon = kills_order[i][0]
                kills = kills_order[i][1]['kills']
                precisionkills = kills_order[i][1]['precisionkills']
                acc = kills_order[i][1]['acc']
                icon_kills = get_icon_kills(kills)
                icon_acc = '🏹'
                if acc >= 58:
                    icon_acc = '🎯'
                msg += f'{icon_kills}{weapon}🔪{kills:^5}{icon_acc}{acc:>4}%\n'
            msg += f'🧨回复 d2 以查看其他功能{AppendInfo}'
            await session.send(msg, at_sender=True)
        else:
            raise Exception('\n❗指令格式错误啦\n👉击杀 码/名 职业')
    except pydest.PydestException as err:
        await session.send(f'连接Bungie服务器失败，请检查用户名/队伍码是否输入正确\n{err}', at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


def Check_Penguin(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['817948795']
    for key in info:
        if info[key] != True:
            notget += 1
            msg += PenguinSouvenirs[key]['name']
            msg += '📍' + PenguinSouvenirs[key]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部9只🐧啦，小日向会非常感谢你的！\n'
    else:
        head = f'🎐你还差{notget}只小🐧没收集哦，下面提供了它们的位置，快带它们回家吧！\n'
    head += msg
    return head


# @on_command('企鹅查询', aliases=('企鹅', '🐧'), only_to_me=False)
async def Check_Penguin_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [104])
        args = info['profile']['data']['userInfo']['displayName']
        msg = f'{args}【企鹅收集】\n'
        res = msg + Check_Penguin(info)
        await session.send(res, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)

        # 3981543480 现有总分
        # 3329916678 年三成就总分


def Check_egg(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['2609997025']
    for key in info:
        if info[key] != True:
            notget += 1
            msg += egg[key]['name']
            msg += '📍' + egg[key]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部40个🥚啦，你就是幽梦之城的守护者！\n'
    else:
        head = f'🎐你还差{notget}颗🥚没收集哦，下面提供了它们的位置，快带着碎愿者冲吧！\n'
    head += msg
    return head, notget


# @on_command('腐化卵查询', aliases=('孵化卵', '蛋', '卵', '🥚', '腐化卵'), only_to_me=False)
async def Check_egg_aync(session: CommandSession):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [104])
        args = info['profile']['data']['userInfo']['displayName']
        res, notget = Check_egg(info)

        message_id = await session.send(f'{args}\n{res}', at_sender=True)
        message_id = message_id['message_id']
        if notget > 15:
            await asyncio.sleep(1)
            await session.send('你的未收集物品过多，查询信息将在8秒内撤回，请复制保存。', at_sender=True)
            await asyncio.sleep(8)
            await session.bot.delete_msg(message_id=message_id, self_id=session.event.self_id)
        else:
            pass
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)

        # 3981543480 现有总分
        # 3329916678 年三成就总分


def get_gambit(info):
    record = info['profileRecords']['data']['records']
    metric = info['metrics']['data']['metrics']
    击败入侵者 = record['3381316332']['intervalObjectives'][0]['progress']
    入侵击杀守护者 = record['985373860']['intervalObjectives'][0]['progress']
    守护天使 = record['1334533602']['objectives'][0]['progress']
    一人成军 = record['511083400']['objectives'][0]['progress']
    唤雨师 = record['4206114008']['objectives'][0]['progress']
    半库江山 = record['1197518485']['objectives'][0]['progress']  # 🎯🏆✨🎐🎉💊

    赛季消灭阻绝者 = metric['2709150210']['objectiveProgress']['progress']
    赛季存储荧光 = metric['2920575849']['objectiveProgress']['progress']
    赛季智谋胜场 = metric['3483580010']['objectiveProgress']['progress']
    msg = f'''【职业生涯】
🏆唤雨师：{唤雨师}次
🏆半库江山：{半库江山}次
🏆守护天使：{守护天使}次
🏆一人成军：{一人成军}次
🎯击败入侵者：{击败入侵者}人
🎯入侵击杀守护者：{入侵击杀守护者}人
【当前赛季】
🎉智谋胜场：{赛季智谋胜场}场
✨存储荧光：{赛季存储荧光}块
🎐消灭阻绝者：{赛季消灭阻绝者}只
'''
    return msg


# @on_command('智谋', aliases=('智谋查询', '千谋'), only_to_me=False)
async def gambit_info(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900, 1100])
        args = info['profile']['data']['userInfo']['displayName']
        res = get_gambit(info)
        head = f'{args}\n' + res + '#回复d2以查看其他功能'
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_zengfu(info):
    msg = ''
    notget = 0
    info = info['profileRecords']['data']['records']['1121652081']['objectives']
    for key in info:
        if key['complete'] != True:
            notget += 1
            msg += 增幅[str(key['objectiveHash'])]['name'] + '📍' + \
                增幅[str(key['objectiveHash'])]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部8个地区的增幅✈啦，你就是木卫二的守护者！\n'
    else:
        head = f'🎐你还差{notget}个地区的增幅✈没收集哦，快看看周报决定去哪获得增幅吧~\n'
    head += msg
    return head


# @on_command('增幅', aliases=(), only_to_me=False)
async def Check_zengfu_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_zengfu(info)
        head = f'{args}\n' + res + '#回复d2以查看其他功能'
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


dungeondict = {
    1077850348: "预言",
    # 1099555105: "冥冥低语:英雄",
    1375089621: "异端深渊",
    1738383283: "先知",
    2032534090: "破碎王座",
    2124066889: "前兆:普通",
    2582501063: "异端深渊",
    # 2731208666: "行动时刻:英雄",
    4148187374: "预言",
    4212753278: "前兆:大师"}


# @ on_command('地牢', aliases=('地牢查询'), only_to_me=False)
# async def Dungeon(session):
#     try:
#         hardlink = gethardlink(session)
#         if hardlink:
#             args = hardlink
#         else:
#             args = session.current_arg
#         info = await GetInfo(args,[])
#         args = info['profile']['data']['userInfo']['displayName']
#         membershipid = info['profile']['data']['userInfo']['membershipId']
#         url = f'https://bolskmfp72.execute-api.us-west-2.amazonaws.com/dungeon/api/player/{membershipid}'
#         async with aiohttp.request("GET", url) as r:
#             # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
#             response = await r.text(encoding="utf-8")
#         dungeon = json.loads(response)
#         dungeon = dungeon['response']
#         clears = dungeon['clearsRank']
#         clears_count = clears['value']
#         clear_rank = clears['tier'] + ' ' + \
#             clears['subtier'] if 'subtier' in clears else clears['tier']
#         speed = dungeon['speedRank']
#         speed_count = get_time_text(speed['value'])
#         speed_rank = speed['tier'] + ' ' + \
#             speed['subtier'] if 'subtier' in speed else speed['tier']
#         activities = dungeon['activities']
#         head = f'''{args}【地牢查询】
# 🎉【完成】{clears_count}次 📍{clear_rank}
# ✨【时间】{speed_count} 🚀{speed_rank}
# '''
#         record = {}
#         for i in activities:
#             hashid = i['activityHash']
#             dungeonname = dungeondict[hashid] if hashid in dungeondict else ''
#             if not dungeonname:
#                 continue
#             entity = i['values']
#             if dungeonname in record:
#                 record[dungeonname]['clears'] += entity['clears']
#                 record[dungeonname]['fullClears'] += entity['fullClears']
#                 record[dungeonname]['sherpaCount'] += entity['sherpaCount']
#                 if 'fastestFullClear' in entity:
#                     record[dungeonname]['fastestFullClear'] = entity['fastestFullClear']['value'] if entity['fastestFullClear'][
#                         'value'] < record[dungeonname]['fastestFullClear'] else record[dungeonname]['fastestFullClear']
#                 if 'flawlessDetails' in entity:
#                     least = 3
#                     for j in entity['flawlessActivities']:
#                         least = [least, j['accountCount']
#                                  ][j['accountCount'] < least]
#                     record[dungeonname]['flawlessDetails'] = least if least < record[dungeonname]['flawlessDetails'] or record[
#                         dungeonname]['flawlessDetails'] == 0 else record[dungeonname]['flawlessDetails']
#                 if 'bestPlayerCountDetails' in entity:
#                     record[dungeonname]['bestPlayerCountDetails'] = entity['bestPlayerCountDetails']['accountCount'] if entity['bestPlayerCountDetails'][
#                         'accountCount'] < record[dungeonname]['bestPlayerCountDetails'] or record[dungeonname]['bestPlayerCountDetails'] == 0 else record[dungeonname]['bestPlayerCountDetails']
#             else:
#                 clears = entity['clears']
#                 fullClears = entity['fullClears']
#                 sherpaCount = entity['sherpaCount']
#                 fastestFullClear = entity['fastestFullClear']['value'] if 'fastestFullClear' in entity else 0
#                 if 'flawlessActivities' in entity:
#                     least = 3
#                     for j in entity['flawlessActivities']:
#                         least = [least, j['accountCount']
#                                  ][j['accountCount'] < least]
#                     flawlessDetails = least
#                 else:
#                     flawlessDetails = 0
#                 bestPlayerCountDetails = entity['bestPlayerCountDetails'][
#                     'accountCount'] if 'bestPlayerCountDetails' in entity else 0
#                 record[dungeonname] = {'clears': clears, 'fullClears': fullClears,
#                                        'sherpaCount': sherpaCount, 'fastestFullClear': fastestFullClear,
#                                        'flawlessDetails': flawlessDetails, 'bestPlayerCountDetails': bestPlayerCountDetails}

#         # 归类完成
#         dungeon_order = sorted(
#             record.items(), key=lambda x: x[1]['clears'], reverse=True)
#         for i in dungeon_order:
#             dungeonname = i[0]
#             singledict = i[1]
#             clears = singledict['clears']
#             fullClears = singledict['fullClears']
#             sherpaCount = singledict['sherpaCount']
#             fastestFullClear = get_time_text(singledict['fastestFullClear'])
#             icon1 = '💎'if singledict['flawlessDetails'] == 1 else '⚪'
#             icon2 = '🎉' if singledict['bestPlayerCountDetails'] == 1 else '⚪'
#             head += f'''{icon1}{icon2}『{dungeonname}』🚀{fastestFullClear}
#         🎯{fullClears:<3}/✅{clears:<3} 🎓{sherpaCount:<2}\n'''
#         head += '💎单人无暇 🎉单人\n🚀回复d2以查看其他功能'
#         await session.send(head, at_sender=True)
#     except Exception as e:
#         await session.send(f'获取失败，{e}', at_sender=True)


def Check_bones(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['1297424116']
    for i in bones:
        if info[i] == False:
            notget += 1
            msg += bones[i]['name']
            msg += '📍' + bones[i]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部16个阿罕卡拉遗骨🦴啦，你就是行遍幽梦之城的破咒者\n'
    else:
        head = f'🎐你还差{notget}个遗骨🦴没收集哦，顺便去看看这周上维挑战在哪嗷\n'
    head += msg
    return head, notget


# @on_command('骨头', aliases=('🦴'), only_to_me=False)
async def Check_bones_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [104])
        args = info['profile']['data']['userInfo']['displayName']
        res, notget = Check_bones(info)
        head = f'{args}\n' + res
        message_id = await session.send(head, at_sender=True)
        message_id = message_id['message_id']
        if notget > 10:
            await asyncio.sleep(1)
            await session.send('你的未收集物品过多，查询信息将在10秒内撤回，请复制保存。', at_sender=True)
            await asyncio.sleep(10)
            await session.bot.delete_msg(message_id=message_id, self_id=session.event.self_id)
        else:
            pass

    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_cats(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['2726513366']
    for i in cats:
        if info[i] == False:
            notget += 1
            msg += cats[i]['name']
            msg += '📍' + cats[i]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部9只小猫🐱啦，九柱神向你表示感谢\n'
    else:
        head = f'🎐你还差{notget}只小猫🐱没收集哦，下面是它们的位置：\n'
    head += msg
    return head


# @on_command('猫', aliases=('🐱'), only_to_me=False)
async def Check_cats_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [104])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_cats(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


# def Check_chenghao(info):
#     msg = ''
#     notget = 0
#     info = info['profileProgression']['data']['checklists']['1297424116']
#     for i in bones:
#         if info[i] == False:
#             notget+=1
#             msg+=bones[i]['name']
#             msg+='📍'+bones[i]['location']+'\n'
#     msg += '#回复d2以查看其他功能'
#     if notget == 0:
#         head = '🎉你已经收集了全部16个阿罕卡拉遗骨🦴啦，你就是行遍幽梦之城的破咒者\n'
#     else:
#         head = f'🎐你还差{notget}个遗骨🦴没收集哦，顺便去看看这周上维挑战在哪嗷\n'
#     head += msg
#     return head


# @ on_command('称号', only_to_me=False)
# async def Check_bchenghao_aync(session):
#     try:
#         hardlink = gethardlink(session)
#         if hardlink:
#             args = hardlink
#         else:
#             args = session.current_arg
#         info = await GetInfo(args,[])
#         args = info['profile']['data']['userInfo']['displayName']
#         res = Check_chenghao(info)
#         head = f'{args}\n' + res
#         await session.send(head, at_sender=True)
#     except Exception as e:
#         await session.send(f'获取失败，{e}', at_sender=True)


def Check_chenghao(info):
    msg = ''
    info = info['profileRecords']['data']['records']
    for i in 称号:
        objectives = info[i]['objectives'][0]
        progress = objectives['progress']
        completionValue = objectives['completionValue']
        icon = '🎯' if completionValue <= progress else '⚪'
        icon = '🏆' if 'gold' in 称号[i] and progress == 称号[i]['gold'] else icon
        name = 称号[i]['name']
        msg += f'{icon}{name}：{progress}/{completionValue}\n'
    msg += '🎉回复d2以查看其他功能'
    head = '【称号查询】\n'
    head += msg
    return head


# @on_command('称号', only_to_me=False)
async def Check_chenghao_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_chenghao(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_exo(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['2568476210']
    for i in Exo:
        if info[i] == False:
            notget += 1
            msg += Exo[i]['name']
            msg += '📍' + Exo[i]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部9只🐾死去的Exo啦\n'
    else:
        head = f'🎐你还差{notget}只🐾死去的Exo没收集哦，下面是它们的位置：\n'
    head += msg
    return head


# @on_command('exo', aliases=('Exo', 'EXO'), only_to_me=False)
async def Check_exo_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [104])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_exo(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_suipian(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['1885088224']
    for i in 暗熵碎片:
        if info[i] == False:
            notget += 1
            msg += 暗熵碎片[i]['name']
            msg += '📍' + 暗熵碎片[i]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部9个🔷暗熵碎片啦\n'
    else:
        head = f'🎐你还差{notget}个🔷暗熵碎片没收集哦，下面是它们的位置：\n'
    head += msg
    return head


# @on_command('碎片', aliases=('暗熵碎片', '碎片查询', '🧩'), only_to_me=False)
async def Check_suipian_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [104])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_suipian(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)





def Check_saijitiaozhan(info):
    msg = ''
    info = info['characterPresentationNodes']['data']
    characterid = list(info.keys())[0]
    info = info[characterid]['nodes']
    for i in 赛季挑战:
        objectives = info[i]
        progressValue = objectives['progressValue']
        completionValue = objectives['completionValue']
        icon = '✅' if completionValue == progressValue and completionValue != 0 else '⚪'
        name = 赛季挑战[i]
        msg += f'{icon}{name}：{progressValue}/{completionValue}\n'
    msg += '🎉回复d2以查看其他功能'
    head = '【赛季挑战】\n'
    head += msg
    return head


# @on_command('赛季挑战', only_to_me=False)
async def Check_saijitiaozhan_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [700])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_saijitiaozhan(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_qianzhao(info):
    msg = ''
    records = info['profileRecords']['data']['records']
    格力康号线索 = info['profileProgression']['data']['checklists']['3975225462']
    notShowTag = 0
    notGetWeek = 0
    for i in 前兆['碎片']:
        objectives = records[i]['objectives'][0]
        progressValue = objectives['progress']
        completionValue = objectives['completionValue']
        icon = '✅' if completionValue == progressValue else '⚪'
        name = 前兆['碎片'][i]['name']
        msg += f'{icon}{name}：{progressValue}/{completionValue}\n'
        if progressValue != completionValue:
            notGetWeek += 1
            if notShowTag:
                continue
            else:
                notShowTag = 1
            entries = 前兆['碎片'][i]['entries']
            for check in entries:
                if not 格力康号线索[check]:
                    msg += f'{entries[check]["name"]}：{entries[check]["location"]}\n'


    for i in 前兆['成就']:
        objectives = records[i]['intervalObjectives'][11]
        progressValue = objectives['progress']
        completionValue = objectives['completionValue']
        icon = '✅' if completionValue == progressValue else '⚪'
        name = 前兆['成就'][i]
        msg += f'{icon}{name}：{progressValue}/{completionValue}\n'

    msg += '🎉回复d2以查看其他功能'
    head = '【前兆查询】\n'
    head += msg
    return head,notGetWeek


# @on_command('前兆', only_to_me=False)
async def Check_qianzhao_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900, 104])
        args = info['profile']['data']['userInfo']['displayName']
        res,notGetWeek = Check_qianzhao(info)
        head = f'{args}\n' + res
        print(head)
        await session.send(head, at_sender=True)
        if notGetWeek:
            await asyncio.sleep(2)
            await session.send(f'ヾ(•ω•`)o\n😝现在天选赛季结束还有3周\n👉[{args}]还差 {notGetWeek}周 的线索没有摸完\n👉摸完全部3周的线索可以解锁天选者称号的隐藏成就\n🤣小日向提醒你一下，别忘了噢', at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


classdict = {3655393761: '泰坦', 671679327: '猎人', 2271682572: '术士',
             '泰坦': 3655393761, '猎人': 671679327, '术士': 2271682572}


def Check_DSC(info):
    msg = ''
    characterProgressions = info['characterProgressions']['data']
    characters = info['characters']['data']
    Record = info['profileRecords']['data']['records']
    职业 = ''
    职业msg = ''
    关卡 = ['', '', '', '']
    for i in characterProgressions:
        characterName = classdict[characters[i]['classHash']]
        milestones = characterProgressions[i]['milestones']
        msg += f'{characterName}：'
        if '541780856' in milestones:
            phases = milestones['541780856']['activities'][0]['phases']
            for j in range(4):
                complete = phases[j]['complete']
                msg += '✅' if complete == True else '⚪'
        else:
            for j in range(4):
                msg += '✅'
        msg += '\n'

    msg += '【挑战查询】\n'
    for i in DSC['挑战']:
        name = DSC['挑战'][i]
        icon = '✅' if Record[i]['objectives'][0]['complete'] == True else '⚪'
        msg += f'{icon}{name}\n'
    msg += '🎉回复d2以查看其他功能\n❗由于Bungie数据问题，只打尾王也算完成了全程'
    head = '【深岩墓室查询】\n'
    head += msg
    return head


# @on_command('地窖', aliases=('深岩墓室'), only_to_me=False)
async def Check_DSC_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [200, 202, 900])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_DSC(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_dianfeng(info, characterId):
    msg = ''
    info = info['characterProgressions']['data'][characterId]['milestones']
    for i in 巅峰:
        if 'name' not in 巅峰[i]:
            # earned = info[i]['rewards'][0]['entries'][0]['earned']
            icon = '⚪' if i in info else '✅'
            name = 巅峰[i]
            msg += f'{icon}{name}\n'
        else:
            icon = '⚪' if i in info else '✅'
            # earned = info[i]['availableQuests'][0]['status']['completed']
            name = 巅峰[i]['name']
            msg += f'{icon}{name}\n'
    msg += '🎉回复d2以查看其他功能'
    head = '【巅峰球查询】\n'
    head += msg
    return head


# @on_command('巅峰', aliases=('巅峰球'), only_to_me=False)
async def Check_dianfeng_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        res1 = re.match(r'(7656\d{13}) +(术士|猎人|泰坦)', args)
        res = res1 if res1 else re.match(r'(.+) +(术士|猎人|泰坦)', args)

        if res:
            id = res.group(1)
            classtype = classdict[res.group(2)]
            info = await GetInfo(id, [200, 202])
            args = info['profile']['data']['userInfo']['displayName']
            for characterId in info['characters']['data']:
                if info['characters']['data'][characterId]['classHash'] == classtype:
                    break
            msg = Check_dianfeng(info, characterId)
            head = f'{args}\n' + msg
            await session.send(head, at_sender=True)
        else:
            raise Exception('\n❗指令格式错误啦\n👉巅峰 名/码 职业')
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


def get_zongshi_icon(num):
    if num == 0:
        return '⚪'
    elif num <= 15:
        return '✅'
    elif num <= 30:
        return '🎉'
    else:
        return '🙏'


def Check_zongshi(info):
    msg = ''
    info = info['profileRecords']['data']['records']
    for i in 宗师:
        objectives = info[i]['objectives'][0]
        progress = objectives['progress']
        icon = get_zongshi_icon(progress)
        name = 宗师[i]
        msg += f'{icon}{name}：{progress}次\n'
    msg += '🎉回复d2以查看其他功能'
    head = '【宗师查询】\n'
    head += msg
    return head


# @on_command('宗师', only_to_me=False)
async def Check_zongshi_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_zongshi(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_jiling(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['1856270404']
    for i in 机灵:
        if info[i] == False:
            notget += 1
            msg += 机灵[i]['name']
            msg += '📍' + 机灵[i]['location'] + '\n'
    msg += '🎉回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部10个📕机灵啦\n'
    else:
        head = f'🎐你还差{notget}个📕机灵没收集哦，下面是它们的位置：\n'
    head += msg
    return head


# @on_command('机灵', aliases=('死去的机灵',), only_to_me=False)
async def Check_jiling_aync(session: CommandSession):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [104])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_jiling(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_yutu(info, characterId):
    msg = ''
    notget = 0
    info = info['characterProgressions']['data'][characterId]['checklists']['1912364094']
    for i in 玉兔:
        if info[i] == False:
            notget += 1
            msg += 玉兔[i]['name']
            msg += '📍' + 玉兔[i]['location'] + '\n'
    if notget == 0:
        head = '🎉你已经收集了全部9只🐇兔子啦\n'
    else:
        head = f'🎐你还差{notget}只🐇兔子没收集哦，下面是它们的位置：\n'
    msg += '🎉回复d2以查看其他功能'
    head += msg
    return head


# @on_command('兔子', aliases=('玉兔'), only_to_me=False)
async def Check_yutu_aync(session: CommandSession):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        res1 = re.match(r'(7656\d{13}) +(术士|猎人|泰坦)', args)
        res = res1 if res1 else re.match(r'(.+) +(术士|猎人|泰坦)', args)

        if res:
            id = res.group(1)
            classtype = classdict[res.group(2)]
            info = await GetInfo(id, [200, 202])
            args = info['profile']['data']['userInfo']['displayName']
            for characterId in info['characters']['data']:
                if info['characters']['data'][characterId]['classHash'] == classtype:
                    break
            msg = Check_yutu(info, characterId)
            head = f'{args}\n' + msg
            await session.send(head, at_sender=True)
        else:
            raise Exception('\n❗指令格式错误啦\n👉兔子 名/码 职业')
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


def GetDaysPlayedTotal(minutes: int) -> str:
    days = round(int(minutes)/60, 1)
    return f'{days}h'


def Check_shengya(info):
    msg = ''
    character_msg = ''
    seasons = info['profile']['data']['seasonHashes']
    characters = info['characters']['data']
    records = info['profileRecords']['data']
    传承成就分 = "{:,}".format(records['legacyScore'])
    当前成就分 = "{:,}".format(records['activeScore'])
    熔炉胜场 = records['records']['3561485187']['intervalObjectives'][0]['progress']
    智谋胜场 = records['records']['1676011372']['objectives'][0]['progress'] + \
        records['records']['2129704137']['objectives'][0]['progress'] + \
        records['records']['89114360']['objectives'][0]['progress']
    打击列表 = records['records']['2780814366']['objectives'][2]['progress']

    season_msg = '年三：'
    for season in 赛季['年三']:
        if season in seasons:
            season_msg += f'✅{赛季["年三"][season]}'
        else:
            season_msg += f'⚪{赛季["年三"][season]}'
    season_msg += '\n年四：'
    for season in 赛季['年四']:
        if season in seasons:
            season_msg += f'✅{赛季["年四"][season]}'
        else:
            season_msg += f'⚪{赛季["年四"][season]}'
    for value in characters.values():
        className = classdict[value['classHash']]
        daysPlayedTotal = GetDaysPlayedTotal(value['minutesPlayedTotal'])
        character_msg += f'📕{className}：{daysPlayedTotal}\n'

    msg = f'''
{season_msg}
🔷传承成就分：{传承成就分}
🔷当前成就分：{当前成就分}
{character_msg}🏅熔炉胜场：{熔炉胜场}次
🏅智谋胜场：{智谋胜场}次
🏅打击列表：{打击列表}次
'''
    msg += '🎉回复d2以查看其他功能'
    return msg


# @on_command('生涯', aliases=('生涯查询', '角色查询'), only_to_me=False)
async def Check_shengya_aync(session: CommandSession):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [200, 900])
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_shengya(info)
        head = f'{args}' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


# def Check_rabbit(info):
#     明日之眼 = info['profileCollectibles']['data']['collectibles']['753200559']['state']


# @ on_command('突袭周常', only_to_me=False)
# async def Check_mingrizhiyan_aync(session):
#     try:
#         hardlink = gethardlink(session)
#         if hardlink:
#             args = hardlink
#         else:
#             args = session.current_arg
#         info = await GetInfo(args,[])
#         args = info['profile']['data']['userInfo']['displayName']
#         res = Check_weeklyraid(info)
#         head = f'{args}\n' + res
#         await session.send(head, at_sender=True)
#     except Exception as e:
#         await session.send(f'获取失败，{e}', at_sender=True)


黑色 = '#000000'
灰色 = '#818181'
黑体 = ImageFont.truetype('simhei.ttf', size=20)
活动标题 = ImageFont.truetype('font1559.ttf', size=30)
标题2 = ImageFont.truetype('font1559.ttf', size=24)
绿块 = Image.new('RGB', [40, 100], '#00b034')
红块 = Image.new('RGB', [40, 100], (229, 115, 125))





奇数颜色_战绩 = '#292929'
偶数颜色_战绩 = '#1F1F1F'
奇数块_战绩 = Image.new('RGB', [1000, 100], 奇数颜色_战绩)
偶数块_战绩 = Image.new('RGB', [1000, 100], 偶数颜色_战绩)

绿色_战绩 = '#3D8D4D'
红色_战绩 = '#8F2020'
标题_战绩 = ImageFont.truetype('MYingHeiPRC-W7.ttf',size=20)
KD字体_战绩 = ImageFont.truetype('MYingHeiPRC-W7.ttf',size=36)
KD标题字体_战绩 = ImageFont.truetype('MYingHeiPRC-W4.ttf',size=20)
中字_战绩 = ImageFont.truetype('MYingHeiPRC-W5.ttf',size=16)
小字_战绩 = ImageFont.truetype('MYingHeiPRC-W4.ttf',size=16)



def get_activity_time(period):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utcTime = datetime.datetime.strptime(period, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    now = datetime.datetime.now()
    temp = now - localtime
    if temp.days >= 365:
        return str(round(temp.days / 365)) + '年前'
    elif temp.days >= 30:
        return str(round(temp.days / 30)) + '月前'
    elif temp.days >= 7:
        return str(round(temp.days / 7)) + '周前'
    elif temp.days >= 1:
        return str(round(temp.days)) + '天前'
    elif temp.seconds >= 3600:
        return str(round(temp.seconds / 3600)) + '小时前'
    else:
        return str(round(temp.seconds / 60)) + '分钟前'


@ on_command('战绩', aliases=('查询战绩', '战绩查询'), only_to_me=False)
async def d2_activity(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        res = await GetInfo(args, [200])
        args = res['profile']['data']['userInfo']['displayName']
        
        activityList = []
        characters = res['characters']['data']

        characterIdList = list(characters.keys())
        for characterId in characterIdList:
            className = classdict[characters[characterId]['classHash']]
            activities = await destiny.api.get_activity_history(res['membershiptype_num'], res['membershipid'], characterId, 50)
            if activities['ErrorStatus'] != 'Success':
                Message = activities['Message']
                raise Exception(f'🤔啊这...战绩查询失败了，可能是玩家设置了数据隐私。\n{Message}')
            activities = activities['Response']['activities']
            for i in activities:
                i['characterId'] = characterId
                i['className'] = className
            activityList.extend(activities)
        activityList_order = sorted(
            activityList, key=lambda x: x['period'], reverse=True)
        activityListToBeUsed = activityList_order[:50]
        


        Length = len(activityListToBeUsed)
        activityRaw = Image.new('RGB', [1000, 80+Length*100], '#303030')
        draw = ImageDraw.Draw(activityRaw)

        draw.text([60,15],
            f'小日向战绩查询: {args}',
            font=KD字体_战绩, 
            fill='white')
        
        
        
        for i in range(50):
            activity = activityListToBeUsed[i]
            res = await destiny.decode_hash(activity['activityDetails']['directorActivityHash'], 'DestinyActivityDefinition')
            res2 = await destiny.decode_hash(activity['activityDetails']['referenceId'], 'DestinyActivityDefinition')
            模式 = res['displayProperties']['name']
            名称 = res2['displayProperties']['name']
            modeNum = activity['activityDetails']['modes']
            时间 = get_activity_time(activity['period'])
            K = int(activity['values']['kills']['basic']['displayValue'])
            D = int(activity['values']['deaths']['basic']['displayValue'])
            A = int(activity['values']['assists']['basic']['displayValue'])
            KD = activity['values']['killsDeathsRatio']['basic']['displayValue']
            进行时间 = activity['values']['timePlayedSeconds']['basic']['displayValue']
            Score = int(activity['values']['score']['basic']['value'])
            ScoreShow = activity['values']['score']['basic']['displayValue']

            teamScore = int(activity['values']['teamScore']['basic']['value'])
            if i % 2 ==0:
                activityRaw.paste(偶数块_战绩,[0,80+i*100])
            else:
                activityRaw.paste(奇数块_战绩,[0,80+i*100])

            draw.text([60,95+i*100],
                f'{模式}',
                font=标题_战绩, 
                fill='white'
                )

            draw.text([60,125+i*100],
                f'▢ {名称}',
                font=小字_战绩, 
                fill='#E5E5E5'
                )
            
            draw.text([60,150+i*100],
                f'▢ {时间} · 用时 {进行时间}',
                font=小字_战绩, 
                fill='#E5E5E5'
                )

            draw.text([410,95+i*100],
                f'K: {K}',
                font=中字_战绩, 
                fill='white')

            draw.text([410,120+i*100],
                f'D: {D}',
                font=中字_战绩, 
                fill='white'
                )
            draw.text([410,145+i*100],
                f'A: {A}',
                font=中字_战绩, 
                fill='white'
                )

            KandD = K + D
            try:
                D长度 = int(150 * D / KandD)
            except:
                D长度 = 0
            K长度 = 150 - D长度
            KD_K = Image.new('RGB', [K长度, 10], '#03A9F4')
            KD_D = Image.new('RGB', [D长度, 10], '#E8786E')
            activityRaw.paste(KD_K, (490, 135+100*i))
            activityRaw.paste(KD_D, (490 + K长度, 135+100*i))
            w,h = KD字体_战绩.getsize(f'{KD}')
            draw.text([640-w,90+i*100],
                f'{KD}',
                font=KD字体_战绩, 
                fill='white'
                )
            draw.text([490,150+i*100],
                f'KD',
                font=KD标题字体_战绩, 
                fill='white'
                )
            
            try:
                if Score > teamScore:
                    teamScore = Score
                Score长度 = int (150 * Score / teamScore)
            except:
                Score长度 = 150
            其他Score长度 = 150 - Score长度
            我score = Image.new('RGB', [Score长度, 10], '#03A9F4')
            其他score = Image.new('RGB', [其他Score长度, 10], '#E8786E')
            activityRaw.paste(我score, (670, 135+100*i))
            activityRaw.paste(其他score, (670 + Score长度, 135+100*i))
            w,h = KD字体_战绩.getsize(f'{ScoreShow}')
            draw.text([820-w,90+i*100],
                f'{ScoreShow}',
                font=KD字体_战绩, 
                fill='white'
                )
            draw.text([670,150+i*100],
                f'SCORE',
                font=KD标题字体_战绩, 
                fill='white'
                )





            # draw.text([700,90+i*100],
            #     f'{Score}',
            #     font=KD字体_战绩, 
            #     fill='white'
            #     )
            # draw.text([700,135+i*100],
            #     f'SCORE',
            #     font=KD标题字体_战绩, 
            #     fill='white'
            #     )
            draw.text([850,90+i*100],
                f"{activity['className']}",
                font=KD字体_战绩, 
                fill='white'
                )
            draw.text([850,135+i*100],
                f'CHARACTER',
                font=KD标题字体_战绩, 
                fill='white'
                )

            if activity['activityDetails']['mode'] == 6:
                continue

            if 'standing' in activity['values']:
                if activity['values']['standing']['basic']['displayValue'] == 'Victory':
                    activityRaw.paste(绿块, (0, 80 + 100 * i))
                elif activity['values']['standing']['basic']['displayValue'] == 'Defeat':
                    activityRaw.paste(红块, (0, 80 + 100 * i))
                else:
                    if activity['values']['standing']['basic']['value'] <= 2:
                        activityRaw.paste(绿块, (0, 80 + 100 * i))
                    else:
                        activityRaw.paste(红块, (0, 80 + 100 * i))

            else:
                if activity['values']['completed']['basic']['displayValue'] == 'Yes':
                    if activity['values']['completionReason']['basic']['displayValue'] == 'Failed':
                        activityRaw.paste(红块, (0, 80 + 100 * i))
                        continue

                    activityRaw.paste(绿块, (0, 80 + 100 * i))
   
                else:
                    activityRaw.paste(红块, (0, 80 + 100 * i))
        
        
        name = time.time()
        path = os.path.join(os.getcwd(), 'res', 'destiny2',
                            'cache', f'activit_{name}.png')
        activityRaw.save(path, 'png')
        append = f'[CQ:image,file=file:///{path}]'
        await session.send(append)
    except Exception as e:
        await session.send(f'{e}',at_sender=True)

eloModeDict = {"control": "占领",
               "iron-banner": "铁骑",
               "pvecomp_gambit": "智谋",
               "allMayhem": "鏖战",
               "trials_of_osiris": "试炼",
               "elimination": "灭绝",
               "survival": "生存",
               "clash": "死斗",
               "rumble": "混战"}


async def GetEloDict(membershiptype, membershipid):
    url = f'https://api.tracker.gg/api/v2/destiny-2/standard/profile/{membershiptype}/{membershipid}/segments/playlist?season=13'
    async with aiohttp.request("GET", url) as r:
        # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
        response = await r.text(encoding="utf-8")
    info = json.loads(response)
    info = info['data']
    eloDict = {}
    for i in info:
        try:
            模式 = eloModeDict[i['attributes']['playlist']]
        except:
            continue
        Elo颜色 = eval(i['stats']['elo']['metadata']['rankColor']
                     ['value'].replace('rgb(', '').replace(')', ''))
        Elo分 = i['stats']['elo']['displayValue']
        if not (Elo排名 := i['stats']['elo']['rank']):
            Elo排名 = 999999

        if not (Elo排名百分比 := i['stats']['elo']['percentile']):
            Elo排名百分比 = 0
        Elo段位 = i['stats']['elo']['metadata']['rankName'].replace('Diamond', '钻石').replace(
            'Platinum', '白金').replace('Gold', '黄金').replace('Silver', '白银').replace('Bronze', '青铜')
        Elo段位名称 = Elo段位[:2]
        胜利 = i['stats']['activitiesWon']['value']
        失败 = i['stats']['activitiesLost']['value']
        胜率 = i['stats']['wl']['displayValue']
        K = i['stats']['kills']['value']
        D = i['stats']['deaths']['value']
        A = i['stats']['assists']['value']
        KD = i['stats']['kd']['displayValue']
        KDA = i['stats']['kda']['displayValue']
        KAD = i['stats']['kad']['displayValue']
        eloDict[模式] = {
            'Elo颜色': Elo颜色,
            'Elo分': Elo分,
            'Elo排名': Elo排名,
            'Elo排名百分比': Elo排名百分比,
            'Elo段位': Elo段位,
            'Elo段位名称': Elo段位名称,
            '胜利': 胜利,
            '失败': 失败,
            '胜率': 胜率,
            'K': K,
            'D': D,
            'A': A,
            'KD': KD,
            'KDA': KDA,
            'KAD': KAD
        }
    return eloDict


标题 = ImageFont.truetype('思源黑体B.otf', size=20)
模式 = ImageFont.truetype('思源黑体B.otf', size=26)
描述文本 = ImageFont.truetype('数字字体.ttf', size=20)
段位 = ImageFont.truetype('Dengb.ttf', size=18)
Elo分 = ImageFont.truetype('数字字体.ttf', size=26)
标题文字 = '#CCCCCC'
奇数颜色 = '#292929'
偶数颜色 = '#1F1F1F'
排行白色 = '#B7B7B7'
排行灰色 = '#545454'
奇数背景 = Image.new('RGB', [1200, 80], 奇数颜色)
偶数背景 = Image.new('RGB', [1200, 80], 偶数颜色)


@ on_command('ELO', aliases=('Elo', 'elo'), only_to_me=False)
async def Elo(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [])
        args = info['profile']['data']['userInfo']['displayName']
        membershiptype = info['profile']['data']['userInfo']['membershipType']
        membershipid = info['profile']['data']['userInfo']['membershipId']
        eloDict = await GetEloDict(membershiptype, membershipid)
        eloDictLength = len(eloDict)
        img_elo = Image.new('RGB', [1050, 100+eloDictLength*80], '#303030')
        draw = ImageDraw.Draw(img_elo)
        标题块 = Image.new('RGB', [1200, 40], '#3D3D3D')
        img_elo.paste(标题块, (0, 60))
        draw.text((50, 20), f'小日向Elo查询：{args}',
                  font=模式, fill=标题文字, direction=None)
        draw.text((60, 70), f'模式/段位', font=标题, fill=标题文字, direction=None)
        draw.text((300, 70), f'排名', font=标题, fill=标题文字, direction=None)
        draw.text((550, 70), f'K/D', font=标题, fill=标题文字, direction=None)
        draw.text((800, 70), f'胜率 %', font=标题, fill=标题文字, direction=None)
        keysList = list(eloDict.keys())
        for i in range(eloDictLength):
            模式名称 = keysList[i]
            try:
                mode = eloDict[模式名称]
            except:
                continue
            Elo分数 = mode['Elo分']
            Elo排名 = "{:,}".format(mode['Elo排名'])
            Elo段位 = mode['Elo段位']
            Elo段位名称 = mode['Elo段位名称']
            段位图片 = Image.open(f'{Elo段位名称} (自定义).png')
            Elo颜色 = mode['Elo颜色']
            Elo排名百分比 = mode['Elo排名百分比']
            K = int(mode['K'])
            D = int(mode['D'])
            KD = mode['KD']
            胜利 = int(mode['胜利'])
            失败 = int(mode['失败'])
            胜率 = mode['胜率']
            if i % 2 == 0:
                img_elo.paste(偶数背景, (0, 100 + 80 * i))
                段位图片 = Image.composite(段位图片, Image.new(
                    'RGB', 段位图片.size, 偶数颜色), 段位图片)
            else:
                img_elo.paste(奇数背景, (0, 100 + 80 * i))
                段位图片 = Image.composite(段位图片, Image.new(
                    'RGB', 段位图片.size, 奇数颜色), 段位图片)
            img_elo.paste(段位图片, (60, 105+80*i))

            draw.text((135, 130+80*i), f'{模式名称}',
                      font=模式, fill='white', direction=None)
            draw.text((200, 135+80*i), f'{Elo段位}',
                      font=段位, fill=Elo颜色, direction=None)
            灰高 = int((100 - Elo排名百分比) * 0.6)
            白高 = 60-灰高
            Rating灰 = Image.new('RGB', [10, 灰高], 排行灰色)
            Rating白 = Image.new('RGB', [10, 白高], 排行白色)
            img_elo.paste(Rating灰, (300, 110+80*i))
            img_elo.paste(Rating白, (300, 110 + 灰高+80*i))
            draw.text((320, 115 + 80 * i), f'{Elo分数}',
                      font=Elo分, fill='white', direction=None)
            if Elo排名百分比 >= 70:
                temp = round(100-Elo排名百分比, 1)
                Elo排名描述性 = f'Top {temp}%'

            else:
                Elo排名描述性 = f'Bottom {Elo排名百分比}%'

            draw.text((320, 145+80*i), f'#{Elo排名} • {Elo排名描述性}',
                      font=描述文本, fill='#FCD401' if Elo排名百分比 >= 90 else '#C3C3C3', direction=None)
            绿色 = '#3D8D4D'
            红色 = '#8F2020'
            KandD = K + D
            try:
                K长度 = int(200 * K / KandD)
            except:
                K长度 = 0
            D长度 = 200 - K长度
            KD_K = Image.new('RGB', [K长度, 10], 绿色)
            KD_D = Image.new('RGB', [D长度, 10], 红色)
            img_elo.paste(KD_K, (550, 150+80*i))
            img_elo.paste(KD_D, (550 + K长度, 150+80*i))
            draw.text((550, 115+80*i), f'{KD}',
                      font=Elo分, fill='white', direction=None)
            draw.text((630, 120+80*i), f'({K} - {D})',
                      font=描述文本, fill='#C3C3C3', direction=None)
            WandL = 胜利+失败
            try:
                W长度 = int(200 * 胜利 / WandL)
            except:
                W长度 = 0
            L长度 = 200 - W长度
            WL_W = Image.new('RGB', [W长度, 10], 绿色)
            WL_L = Image.new('RGB', [L长度, 10], 红色)
            img_elo.paste(WL_W, (800, 150+80*i))
            img_elo.paste(WL_L, (800 + W长度, 150+80*i))
            draw.text((800, 115+80*i), f'{胜率}%',
                      font=Elo分, fill='white', direction=None)
            draw.text((860, 120+80*i), f'({胜利} - {失败})',
                      font=描述文本, fill='#C3C3C3', direction=None)

        name = time.time()
        path = os.path.join(os.getcwd(), 'res', 'destiny2',
                            'cache', f'elo_{name}.png')
        img_elo.save(path, 'png')
        append = f'[CQ:image,file=file:///{path}]'
        await session.send(f'{append}', at_sender=False)

    except KeyError as err:
        await session.send(f'Tracker服务器繁忙，请两分钟后再试\n{err}', at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


RAID_LIST = ['深岩墓室', '救赎花园', '最后一愿', '忧愁王冠', '往日之苦', '星之塔：巅峰',
             '利维坦：巅峰', '世界吞噬者：巅峰', '星之塔：普通', '世界吞噬者：普通', '利维坦：普通']
FLAWLESS_DICT = {
    6: 'Flawless',
    5: 'Flawless',
    4: 'Flawless',
    3: 'Flawless Trio',
    2: 'Flawless Duo',
    1: 'Solo Flawless'}
LOWMAN_DICT = {
    3: 'Trio',
    2: 'Duo',
    1: 'Solo'}

TAG_COLOR_DICT = {
    'Flawless': '#31b573',
    'Flawless Trio': '#FA576F',
    'Flawless Duo':'#FA576F',
    'Solo Flawless':'#FA576F',
    'Trio':'#f4b757',
    'Duo':'#f4b757',
    'Solo':'#00709e',

}


RAID_NAEM_DICT = {
    '深岩墓室': '深岩墓室',
    '最后一愿: 等级55': '最后一愿',
    '最后一愿: 普通': '最后一愿',
    '救赎花园': '救赎花园',
    '往日之苦': '往日之苦',
    '忧愁王冠: 普通': '忧愁王冠',
    '利维坦: 巅峰': '利维坦：巅峰',
    '利维坦: 普通': '利维坦：普通',
    '利维坦，星之塔: 普通': '星之塔：普通',
    '利维坦，星之塔: 巅峰': '星之塔：巅峰',
    '世界吞噬者，利维坦: 巅峰': '世界吞噬者：巅峰',
    '世界吞噬者，利维坦: 普通': '世界吞噬者：普通',
    '世界吞噬者，利维坦': '世界吞噬者：普通',
    '利维坦': '利维坦：普通'}


def get_Activities_lowest_accountCount(Activities: list) -> int:
    accountCount = 6
    for j in Activities:
        accountCount = [accountCount, j['accountCount']
                        ][j['accountCount'] < accountCount]
    return accountCount


async def add_raid_data_dict(all_raid_data_dict: dict, single_raid_data_dict: dict):
    activity_hash = single_raid_data_dict['activityHash']
    activity_name_info = await destiny.decode_hash(activity_hash, 'DestinyActivityDefinition')
    activity_name = RAID_NAEM_DICT[activity_name_info['displayProperties']['name']]

    data_values = single_raid_data_dict['values']
    if activity_name in all_raid_data_dict:
        raid_now_dict = all_raid_data_dict[activity_name]
        raid_now_dict['clears'] += data_values['clears']
        raid_now_dict['fullClears'] += data_values['fullClears']
        raid_now_dict['sherpaCount'] += data_values['sherpaCount']
        if 'fastestFullClear' in data_values:
            if not ('fastestFullClear' in raid_now_dict) or (raid_now_dict['fastestFullClear'] > data_values['fastestFullClear']['value']):
                raid_now_dict['fastestFullClear'] = data_values['fastestFullClear']['value']
        if 'bestPlayerCountDetails' in data_values:
            accountCount = data_values['bestPlayerCountDetails']['accountCount']
            if not ('bestPlayerCountDetails' in raid_now_dict) or (accountCount < raid_now_dict['bestPlayerCountDetails']):
                raid_now_dict['bestPlayerCountDetails'] = accountCount
        if 'lowAccountCountActivities' in data_values:
            accountCount = get_Activities_lowest_accountCount(
                data_values['lowAccountCountActivities']
            )
            if not ('lowAccountCountActivities' in raid_now_dict) or (accountCount < raid_now_dict['lowAccountCountActivities']):
                raid_now_dict['lowAccountCountActivities'] = accountCount
        if 'flawlessActivities' in data_values:
            # raid_now_dict['flawlessActivities']
            accountCount = get_Activities_lowest_accountCount(
                data_values['flawlessActivities']
            )
            if not ('flawlessActivities' in raid_now_dict) or (accountCount < raid_now_dict['flawlessActivities']):
                raid_now_dict['flawlessActivities'] = accountCount
    else:
        all_raid_data_dict[activity_name] = {
            'clears': data_values['clears'],
            'fullClears': data_values['fullClears'],
            'sherpaCount': data_values['sherpaCount'],
            'fastestFullClear': data_values['fastestFullClear']['value'] if 'fastestFullClear' in data_values else 0,
        }
        if 'bestPlayerCountDetails' in data_values:
            all_raid_data_dict[activity_name]['bestPlayerCountDetails'] = data_values['bestPlayerCountDetails']['accountCount']
        if 'lowAccountCountActivities' in data_values:
            all_raid_data_dict[activity_name]['lowAccountCountActivities'] = get_Activities_lowest_accountCount(
                data_values['lowAccountCountActivities']
            )
        if 'flawlessActivities' in data_values:
            all_raid_data_dict[activity_name]['flawlessActivities'] = get_Activities_lowest_accountCount(
                data_values['flawlessActivities']
            )


突袭_奇数颜色 = '#292929'
突袭_偶数颜色 = '#1F1F1F'
突袭_奇数背景 = Image.new('RGB', [700, 120], '#292929')
突袭_偶数背景 = Image.new('RGB', [700, 120], '#1F1F1F')

深岩墓室_ = Image.open(f'深岩墓室.png')
救赎花园_ = Image.open(f'救赎花园.png')
最后一愿_ = Image.open(f'最后一愿.png')
忧愁王冠_ = Image.open(f'忧愁王冠.png')
往日之苦_ = Image.open(f'往日之苦.png')
星之塔巅峰_ = Image.open(f'星之塔：巅峰.png')
世界吞噬者巅峰_ = Image.open(f'世界吞噬者：巅峰.png')
利维坦巅峰_ = Image.open(f'利维坦：巅峰.png')
星之塔普通_ = Image.open(f'星之塔：普通.png')
世界吞噬者普通_ = Image.open(f'世界吞噬者：普通.png')
利维坦普通_ = Image.open(f'利维坦：普通.png')
raid双榜图_ = Image.open(f'raid双榜图 (自定义).png')


RAID_IMAGE = {
    '深岩墓室': 深岩墓室_,
    '救赎花园': 救赎花园_,
    '最后一愿': 最后一愿_,
    '忧愁王冠': 忧愁王冠_,
    '往日之苦': 往日之苦_,
    '星之塔：巅峰': 星之塔巅峰_,
    '世界吞噬者：巅峰': 世界吞噬者巅峰_,
    '利维坦：巅峰': 利维坦巅峰_,
    '星之塔：普通': 星之塔普通_,
    '世界吞噬者：普通': 世界吞噬者普通_,
    '利维坦：普通': 利维坦普通_
}

突袭_绿色 = '#31b573'
突袭_蓝色 = '#00709e'
突袭_橙色 = '#f4b757'
突袭_青色 = '#3eb8b4'
_深岩墓室 = ImageFont.truetype('思源黑体B.otf', size=24)
_导师次数 = ImageFont.truetype('思源黑体B.otf', size=16)
_FlawlessDuo = ImageFont.truetype('思源黑体B.otf', size=13)
_段位文字 = ImageFont.truetype('思源黑体B.otf', size=18)

TIER_COLOR = {
    'Challenger': '#FA576F',
    'Master': '#FA576F',
    'Diamond': '#048AB4',
    'Platinum': '#04B1A1',
    'Gold': '#FABC44',
    'Silver': '#9EA3B0',
    'Bronze': '#6A5B3F'
}

RAID_FLAWLESS_DICT = {
    '深岩墓室': '3560923614',
    '救赎花园': '1522774125',
    '最后一愿': '380332968',
    '忧愁王冠': '3292013042',
    '往日之苦': '2925485370',
}


def get_time_text(secondes):
    if secondes > 0:
        m, s = divmod(secondes, 60)
        h, m = divmod(m, 60)
        if h == 0:
            time = f'{m}m {s}s'
        else:
            time = f'{h}h {m}m {s}s'
        return time
    else:
        return '无'


def get_flawless_tag(tag_list: list, records: dict, raidname: str):
    if raidname not in RAID_FLAWLESS_DICT:
        return

    for tag in tag_list:
        if 'Flawless' in tag:
            return

    record_id = RAID_FLAWLESS_DICT[raidname]
    state = records[record_id]['state']
    RecordRedeemed = (state & 1) > 0
    ObjectiveNotCompleted = (state & 4) > 0
    if RecordRedeemed:
        tag_list.append('Flawless')
        return
    if not ObjectiveNotCompleted:
        tag_list.append('Flawless')
        return


@ on_command('突袭', aliases=('raid', 'RAID', 'Raid'), only_to_me=False)
async def get_raid(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900])
        args = info['profile']['data']['userInfo']['displayName']
        records = info['profileRecords']['data']['records']
        membershipid = info['profile']['data']['userInfo']['membershipId']
        url = f'https://b9bv2wd97h.execute-api.us-west-2.amazonaws.com/prod/api/player/{membershipid}'
        async with aiohttp.request("GET", url) as r:
            response = await r.text(encoding="utf-8")
        raid_info = json.loads(response)
        try:
            raid_info = raid_info['response']
        except:
            raise Exception(f'唉...你好像没有打过突袭噢，快跟小伙伴去试试吧！')

        speed_value = get_time_text(raid_info['speedRank']['value'])
        speed_tier = raid_info['speedRank']['tier']
        speed_subtier = raid_info['speedRank']['subtier'] \
            if 'subtier' in raid_info['speedRank'] else ''
        img_speed = Image.new(
            'RGB', [200, 80], TIER_COLOR[speed_tier])
        raid双榜图speed_ = Image.composite(raid双榜图_, Image.new(
            'RGB', raid双榜图_.size, TIER_COLOR[speed_tier]), raid双榜图_)

        clears_value = raid_info['clearsRank']['value']
        clears_tier = raid_info['clearsRank']['tier']
        clears_subtier = raid_info['clearsRank']['subtier'] \
            if 'subtier' in raid_info['clearsRank'] else ''
        img_clears = Image.new(
            'RGB', [200, 80], TIER_COLOR[clears_tier])
        raid双榜图clears_ = Image.composite(raid双榜图_, Image.new(
            'RGB', raid双榜图_.size, TIER_COLOR[clears_tier]), raid双榜图_)

        raid_data_dict = {}
        for i in raid_info['activities']:
            await add_raid_data_dict(raid_data_dict, i)

        raid_data_dict_len = len(raid_data_dict)
        img_raid = Image.new(
            'RGB', [700, 120 + raid_data_dict_len * 120], '#303030')
        draw = ImageDraw.Draw(img_raid)
        draw.text([40, 20], f'小日向Raid查询', '#CCCCCC', _深岩墓室)
        draw.text([40, 65], f'{args}', 'white', _深岩墓室)
        img_raid.paste(img_clears, (260, 20))
        img_raid.paste(img_speed, (480, 20))
        img_raid.paste(raid双榜图clears_, (260, 30))
        img_raid.paste(raid双榜图speed_, (480, 30))

        draw.text([320, 27], f'Full Clears Rank', 'white', _FlawlessDuo)
        draw.text([320, 50], f'{clears_tier} {clears_subtier}', 'white', _段位文字)
        draw.text([320, 75], f'{clears_value}', 'white', _FlawlessDuo)

        draw.text([540, 27], f'Speed Rank', 'white', _FlawlessDuo)
        draw.text([540, 50], f'{speed_tier} {speed_subtier}', 'white', _段位文字)
        draw.text([540, 75], f'{speed_value}', 'white', _FlawlessDuo)

        i = 0
        for raidname in RAID_LIST:
            if raidname not in raid_data_dict:
                continue

            tag_list = []
            raid_now_dict = raid_data_dict[raidname]
            clears = raid_now_dict['clears']
            fullClears = raid_now_dict['fullClears']
            sherpaCount = raid_now_dict['sherpaCount']
            fastestFullClear = get_time_text(raid_now_dict['fastestFullClear'])
            if 'flawlessActivities' in raid_now_dict:
                flawlessActivities = raid_now_dict['flawlessActivities']
            else:
                flawlessActivities = 0

            if 'lowAccountCountActivities' in raid_now_dict:
                lowAccountCountActivities = raid_now_dict['lowAccountCountActivities']
            else:
                lowAccountCountActivities = 0

            if flawlessActivities and lowAccountCountActivities:
                if flawlessActivities == lowAccountCountActivities:
                    tag_list.append(FLAWLESS_DICT[flawlessActivities])
                else:
                    if flawlessActivities:
                        tag_list.append(FLAWLESS_DICT[flawlessActivities])
                    if lowAccountCountActivities:
                        tag_list.append(LOWMAN_DICT[lowAccountCountActivities])
            else:
                if flawlessActivities:
                    tag_list.append(FLAWLESS_DICT[flawlessActivities])
                if lowAccountCountActivities:
                    tag_list.append(LOWMAN_DICT[lowAccountCountActivities])
            get_flawless_tag(tag_list, records, raidname)

            突袭原图片 = RAID_IMAGE[raidname]
            if i % 2 == 0:
                img_raid.paste(突袭_偶数背景, (0, 120 + 120 * i))
                突袭图片 = Image.composite(突袭原图片, Image.new(
                    'RGB', 突袭原图片.size, 突袭_偶数颜色), 突袭原图片)
            else:
                img_raid.paste(突袭_奇数背景, (0, 120 + 120 * i))
                突袭图片 = Image.composite(突袭原图片, Image.new(
                    'RGB', 突袭原图片.size, 突袭_奇数颜色), 突袭原图片)
            img_raid.paste(突袭图片, (10, 10 + 120 + 120 * i))
            draw.text([290, 15 + 120 + 120 * i], f'{raidname}', 'white', _深岩墓室)
            draw.text([290, 2+35+15 + 120 + 120 * i],
                      f'导师：{sherpaCount}次', 突袭_橙色, _导师次数)
            draw.text([290, 30 + 35 + 15 + 120 + 120 * i],
                      f'最快：{fastestFullClear}', 突袭_青色, _导师次数)
            全程次数 = fullClears
            完成次数 = clears
            全程长度 = int(全程次数 / 完成次数 * 200)
            if 全程长度:
                全程 = Image.new('RGB', [全程长度, 10], 突袭_绿色)
                完成 = Image.new('RGB', [200-全程长度, 10], 突袭_蓝色)
                img_raid.paste(全程, (450, 80 + 120 + 120 * i))
                img_raid.paste(完成, (450+全程长度, 80 + 120 + 120 * i))
            else:
                完成 = Image.new('RGB', [200, 10], 突袭_蓝色)
                img_raid.paste(完成, (450, 80 + 120 + 120 * i))
            draw.text([450, 50 + 120 + 120 * i],
                      f'{全程次数} - {完成次数}', '#dadada', _深岩墓室)
            draw.text([575, 95 + 120 + 120 * i], '全程 - 完成', '#dadada', _导师次数)

            height = 5
            for tag in tag_list:
                w, h = _FlawlessDuo.getsize(tag)
                tag颜色 = TAG_COLOR_DICT[tag]
                底色 = Image.new('RGB', [w + 4, h + 4], tag颜色)
                img_raid.paste(底色, (250 - w, height + 15 + 120 + 120 * i))
                draw.text([250 - w+2, height + 15 + 120 + 120 * i+1],
                          f'{tag}', 'white', _FlawlessDuo)
                height += 25
            i += 1

        name = time.time()
        path = os.path.join(os.getcwd(), 'res', 'destiny2',
                            'cache', f'raid_{name}.png')
        img_raid.save(path, 'png')
        append = f'[CQ:image,file=file:///{path}]'
        await session.send(f'{append}', at_sender=False)
    except Exception as err:
        await session.send(f'{err}', at_sender=True)


DUNGEON_NAEM_DICT = {
    '异域任务：前兆: 大师': '前兆: 大师',
    '异域任务：前兆: 普通': '前兆: 普通',
    '先知': '先知',
    '预言': '预言',
    '异端深渊: 普通': '异端深渊',
    '破碎王座': '破碎王座',
    '行动时刻（英雄）': '行动时刻: 英雄',
    '行动时刻': '行动时刻: 普通',
    '冥冥低语（英雄模式）': '冥冥低语: 英雄',
    '冥冥低语': '冥冥低语: 普通'
}

DUNGEON_NAEM_LIST = list(DUNGEON_NAEM_DICT.values())


async def add_dungeon_data_dict(all_dungeon_data_dict, i):
    dungeonHash = i['activityHash']
    dungeonNameInfo = await destiny.decode_hash(dungeonHash, 'DestinyActivityDefinition')
    try:
        dungeonName = DUNGEON_NAEM_DICT[dungeonNameInfo['displayProperties']['name']]
    except Exception as e:
        raise Exception(f'某个数据丢失，请及时联系小日向开发者，感谢🤞\n{e}')
    data_values = i['values']
    if dungeonName in all_dungeon_data_dict:
        dungeon_now_dict = all_dungeon_data_dict[dungeonName]
        dungeon_now_dict['clears'] += data_values['clears']
        dungeon_now_dict['fullClears'] += data_values['fullClears']
        dungeon_now_dict['sherpaCount'] += data_values['sherpaCount']
        if 'fastestFullClear' in data_values:
            if not ('fastestFullClear' in dungeon_now_dict) or (dungeon_now_dict['fastestFullClear'] > data_values['fastestFullClear']['value']):
                dungeon_now_dict['fastestFullClear'] = data_values['fastestFullClear']['value']
        if 'bestPlayerCountDetails' in data_values:
            accountCount = data_values['bestPlayerCountDetails']['accountCount']
            if not ('bestPlayerCountDetails' in dungeon_now_dict) or (accountCount < dungeon_now_dict['bestPlayerCountDetails']):
                dungeon_now_dict['bestPlayerCountDetails'] = accountCount
        if 'lowAccountCountActivities' in data_values:
            accountCount = get_Activities_lowest_accountCount(
                data_values['lowAccountCountActivities']
            )
            if not ('lowAccountCountActivities' in dungeon_now_dict) or (accountCount < dungeon_now_dict['lowAccountCountActivities']):
                dungeon_now_dict['lowAccountCountActivities'] = accountCount
        if 'flawlessActivities' in data_values:
            # dungeon_now_dict['flawlessActivities']
            accountCount = get_Activities_lowest_accountCount(
                data_values['flawlessActivities']
            )
            if not ('flawlessActivities' in dungeon_now_dict) or (accountCount < dungeon_now_dict['flawlessActivities']):
                dungeon_now_dict['flawlessActivities'] = accountCount
    else:
        all_dungeon_data_dict[dungeonName] = {
            'clears': data_values['clears'],
            'fullClears': data_values['fullClears'],
            'sherpaCount': data_values['sherpaCount'],
            'fastestFullClear': data_values['fastestFullClear']['value'] if 'fastestFullClear' in data_values else 0,
        }
        if 'bestPlayerCountDetails' in data_values:
            all_dungeon_data_dict[dungeonName]['bestPlayerCountDetails'] = data_values['bestPlayerCountDetails']['accountCount']
        if 'lowAccountCountActivities' in data_values:
            all_dungeon_data_dict[dungeonName]['lowAccountCountActivities'] = get_Activities_lowest_accountCount(
                data_values['lowAccountCountActivities']
            )
        if 'flawlessActivities' in data_values:
            all_dungeon_data_dict[dungeonName]['flawlessActivities'] = get_Activities_lowest_accountCount(
                data_values['flawlessActivities']
            )


DUNGEON_APPEND_DICT = {
    '异端深渊': {'Solo Flawless': '3950599483',
             'Solo': '3841336511',
             'Flawless': '245952203', },
    '破碎王座': {'Solo Flawless': '3205009787',
             'Solo': '3899996566',
             'Flawless': '1178448425', },
    '先知': {'Solo Flawless': '3047181179',
           'Solo': '3657275647',
           'Flawless': '2902814383'},
    '预言': {'Solo Flawless': '3191784400',
           'Solo': '3002642730',
           'Flawless': '2010041484'},
    '前兆: 大师': {'Flawless': '2335417976'},
    '前兆: 普通': {'Solo Flawless': '4206923617'}
}


def append_method(state: int, typeName: str,tag_list:list):

    RecordRedeemed = (state & 1) > 0
    ObjectiveNotCompleted = (state & 4) > 0
    if RecordRedeemed:
        tag_list.append(typeName)
        return
    if not ObjectiveNotCompleted:
        tag_list.append(typeName)
        return

def dungeon_tag_append(tag_list: list, records: dict, dungeonName: str):
    if dungeonName not in DUNGEON_APPEND_DICT:
        return

    if dungeonName != '先知':
        records = records['profileRecords']['data']['records']
    else:
        characterid = list(records['characterRecords']['data'].keys())
        characterid = characterid[0]
        records = records['characterRecords']['data'][characterid]['records']
    
    
    for tag in tag_list:
        if 'Solo Flawless' in tag:
            return

    for typeName,record_id in DUNGEON_APPEND_DICT[dungeonName].items():
        if typeName == 'Falwless Solo':
            state = records[record_id]['state']
            append_method(state, typeName, tag_list)
            return

        if typeName in tag_list:
            continue
        else:
            state = records[record_id]['state']
            append_method(state, typeName, tag_list)


前兆大师_ = Image.open(f'前兆大师.png')
前兆普通_ = Image.open(f'前兆大师.png')
先知_ = Image.open(f'先知.png')
预言_ = Image.open(f'预言.png')
异端深渊_ = Image.open(f'异端深渊.png')
破碎王座_ = Image.open(f'破碎王座.png')
行动时刻英雄_ = Image.open(f'行动时刻英雄.png')
行动时刻普通_ = Image.open(f'行动时刻英雄.png')
冥冥低语英雄_ = Image.open(f'冥冥低语英雄.png')
冥冥低语普通_ = Image.open(f'冥冥低语英雄.png')


DUNGEON_IMAGE = {
    '前兆: 大师': 前兆大师_,
    '前兆: 普通': 前兆普通_,
    '先知': 先知_,
    '预言': 预言_,
    '异端深渊': 异端深渊_,
    '破碎王座': 破碎王座_,
    '行动时刻: 英雄': 行动时刻英雄_,
    '行动时刻: 普通': 行动时刻普通_,
    '冥冥低语: 英雄': 冥冥低语英雄_,
    '冥冥低语: 普通': 冥冥低语普通_
}



@ on_command('地牢', aliases=('地牢查询'), only_to_me=False)
async def get_player_dungeon_info(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [900])
        args = info['profile']['data']['userInfo']['displayName']
        membershipid = info['profile']['data']['userInfo']['membershipId']
        url = f'https://bolskmfp72.execute-api.us-west-2.amazonaws.com/dungeon/api/player/{membershipid}'
        async with aiohttp.request("GET", url) as r:
            response = await r.text(encoding="utf-8")
        dungeon_raw_data = json.loads(response)
        if 'response' not in dungeon_raw_data:
            raise Exception('获取玩家信息失败，请检查输入的名称或尝试使用队伍码查询')
        if not (dungeon_raw_data := dungeon_raw_data['response']):
            raise Exception('获取玩家信息失败，请检查输入的名称或尝试使用队伍码查询')

        clears_value = dungeon_raw_data['clearsRank']['value']
        clears_tier = dungeon_raw_data['clearsRank']['tier']
        clears_subtier = dungeon_raw_data['clearsRank']['subtier'] \
            if 'subtier' in dungeon_raw_data['clearsRank'] else ''
        img_clears = Image.new(
            'RGB', [200, 80], TIER_COLOR[clears_tier])
        dungeon双榜图clears_ = Image.composite(raid双榜图_, Image.new(
            'RGB', raid双榜图_.size, TIER_COLOR[clears_tier]), raid双榜图_)


        speed_value = get_time_text(dungeon_raw_data['speedRank']['value'])
        speed_tier = dungeon_raw_data['speedRank']['tier']
        speed_subtier = dungeon_raw_data['speedRank']['subtier'] \
            if 'subtier' in dungeon_raw_data['speedRank'] else ''
        img_speed = Image.new(
            'RGB', [200, 80], TIER_COLOR[speed_tier])
        dungeon双榜图speed_ = Image.composite(raid双榜图_, Image.new(
            'RGB', raid双榜图_.size, TIER_COLOR[speed_tier]), raid双榜图_)


        dungeon_data_dict = {}
        for i in dungeon_raw_data['activities']:
            await add_dungeon_data_dict(dungeon_data_dict, i)

        dungeon_dictkeys_to_list = list(dungeon_data_dict.keys())
        dungeon_dict_length = len(dungeon_data_dict)
        img_dungeon = Image.new(
            'RGB', [700, 120 + dungeon_dict_length* 120], '#303030')
        draw = ImageDraw.Draw(img_dungeon)
        draw.text([40, 20], f'小日向地牢查询', '#CCCCCC', _深岩墓室)
        draw.text([40, 65], f'{args}', 'white', _深岩墓室)
        img_dungeon.paste(img_clears, (260, 20))
        img_dungeon.paste(img_speed, (480, 20))
        img_dungeon.paste(dungeon双榜图clears_, (260, 30))
        img_dungeon.paste(dungeon双榜图speed_, (480, 30))

        draw.text([320, 27], f'Full Clears Rank', 'white', _FlawlessDuo)
        draw.text([320, 50], f'{clears_tier} {clears_subtier}', 'white', _段位文字)
        draw.text([320, 75], f'{clears_value}', 'white', _FlawlessDuo)

        draw.text([540, 27], f'Speed Rank', 'white', _FlawlessDuo)
        draw.text([540, 50], f'{speed_tier} {speed_subtier}', 'white', _段位文字)
        draw.text([540, 75], f'{speed_value}', 'white', _FlawlessDuo)


        i = 0
        for dungenonName in DUNGEON_NAEM_LIST:
            if dungenonName not in dungeon_dictkeys_to_list:
                continue
            tag_list = []
            dungeon_now_dict = dungeon_data_dict[dungenonName]
            clears = dungeon_now_dict['clears']
            fullClears = dungeon_now_dict['fullClears']
            sherpaCount = dungeon_now_dict['sherpaCount']
            fastestFullClear = get_time_text(
                dungeon_now_dict['fastestFullClear'])
            if 'flawlessActivities' in dungeon_now_dict:
                flawlessActivities = dungeon_now_dict['flawlessActivities']
            else:
                flawlessActivities = 0

            if 'lowAccountCountActivities' in dungeon_now_dict:
                lowAccountCountActivities = dungeon_now_dict['lowAccountCountActivities']
            else:
                lowAccountCountActivities = 0

            if lowAccountCountActivities == 1 and flawlessActivities == lowAccountCountActivities:
                tag_list.append('Solo Flawless')
            else:
                if flawlessActivities:
                    tag_list.append('Flawless')
                if lowAccountCountActivities == 1:
                    tag_list.append('Solo')
            dungeon_tag_append(tag_list, info, dungenonName)

            地牢原图片 = DUNGEON_IMAGE[dungenonName]

            if i % 2 == 0:
                img_dungeon.paste(突袭_偶数背景, (0, 120 + 120 * i))
                地牢图片 = Image.composite(地牢原图片, Image.new(
                    'RGB', 地牢原图片.size, 突袭_偶数颜色), 地牢原图片)
            else:
                img_dungeon.paste(突袭_奇数背景, (0, 120 + 120 * i))
                地牢图片 = Image.composite(地牢原图片, Image.new(
                    'RGB', 地牢原图片.size, 突袭_奇数颜色), 地牢原图片)
            img_dungeon.paste(地牢图片, (10, 10 + 120 + 120 * i))
            draw.text([290, 15 + 120 + 120 * i],
                      f'{dungenonName}', 'white', _深岩墓室)
            draw.text([290, 2+35+15 + 120 + 120 * i],
                      f'导师：{sherpaCount}次', 突袭_橙色, _导师次数)
            draw.text([290, 30 + 35 + 15 + 120 + 120 * i],
                      f'最快：{fastestFullClear}', 突袭_青色, _导师次数)
            全程次数 = fullClears
            完成次数 = clears
            全程长度 = int(全程次数 / 完成次数 * 200)
            if 全程长度:
                全程 = Image.new('RGB', [全程长度, 10], 突袭_绿色)
                完成 = Image.new('RGB', [200-全程长度, 10], 突袭_蓝色)
                img_dungeon.paste(全程, (450, 80 + 120 + 120 * i))
                img_dungeon.paste(完成, (450+全程长度, 80 + 120 + 120 * i))
            else:
                完成 = Image.new('RGB', [200, 10], 突袭_蓝色)
                img_dungeon.paste(完成, (450, 80 + 120 + 120 * i))
            draw.text([450, 50 + 120 + 120 * i],
                      f'{全程次数} - {完成次数}', '#dadada', _深岩墓室)
            draw.text([575, 95 + 120 + 120 * i], '全程 - 完成', '#dadada', _导师次数)

            height = 5
            for tag in tag_list:
                w, h = _FlawlessDuo.getsize(tag)
                tag颜色 = TAG_COLOR_DICT[tag]
                底色 = Image.new('RGB', [w + 4, h + 4], tag颜色)
                img_dungeon.paste(底色, (250 - w, height + 15 + 120 + 120 * i))
                draw.text([250 - w+2, height + 15 + 120 + 120 * i+1],
                          f'{tag}', 'white', _FlawlessDuo)
                height += 25
            i += 1

        name = time.time()
        path = os.path.join(os.getcwd(), 'res', 'destiny2',
                            'cache', f'dungeon_{name}.png')
        img_dungeon.save(path, 'png')
        append = f'[CQ:image,file=file:///{path}]'
        await session.send(f'{append}', at_sender=False)

    except Exception as e:
        await session.send(f'{e}',at_sender=True)




def Check_zhengzhang(info):
    completionDict = {}
    info_profile = info['profilePresentationNodes']['data']['nodes']
    info_character = info['characterPresentationNodes']['data']

    for name in 证章:
        completionDict[name]={}
        for className in 证章[name]:
            nodeHashNum = str(证章[name][className])
            
            if name == '不朽赛季':
                for characterid in info_character:
                    characterRecords = info_character[characterid]['nodes']
                    if nodeHashNum in characterRecords:
                        progress = characterRecords[nodeHashNum]['objective']['progress']
                        completionValue = characterRecords[nodeHashNum]['objective']['completionValue']
                        completionDict[name][className] = {'progress':progress,'completionValue':completionValue}
                        break


                continue
            
            nodeHash = info_profile[nodeHashNum]
            if 'objective' in nodeHash:
                progress = info_profile[nodeHashNum]['objective']['progress']
                completionValue = info_profile[nodeHashNum]['objective']['completionValue']
            elif 'progressValue' in nodeHash:
                progress = nodeHash['progressValue']
                completionValue = nodeHash['completionValue']

            completionDict[name][className] = {'progress':progress,'completionValue':completionValue}
    return completionDict
            


证章_root = os.path.join(os.getcwd(),'res','destiny2','证章')
标题_证章 = ImageFont.truetype('MYingHeiPRC-W7.ttf',size=20)
名字_证章= ImageFont.truetype('MYingHeiPRC-W7.ttf',size=36)
数字_证章 = ImageFont.truetype('MYingHeiPRC-W7.ttf',size=40)
职业_证章 = ImageFont.truetype('MYingHeiPRC-W7.ttf',size=20)




奇数块_证章 = Image.new('RGB', [900, 160], "#292929")
偶数块_证章 = Image.new('RGB', [900, 160], '#1F1F1F')
镀金 = Image.new('RGB', [168, 104], '#FABC44')


@on_command('证章', only_to_me=False)
async def Check_zhengzhang_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args, [700])
        args = info['profile']['data']['userInfo']['displayName']
        completionDict = Check_zhengzhang(info)
        证章_蓝色 = '#03A9F4'
        证章_红色 = '#E8786E'
        证章图 = Image.new('RGB', [900, 80+21*160], '#303030')
        draw = ImageDraw.Draw(证章图)



        draw.text((40, 20), f'小日向证章查询：{args}',
                    font=名字_证章, fill='white', direction=None)

        nameList = list(completionDict.keys())
        length = len(nameList)
        for i in range(length):
            name = nameList[i]
            completion = completionDict[name]
            证章图_path = os.path.join(证章_root, f'{name}.png')
            img = Image.open(证章图_path)
            

            
            if i % 2 == 0:
                证章图.paste(偶数块_证章, (0, 80+i*160))
            else:
                
                证章图.paste(奇数块_证章, (0, 80+i*160))
            draw.text((40, 10+80+i*160), f'□ {name}', font=标题_证章, fill='white', direction=None)
            
            # img = img.convert('RGBA')
            # x, y = img.size # 获得长和宽
            # for i in range(x):
            #     for k in range(y):
            #         color = img.getpixel((i, k))
            #         color = color[:-1] + (150, )
            #         img.putpixel((i, k), color)
            # 证章图_path = os.path.join(证章_root, f'{name}__.png')
            # img.save(证章图_path,'png')

            


            classList = ['泰坦','猎人','术士']
            Unget = 1
            get = 0
            for j in range(3):
                className = classList[j]
                完成 = completionDict[name][className]['progress']
                总完成 = completionDict[name][className]['completionValue']
                if Unget and 完成==总完成:
                    Unget = 0
                if 完成==总完成:
                    get+=1
                

                完成长度 = int(150*完成/总完成)
                未完成长度 = 150-完成长度
                完成块 = Image.new('RGB', [完成长度, 10], 证章_蓝色)
                未完成块 = Image.new('RGB', [未完成长度, 10], 证章_红色)

                证章图.paste(完成块, (310+j*200, 47 + 120+ 160 * i))
                证章图.paste(未完成块, (310+j*200+完成长度, 47 +120+ 160 * i))
                w,h = 数字_证章.getsize(f'{完成} / {总完成}')
                draw.text((460-w+200*j, 110+ 160 * i), f'{完成} / {总完成}', font=数字_证章, fill='white', direction=None)
                color = '#FFF36D' if 总完成== 完成 else 'white'
                draw.text((460-42+200*j, 65+120+ 160 * i), f'{className}', font=职业_证章, fill=color, direction=None)
            
            if Unget:
                a = np.array(img.convert("L"))
                c = (100/255) *a + 80
                img = Image.fromarray(c.astype('uint8'))
            if get == 3:
                证章图.paste(镀金, (38, 43+80+i*160))

            证章图.paste(img, (40, 45+80+i*160))
        
        name = time.time()
        path = os.path.join(os.getcwd(), 'res', 'destiny2',
                            'cache', f'证章_{name}.png')
        证章图.save(path, 'png')
        append = f'[CQ:image,file=file:///{path}]'
        await session.send(f'{append}', at_sender=False)












    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)
