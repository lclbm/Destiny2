import os
from nonebot import on_command
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
import sys
import re
sys.path.append('C:/HoshinoBot/hoshino/modules/test')
from data.checklist import PenguinSouvenirs, egg, 增幅,bones,cats
from daily.report import getdailyreport
from data.tie import gethardlink


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

HELP_MSG = f'''目 前 可 公 开 的 情 报：
✨PVP/Pvp/pvp [队伍码/用户名]
💊Raid/raid [队伍码/用户名]
🎐智谋 [队伍码/用户名]
📍地牢 [队伍码/用户名]
🎯ELO [队伍码/用户名]
⚪战绩 [队伍码/用户名]
🎊队伍 [队伍码/用户名]
🏆击杀 [队伍码/用户名] [职业]
🐧企鹅 [队伍码/用户名]
✈增幅 [队伍码/用户名]
🦴骨头 [队伍码/用户名]
🥚蛋/卵 [队伍码/用户名]
🎈绑定功能已开放，输入绑定帮助查看
📣小日向交流群827529117
交流开发/提交问题/购买小日向'''


sv = hoshino.Service('命运2', help_=HELP_MSG)


# ⚪生涯查询 [队伍码/用户名]
# 查询玩家生涯数据
@sv.on_fullmatch(('功能', 'd2', 'D2', '喵内嘎', '喵内', '日向', '小日向', '喵内噶'))
async def D2Help(bot, ev):
    global count
    count += 1
    await bot.send(ev, HELP_MSG)


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





@sv.on_fullmatch(('收费'))
async def D2_say(bot, ev):
    info = f'''⚪3月18日后，小日向1代将停止服务，届时只为付费的群组提供服务。
⚪收费标准如下：
6元/月 35/半年 60/年
群人数≤20价格半价且后续不另收费
如果需要购买请加QQ群827529117
⚪承诺后续更新的内容：
日报、周报、perk、试炼查询（周五前更新）
地牢查询、PVE数据查询
火力战队查询将具体到玩家进行的活动
熔炉具体武器击杀查询（如：稳手、邪东等）
❤感谢大家对小日向的支持'''
    await bot.send(ev, info)


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
                if length == 1 or (length == 2 and response['Response'][0]['membershipId'] == response['Response'][1]['membershipId']):
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


async def GetInfo(args) -> dict:
    global count
    count += 1
    result = await GetMembershipidAndMembershiptype(args)
    membershipid = result['membershipid']
    membershiptype = result['membershiptype_num']
    response = await destiny.api.get_profile(membershiptype, membershipid, [200, 100, 104, 900, 1100, 1000])
    get_success(response, args)
    if len(response['Response']['metrics']) == 1:
        raise Error_Privacy(args)
    response['Response']['membershipid'] = membershipid
    response['Response']['membershiptype_num'] = membershiptype
    response['Response']['membershiptype_char'] = result['membershiptype_char']
    return response['Response']


def get_time_text(secondes):
    if secondes > 0:
        m, s = divmod(secondes, 60)
        h, m = divmod(m, 60)
        if h == 0:
            time = f'{m}m{s}s'
        else:
            time = f'{h}h{m}m{s}s'
        return time
    else:
        return '0m0s'


def get_flawless(i, info):
    dict = {
        '救赎花园': '1522774125',
        '深岩墓室': '3560923614',
        '往日之苦': '2925485370',
        '最后一愿: 等级55': '380332968',
        '忧愁王冠: 普通': '3292013042'}
    if i[0] in dict.keys() and 'objectives' in info['profileRecords']['data']['records'][dict[i[0]]]:
        return info['profileRecords']['data']['records'][dict[i[0]]]['objectives'][0]['complete']
    else:
        return False


