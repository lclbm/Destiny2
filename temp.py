import json
import pydest
import asyncio
import time
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import datetime

API_KEY = '19a8efe4509a4570bee47bd9883f7d93'
destiny = pydest.Pydest(API_KEY)

黑色 = '#000000'
灰色 = '#818181'
# 黑体 = ImageFont.truetype('simhei.ttf', size=20)
# 标题 = ImageFont.truetype('font1559.ttf', size=30)
# 标题2 = ImageFont.truetype('font1559.ttf', size=24)

模式 = ImageFont.truetype('思源黑体B.otf', size=26)
print(模式.getsize('天选赛季'))
print(模式.getsize('天选赛季'))


# draw = ImageDraw.Draw(img_raw)
# draw.text((86, 6), '钢铁旗帜占领', font=标题, fill=黑色, direction=None)
# draw.text((86, 70), '日落：严酷考验：宗师 · 20分钟前', font=黑体, fill=灰色, direction=None)
# draw.text((328, 30), '用时：1h35min', font=黑体, fill=灰色, direction=None)
# draw.text((500, 20), 'K/D/A', font=标题2, fill=黑色, direction=None)
# draw.text((500, 60), '38/6/2', font=黑体, fill=黑色, direction=None)
# draw.text((600, 20), 'Score', font=标题2, fill=黑色, direction=None)
# draw.text((600, 60), '35', font=黑体, fill=黑色, direction=None)
# img_raw.paste(绿块, (0, 0))

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


classdict = {3655393761: '泰坦', 671679327: '猎人', 2271682572: '术士',
             '泰坦': 3655393761, '猎人': 671679327, '术士': 2271682572}


# 铁骑_字体 = ImageFont.truetype('MYingHeiPRC-W3.ttf', size=24)
# 铁骑_颜色 = '#000000'
# 秋天旗帜_字体 = ImageFont.truetype('MYingHeiPRC-W3.ttf', size=16)
# 秋天旗帜_颜色 = '#A7A7A7'
# 数字_字体 = ImageFont.truetype('数字字体.ttf', size=20)

绿块 = Image.new('RGB', [65, 60], '#3D8D4D')
红块 = Image.new('RGB', [65, 60], '#8F2020')

img_raw = Image.new('RGB', [900, 3000], '#1F1F1F')
标题背景颜色 = '#2A2A2A'
奇数背景颜色 = '#292929'
偶数背景颜色 = '#1F1F1F'


async def main():
    draw = ImageDraw.Draw(img_raw)
    i = 1
    draw.text((70, 2+60*i), f'钢铁旗帜占领', font=铁骑_字体,
              fill=铁骑_颜色, direction=None)
    draw.text((70, 35+60*i), f'秋天旗帜·2小时前',
              font=秋天旗帜_字体, fill=秋天旗帜_颜色, direction=None)
    img_raw.paste(绿块, (0, 0 + 60 * i))
    img_raw.save('02.png', 'png')


    #     draw.text((86, 6+50*i), f'{模式}', font=铁骑_字体,
    #               fill=铁骑_颜色, direction=None)
    #     draw.text((86, 70+50*i), f'{名称} · {时间}',
    #               font=秋天旗帜_字体, fill=秋天旗帜_颜色, direction=None)
    #     draw.text((468, 60+50*i), f'用时：{进行时间}',
    #               font=黑体, fill=黑色, direction=None)
    #     draw.text((468, 30+50*i), f'{activityListToBeUsed[i]["className"]}',
    #               font=黑体, fill=黑色, direction=None)
    #     draw.text((640, 20+50*i), 'K/D/A', font=标题2, fill=黑色, direction=None)
    #     draw.text((640, 60+50*i), f'{K}/{D}/{A}',
    #               font=黑体, fill=黑色, direction=None)
    #     draw.text((740, 20+50*i), 'Score', font=标题2, fill=黑色, direction=None)
    #     draw.text((740, 60+50*i), f'{Score}',
    #               font=黑体, fill=黑色, direction=None)
    #     if 'standing' in activityListToBeUsed[i]['values']:
    #         if activityListToBeUsed[i]['values']['standing']['basic']['displayValue'] == 'Victory':
    #             img_raw.paste(绿块, (0, 0 + 50 * i))
    #         else:
    #             img_raw.paste(红块, (0, 0 + 50 * i))
    #     else:
    #         if activityListToBeUsed[i]['values']['completed']['basic']['displayValue'] == 'Yes':
    #             img_raw.paste(绿块, (0, 0 + 50 * i))
    #         else:
    #             img_raw.paste(红块, (0, 0 + 50 * i))

    # img_raw.save('02.png', 'JPEG')


eloModeDict = {"control": "占领",
               "iron-banner": "铁骑",
               "pvecomp_gambit": "智谋",
               "allMayhem": "鏖战",
               "trials_of_osiris": "试炼",
               "elimination": "灭绝",
               "survival": "生存",
               "clash": "死斗",
               "rumble": "混战"}