@ on_command('突袭', aliases=('raid', 'RAID', 'Raid'), only_to_me=False)
async def GetPlayerProfile(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
        args = info['profile']['data']['userInfo']['displayName']
        membershipid = info['profile']['data']['userInfo']['membershipId']
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
        time = get_time_text(speed_value)
        msg = f'''{args}
🎉【Full Clears Rank】
突袭完成：{clears_value}次 等级：{clears_rank}
🚀【Speed Rank】
完成时间：{time} 等级：{speed_rank}\n'''
# 针对小日向做了较大的更新，输入 d2 返回菜单以查看更新
# 如果数据异常请尝试用队伍码查询'''
        raiddict = {}
        for i in raid['activities']:
            raidname = await destiny.decode_hash(i['activityHash'], 'DestinyActivityDefinition')
            raidname = raidname['displayProperties']['name']
            clears = i['values']['clears']
            full_clears = i['values']['fullClears']
            sherpaCount = i['values']['sherpaCount']
            if 'fastestFullClear' in i['values']:
                time = i['values']['fastestFullClear']['value']
            else:
                time = 0
            if raidname in raiddict.keys():
                raiddict[raidname]['clears'] += clears
                raiddict[raidname]['full_clears'] += full_clears
                raiddict[raidname]['sherpaCount'] += sherpaCount
                if raiddict[raidname]['time'] > time:
                    raiddict[raidname]['time'] = time
            else:
                raiddict[raidname] = {
                    'clears': clears,
                    'full_clears': full_clears,
                    'sherpaCount': sherpaCount,
                    'time': time}
        raid_order = sorted(
            raiddict.items(), key=lambda x: x[1]['clears'], reverse=True)
        namedict = {
            '世界吞噬者，利维坦: 巅峰': '世界吞噬者: 巅峰',
            '世界吞噬者，利维坦: 普通': '世界吞噬者: 普通',
            '忧愁王冠: 普通': '忧愁王冠',
            '最后一愿: 等级55': '最后一愿',
            '最后一愿: 普通': '最后一愿',
            '利维坦，星之塔: 普通': '星之塔: 普通',
            '利维坦，星之塔: 巅峰': '星之塔: 巅峰'
        }
        for i in raid_order:
            raidname = i[0]
            if raidname in namedict.keys():
                raidname = namedict[raidname]
            clears = i[1]['clears']
            # 利维坦，星之塔: 普通
            full_clears = i[1]['full_clears']
            sherpaCount = i[1]['sherpaCount']
            time = get_time_text(i[1]['time'])
            if get_flawless(i, info):
                head = f'💎【{raidname}】'
            else:
                head = f'📕【{raidname}】'
            msg += \
                f'''{head}
🔘{full_clears:^3}/✅{clears:^3}🎓{sherpaCount:^3}次 🚀{time}
'''
        msg += f'#回复d2以查看其他功能\n💎无暇🔘全程✅通关🎓导师🚀最快{AppendInfo}\n❗王冠和往日无暇无法查询'
        await session.send(msg, at_sender=True)
    except Exception as err:
        await session.send(f'{err}', at_sender=True)
    


@ on_command('PVP', aliases=('pvp', 'Pvp'), only_to_me=False)
async def GetPlayerpvp(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        raid = await GetInfo(args)
        args = raid['profile']['data']['userInfo']['displayName']
        raid = raid['metrics']['data']['metrics']
        kill = raid['811894228']['objectiveProgress']['progress']
        reset = raid['3626149776']['objectiveProgress']['progress']
        kda = int(raid['871184140']['objectiveProgress']['progress']) / 100
        valor_now = raid['2872213304']['objectiveProgress']['progress']
        kill_this_season = raid['2935221077']['objectiveProgress']['progress']
        Glory = raid['268448617']['objectiveProgress']['progress']
        msg = f'''{args}
⚪【职业生涯】
击败对手：{kill}人
英勇等级重置：{reset}次
⚪【当前赛季】
KDA：{kda}
生存分：{Glory}
赛季击杀：{kill_this_season}
英勇总分：{valor_now}{AppendInfo}
# 回复d2以查看其他功能'''
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}')


def get_drop(now, localtime):
    temp = now - localtime
    if temp.days >= 365:
        return str(round(temp.days / 365)) + '年前'
    elif temp.days >= 30:
        return str(round(temp.days / 30)) + '月前'
    elif temp.days >= 7:
        return str(round(temp.days / 7)) + '周前'
    elif temp.days >= 1:
        return str(round(temp.days))+'天前'
    elif temp.seconds >= 3600:
        return str(round(temp.seconds/3600)) + '小时前'
    else:
        return str(round(temp.seconds/60)) + '分钟前'


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


@ on_command('战绩', aliases=('查询战绩', '战绩查询'), only_to_me=False)
async def d2_activity(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        res = await GetInfo(args)
        args = res['profile']['data']['userInfo']['displayName']
        msg = args + '\n'
        for characterid in res['characters']['data']:
            json = await destiny.decode_hash(res['characters']['data'][characterid]['classHash'], 'DestinyClassDefinition')
            _class = json['displayProperties']['name']
            re = await destiny.api.get_activity_history(res['profile']['data']['userInfo']['membershipType'], res['profile']['data']['userInfo']['membershipId'], characterid, count=5)
            msg += '⚪' + _class + '⚪' + '\n'
            for times in re['Response']['activities']:
                activityid = times['activityDetails']['directorActivityHash']
                utc = times['period']
                UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
                utcTime = datetime.datetime.strptime(utc, UTC_FORMAT)
                localtime = utcTime + datetime.timedelta(hours=8)
                now = datetime.datetime.now()
                time = get_drop(now, localtime)
                json = await destiny.decode_hash(activityid, 'DestinyActivityDefinition')
                activity = json['displayProperties']['name']
                msg += activity + ' ' + time + ' '
                msg += 'KDA：' + get_kda(times) + '\n'
        msg += f'#回复d2以查看其他功能{AppendInfo}'
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}')


@ sv.on_fullmatch(('状态查询'))
async def D2_condition(bot, ev):
    msg = f'调用次数：{count}'
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


@ on_command('ELO', aliases=('Elo', 'elo'), only_to_me=False)
async def Elo(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetMembershipidAndMembershiptype(args)
        membershipid = info['membershipid']
        membershiptype = info['membershiptype_num']
        url = f'https://api.tracker.gg/api/v2/destiny-2/standard/profile/{membershiptype}/{membershipid}/segments/playlist?season=13'
        async with aiohttp.request("GET", url) as r:
            # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
            response = await r.text(encoding="utf-8")
        info = json.loads(response)
        info = info['data']
        msg = args+'\n'
        checkdict = {"control": "占领",
                     "iron-banner": "铁骑",
                     "pvecomp_gambit": "智谋",
                     "allMayhem": "鏖战",
                     "trials_of_osiris": "试炼",
                     "elimination": "灭绝",
                     "survival": "生存",
                     "clash": "死斗",
                     "rumble": "混战"}
        for i in info:
            mode = checkdict[i['attributes']['playlist']]
            elo = i['stats']['elo']['value']
            # rank = round(100 - i['stats']['elo']['percentile'], 1)
            rank = i['stats']['elo']['percentile']
            if int(rank) <= 60:
                rank = f'👇Rank:后{rank:<4}%'
            else:
                rank = round(100 - rank, 1)
                rank = f'👆Rank:前{rank:<4}%'
            kd = float(i['stats']['kd']['displayValue'])
            if kd > 10:
                kd = round(kd, 1)
            msg += f'🎉{mode}📕 Elo:{elo:<4}\n📏Kd:{kd:^5} {rank:\u3000<11}\n'
        msg += f'#回复d2以查看其他功能{AppendInfo}'
        await session.send(msg, at_sender=True)
    except TypeError:
        await session.send('Tracker服务器繁忙，请两分钟后再试', at_sender=True)
    except FailToGet as e:
        await session.send(f'{e}', at_sender=True)






@ on_command('队伍', aliases=('队伍查询', '火力战队', '找内鬼'), only_to_me=False)
async def getDataFireteam(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
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
                msg += f'🦄 『{name}』\n'
            else:
                msg += f'🐴 『{name}』\n'
            msg += await GetRaidReport(membershipid)
        msg += f'#回复d2以查看其他功能{AppendInfo}'
        await session.send(msg, at_sender=True)
    except Exception as e:
        await session.send(f'{e}', at_sender=True)


@ on_command('保存数据', aliases=('保存'), only_to_me=False)
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


@ on_command('击杀数据', aliases=('击杀', '击杀查询'), only_to_me=False)
async def KillWeaponData(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        if '泰坦' in args or '猎人' in args or '术士' in args:
            if len(args.split(' ')) == 1:
                await session.finish('请按照正确的格式输入指令\n指令样例：击杀 何志武223 术士', at_sender=True)
            if len(args.split(' ')) > 2:
                await session.finish('查询的玩家用户名中有空格，请使用队伍码查询', at_sender=True)
            id = args.split(' ')[0]
            classtype = args.split()[1]
            if classtype != '泰坦' and classtype != '猎人' and classtype != '术士':
                await session.finish(f' {id} ，查询的玩家用户名中有空格，请使用队伍码查询', at_sender=True)
            info = await GetInfo(id)
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
            #args = info['profile']['data']['userInfo']['displayName']
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
                await session.finish(f' {args} 查询失败，请尝试用队伍码查询')
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
            await session.finish(msg, at_sender=True)
        else:
            await session.finish('请输入需要查询的职业\n职业可选：术士/猎人/泰坦\n指令样例：击杀数据 何志武223 术士', at_sender=True)
    except Exception as e:
        await session.send(f'{e}')


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


@ on_command('企鹅查询', aliases=('企鹅', '🐧'), only_to_me=False)
async def Check_Penguin_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
        args = info['profile']['data']['userInfo']['displayName']
        msg = f'{args}【企鹅收集】\n'
        res = msg+Check_Penguin(info)
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
    return head


@ on_command('腐化卵查询', aliases=('孵化卵', '蛋', '卵', '🥚', '腐化卵'), only_to_me=False)
async def Check_egg_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
        args = info['profile']['data']['userInfo']['displayName']
        msg = f'{args}\n【腐化卵🥚收集】\n'
        res = msg+Check_egg(info)
        await session.send(res, at_sender=True)
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


@ on_command('智谋', aliases=('智谋查询', '千谋'), only_to_me=False)
async def gambit_info(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
        args = info['profile']['data']['userInfo']['displayName']
        res = get_gambit(info)
        head = f'{args}\n' + res+'#回复d2以查看其他功能'
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
            print(key)
            msg += 增幅[str(key['objectiveHash'])]['name']+'📍' + \
                增幅[str(key['objectiveHash'])]['location'] + '\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部8个地区的增幅✈啦，你就是木卫二的守护者！\n'
    else:
        head = f'🎐你还差{notget}个地区的增幅✈没收集哦，快看看周报决定去哪获得增幅吧~\n'
    head += msg
    return head


@ on_command('增幅', aliases=(), only_to_me=False)
async def Check_zengfu_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_zengfu(info)
        head = f'{args}\n' + res + '#回复d2以查看其他功能'
        print(head)
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)

dungeondict = {
    1077850348: "预言",
    1099555105: "冥冥低语:英雄",
    1375089621: "异端深渊",
    1738383283: "先知",
    2032534090: "破碎王座",
    2124066889: "前兆:普通",
    2582501063: "异端深渊",
    2731208666: "行动时刻:英雄",
    4148187374: "预言",
    4212753278: "前兆:大师"}


@ on_command('地牢', aliases=('地牢查询'), only_to_me=False)
async def Dungeon(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
        args = info['profile']['data']['userInfo']['displayName']
        membershipid = info['profile']['data']['userInfo']['membershipId']
        url = f'https://bolskmfp72.execute-api.us-west-2.amazonaws.com/dungeon/api/player/{membershipid}'
        async with aiohttp.request("GET", url) as r:
            # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
            response = await r.text(encoding="utf-8")
        dungeon = json.loads(response)
        print(dungeon)
        dungeon = dungeon['response']
        clears = dungeon['clearsRank']
        clears_count = clears['value']
        clear_rank = clears['tier'] + ' ' + \
            clears['subtier'] if 'subtier' in clears else clears['tier']
        speed = dungeon['speedRank']
        speed_count = get_time_text(speed['value'])
        speed_rank = speed['tier'] + ' ' + \
            speed['subtier'] if 'subtier' in speed else speed['tier']
        activities = dungeon['activities']
        head = f'''{args}【地牢查询】
🎉【完成】{clears_count}次 📍{clear_rank}
✨【时间】{speed_count} 🚀{speed_rank}
'''
        temp = '''
🚀【时间】✔🚀🎈🎯✨💎{clears_count}次 📍啊🌠{clears_rank}
'''
        record = {}
        for i in activities:
            hashid = i['activityHash']
            dungeonname = dungeondict[hashid] if hashid in dungeondict else ''
            if not dungeonname:
                continue
            entity = i['values']
            print(entity)
            if dungeonname in record:
                record[dungeonname]['clears'] += entity['clears']
                record[dungeonname]['fullClears'] += entity['fullClears']
                record[dungeonname]['sherpaCount'] += entity['sherpaCount']
                if 'fastestFullClear' in entity:
                    record[dungeonname]['fastestFullClear'] = entity['fastestFullClear']['value'] if entity['fastestFullClear'][
                        'value'] < record[dungeonname]['fastestFullClear'] else record[dungeonname]['fastestFullClear']
                if 'flawlessDetails' in entity:
                    record[dungeonname]['flawlessDetails'] = entity['flawlessDetails']['accountCount'] if entity['flawlessDetails'][
                        'accountCount'] < record[dungeonname]['flawlessDetails'] or record[dungeonname]['flawlessDetails'] == 0 else record[dungeonname]['flawlessDetails']
                if 'bestPlayerCountDetails' in entity:
                    record[dungeonname]['bestPlayerCountDetails'] = entity['bestPlayerCountDetails']['accountCount'] if entity['bestPlayerCountDetails'][
                        'accountCount'] < record[dungeonname]['bestPlayerCountDetails'] or record[dungeonname]['bestPlayerCountDetails'] == 0 else record[dungeonname]['bestPlayerCountDetails']
            else:
                clears = entity['clears']
                fullClears = entity['fullClears']
                sherpaCount = entity['sherpaCount']
                fastestFullClear = entity['fastestFullClear']['value'] if 'fastestFullClear' in entity else 0
                flawlessDetails = entity['flawlessDetails']['accountCount'] if 'flawlessDetails' in entity else 0
                bestPlayerCountDetails = entity['bestPlayerCountDetails'][
                    'accountCount'] if 'bestPlayerCountDetails' in entity else 0
                record[dungeonname] = {'clears': clears, 'fullClears': fullClears,
                                       'sherpaCount': sherpaCount, 'fastestFullClear': fastestFullClear,
                                       'flawlessDetails': flawlessDetails, 'bestPlayerCountDetails': bestPlayerCountDetails}
                
        # 归类完成
        dungeon_order = sorted(
            record.items(), key=lambda x: x[1]['clears'], reverse=True)
        for i in dungeon_order:
            print(i)
            dungeonname = i[0]
            singledict = i[1]
            clears = singledict['clears']
            fullClears = singledict['fullClears']
            sherpaCount = singledict['sherpaCount']
            fastestFullClear = get_time_text(singledict['fastestFullClear'])
            icon1 = '💎'if singledict['flawlessDetails']==1 else '⚪'
            icon2 = '🎉' if singledict['bestPlayerCountDetails'] == 1 else '⚪'
            head += f'''{icon1}{icon2}『{dungeonname}』
        🎯{fullClears:<3}/✅{clears:<3} 🎓{sherpaCount:<2} 🚀{fastestFullClear}\n'''
        head += '💎单人无暇 🎉单人\n#回复d2以查看其他功能\n❗数据暂时有些小问题，请等待修复\n❗数据暂时有些小问题，请等待修复'
        print(head)
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)


def Check_bones(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['1297424116']
    for i in bones:
        if info[i] == False:
            notget+=1
            msg+=bones[i]['name']
            msg+='📍'+bones[i]['location']+'\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部16个阿罕卡拉遗骨🦴啦，你就是行遍幽梦之城的破咒者\n'
    else:
        head = f'🎐你还差{notget}个遗骨🦴没收集哦，顺便去看看这周上维挑战在哪嗷\n'
    head += msg
    return head


@ on_command('骨头', aliases=('🦴'), only_to_me=False)
async def Check_bones_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
        args = info['profile']['data']['userInfo']['displayName']
        res = Check_bones(info)
        head = f'{args}\n' + res
        await session.send(head, at_sender=True)
    except Exception as e:
        await session.send(f'获取失败，{e}', at_sender=True)

def Check_cats(info):
    msg = ''
    notget = 0
    info = info['profileProgression']['data']['checklists']['2726513366']
    for i in cats:
        if info[i] == False:
            notget+=1
            msg+=cats[i]['name']
            msg+='📍'+cats[i]['location']+'\n'
    msg += '#回复d2以查看其他功能'
    if notget == 0:
        head = '🎉你已经收集了全部9只小猫🐱啦，九柱神向你表示感谢\n'
    else:
        head = f'🎐你还差{notget}只小猫🐱没收集哦，下面是它们的位置：\n'
    head += msg
    print(head)
    return head


@ on_command('猫', aliases=('🐱'), only_to_me=False)
async def Check_cats_aync(session):
    try:
        hardlink = gethardlink(session)
        if hardlink:
            args = hardlink
        else:
            args = session.current_arg
        info = await GetInfo(args)
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
#         info = await GetInfo(args)
#         args = info['profile']['data']['userInfo']['displayName']
#         res = Check_chenghao(info)
#         head = f'{args}\n' + res
#         await session.send(head, at_sender=True)
#     except Exception as e:
#         await session.send(f'获取失败，{e}', at_sender=True)