async def elo():
    membershiptype = 3
    membershipid = 4611686018500298797
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
        Elo颜色 = eval(i['stats']['elo']['metadata']['rankColor']['value'].replace(
            'rgb(', '').replace(')', ''))
        Elo分 = i['stats']['elo']['displayValue']
        if not (Elo排名 := i['stats']['elo']['rank']):
            Elo排名 = 999999
        if not (Elo排名百分比 := i['stats']['elo']['percentile']):
            Elo排名百分比 = 2
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


async def main2():
    eloDict = await elo()
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
    eloDictLength = len(eloDict)

    img_elo = Image.new('RGB', [1050, 100+eloDictLength*80], '#303030')
    draw = ImageDraw.Draw(img_elo)
    标题块 = Image.new('RGB', [1200, 40], '#3D3D3D')
    img_elo.paste(标题块, (0, 60))
    draw.text((50, 20), f'Elo查询：好吵', font=模式, fill=标题文字, direction=None)
    draw.text((60, 70), f'模式/段位', font=标题, fill=标题文字, direction=None)
    draw.text((300, 70), f'排名', font=标题, fill=标题文字, direction=None)
    draw.text((550, 70), f'K/D', font=标题, fill=标题文字, direction=None)
    draw.text((800, 70), f'胜率 %', font=标题, fill=标题文字, direction=None)
    keysList = list(eloDict.keys())
    for i in range(eloDictLength):
        模式名称 = keysList[i]
        mode = eloDict[模式名称]
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

    # draw.text((468, 30 + 100 * i), f'', font=黑体, fill=黑色, direction=None)
    img_elo.save('elo.png', 'png')


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
    '世界吞噬者，利维坦':'世界吞噬者：普通'}


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
        if raid_now_dict['fastestFullClear'] > data_values['fastestFullClear']['value']:
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


RAID_LIST = ['深岩墓室', '救赎花园', '最后一愿', '忧愁王冠', '往日之苦', '星之塔：巅峰',
             '利维坦：巅峰', '世界吞噬者：巅峰', '星之塔：普通', '世界吞噬者：普通', '利维坦：普通']
FLAWLESS_DICT = {
    6: 'Flawless',
    5: 'Flawless',
    4: 'Flawless',
    3: 'Flawless Trio',
    2: 'Flawless Duo',
    1: 'Flawless Solo'}
LOWMAN_DICT = {
    3: 'Trio',
    2: 'Duo',
    1: 'Solo'}


突袭_奇数颜色 = '#292929'
突袭_偶数颜色 = '#1F1F1F'
突袭_奇数背景 = Image.new('RGB', [700, 120], '#292929')
突袭_偶数背景 = Image.new('RGB', [700, 120], '#1F1F1F')
深岩墓室_ = Image.open(f'深岩墓室.png')
突袭_绿色 = '#31b573'
突袭_蓝色 = '#00709e'
_深岩墓室 = ImageFont.truetype('思源黑体B.otf', size=24)
_导师次数 = ImageFont.truetype('思源黑体B.otf', size=16)
_FlawlessDuo = ImageFont.truetype('思源黑体B.otf', size=13)


async def get_player_raid_info():
    membership_id = 4611686018497181967
    url = f'https://b9bv2wd97h.execute-api.us-west-2.amazonaws.com/prod/api/player/{membership_id}'
    async with aiohttp.request("GET", url) as r:
        response = await r.text(encoding="utf-8")
    raid_info = json.loads(response)
    raid_info = raid_info['response']

    speed_value = raid_info['speedRank']['value']
    speed_tier = raid_info['speedRank']['tier']
    speed_subtier = raid_info['speedRank']['subtier'] \
        if 'subtier' in raid_info['speedRank'] else ''

    clears_value = raid_info['clearsRank']['value']
    clears_tier = raid_info['clearsRank']['tier']
    clears_subtier = raid_info['clearsRank']['subtier'] \
        if 'subtier' in raid_info['clearsRank'] else ''

    raid_data_dict = {}
    for i in raid_info['activities']:
        await add_raid_data_dict(raid_data_dict, i)

    raid_data_dict_len = len(raid_data_dict)
    raid_data_dict_len = 8
    img_raid = Image.new(
        'RGB', [700, 120 + raid_data_dict_len * 120], '#303030')
    draw = ImageDraw.Draw(img_raid)
    for i in range(2):
        if i % 2 == 0:
            img_raid.paste(突袭_偶数背景, (0, 120 + 120 * i))
            突袭图片 = Image.composite(深岩墓室_, Image.new(
                'RGB', 深岩墓室_.size, 突袭_偶数颜色), 深岩墓室_)
        else:
            img_raid.paste(突袭_奇数背景, (0, 120 + 120 * i))
            突袭图片 = Image.composite(深岩墓室_, Image.new(
                'RGB', 深岩墓室_.size, 突袭_奇数颜色), 深岩墓室_)
        img_raid.paste(突袭图片, (10, 10 + 120 + 120 * i))
        draw.text([290, 15 + 120 + 120 * i], '世界吞噬者：普通', 'white', _深岩墓室)
        print(_深岩墓室.getsize('世界吞噬者：普通'))
        draw.text([290, 35+15 + 120 + 120 * i], '导师：5次', 突袭_蓝色, _导师次数)
        print(_导师次数.getsize('导师：5次'))
        draw.text([290, 30 + 35 + 15 + 120 + 120 * i],
                  '最快：53m 59s', 突袭_绿色, _导师次数)
        全程 = 30
        完成 = 40
        全程长度 = int(全程 / (完成+全程) * 200)
        if 全程长度:
            全程 = Image.new('RGB', [全程长度, 10], 突袭_绿色)
            完成 = Image.new('RGB', [200-全程长度, 10], 突袭_蓝色)
            img_raid.paste(全程, (450, 80 + 120 + 120 * i))
            img_raid.paste(完成, (450+全程长度, 80 + 120 + 120 * i))
        else:
            完成 = Image.new('RGB', [200, 10], 突袭_蓝色)
            img_raid.paste(完成, (450, 80 + 120 + 120 * i))
        draw.text([450, 50 + 120 + 120 * i], '35 - 40', '#dadada', _深岩墓室)
        draw.text([575, 95 + 120 + 120 * i], '全程 - 完成', '#dadada', _导师次数)
        tag_list = ['Flawless Trio', 'solo']
        height = 5
        for tag in tag_list:
            w, h = _FlawlessDuo.getsize(tag)
            底色 = Image.new('RGB', [w + 4, h + 4], 突袭_绿色)
            img_raid.paste(底色,(250 - w, height + 15 + 120 + 120 * i))
            draw.text([250 - w+2, height + 15 + 120 + 120 * i+1], f'{tag}', 'white', _FlawlessDuo)
            height += 25

    img_raid.save('raid.png', 'png')

    # for i in RAID_LIST:
    #     if i in raid_data_dict:
    #         tag_list = []
    #         raid_now_dict = raid_data_dict[i]
    #         clears = raid_now_dict['clears']
    #         fullClears = raid_now_dict['fullClears']
    #         sherpaCount = raid_now_dict['sherpaCount']
    #         fastestFullClear = raid_now_dict['fastestFullClear']
    #         if 'flawlessActivities' in raid_now_dict:
    #             flawlessActivities = raid_now_dict['flawlessActivities']
    #         else:
    #             flawlessActivities = 0

    #         if 'lowAccountCountActivities' in raid_now_dict:
    #             lowAccountCountActivities = raid_now_dict['lowAccountCountActivities']
    #         else:
    #             lowAccountCountActivities = 0

    #         if flawlessActivities and lowAccountCountActivities:
    #             if flawlessActivities == lowAccountCountActivities:
    #                 tag_list.append(FLAWLESS_DICT[flawlessActivities])
    #             else:
    #                 tag_list.append(FLAWLESS_DICT[flawlessActivities])
    #                 tag_list.append(LOWMAN_DICT[lowAccountCountActivities])

    # print(66)

async def test_周常():
    milestonesDict = await destiny.api.get_public_milestones()
    milestonesDict = milestonesDict['Response']
    for milestoneHash in milestonesDict:
        # milestoneName = await destiny.api.get_public_milestone_content(milestoneHash)
        milestoneDict = await destiny.decode_hash(milestoneHash,'DestinyMilestoneDefinition')
        milestoneName = milestoneDict['displayProperties']['name']
        milestoneDescription = milestoneDict['displayProperties']['description']
        # milestoneName = await destiny.api.get_milestone_definitions(milestoneHash)
        print(milestoneHash,milestoneName,milestoneDescription)

    print(66)




async def zhanji():
    activityList = []
    res = await destiny.api.get_profile(3, 4611686018497181967, [100, 200])
    characters = res['Response']['characters']['data']
    characterIdList = list(characters.keys())
    for characterId in characterIdList:
        className = classdict[characters[characterId]['classHash']]
        activities = await destiny.api.get_activity_history(3, 4611686018497181967, characterId, 50,mode=None)
        activities = activities['Response']['activities']
        for i in activities:
            i['characterId'] = characterId
            i['className'] = className
        activityList.extend(activities)
        
    activityList_order = sorted(
        activityList, key=lambda x: x['period'], reverse=True)
    activityListToBeUsed = activityList_order[:50]

    for i in range(30):
        activitiy = activityListToBeUsed[i]
        res = await destiny.decode_hash(activitiy['activityDetails']['directorActivityHash'], 'DestinyActivityDefinition')
        res2 = await destiny.decode_hash(activitiy['activityDetails']['referenceId'], 'DestinyActivityDefinition')
        modeNum = activitiy['activityDetails']['modes']
        模式 = res['displayProperties']['name']
        名称 = res2['displayProperties']['name']
        时间 = get_activity_time(activitiy['period'])
        K = activitiy['values']['kills']['basic']['displayValue']
        D = activitiy['values']['deaths']['basic']['displayValue']
        A = activitiy['values']['assists']['basic']['displayValue']
        KD = activitiy['values']['killsDeathsRatio']['basic']['displayValue']
        进行时间 = activitiy['values']['activityDurationSeconds']['basic']['displayValue']
        Score = activitiy['values']['score']['basic']['displayValue']















loop = asyncio.get_event_loop()
loop.run_until_complete(zhanji())
loop.close()
