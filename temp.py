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
黑体 = ImageFont.truetype('simhei.ttf', size=20)
标题 = ImageFont.truetype('font1559.ttf', size=30)
标题2 = ImageFont.truetype('font1559.ttf', size=24)
绿块 = Image.new('RGB', [67, 100], '#00b034')
红块 = Image.new('RGB', [67, 100], (229, 115, 125))

img_raw = Image.new('RGB', [900, 3000], 'White')

# draw = ImageDraw.Draw(img_raw)
# draw.text((86, 6), '钢铁旗帜占领', font=标题, fill=黑色, direction=None)
# draw.text((86, 70), '日落：严酷考验：宗师 · 20分钟前', font=黑体, fill=灰色, direction=None)
# draw.text((328, 30), '用时：1h35min', font=黑体, fill=灰色, direction=None)
# draw.text((500, 20), 'K/D/A', font=标题2, fill=黑色, direction=None)
# draw.text((500, 60), '38/6/2', font=黑体, fill=黑色, direction=None)
# draw.text((600, 20), 'Score', font=标题2, fill=黑色, direction=None)
# draw.text((600, 60), '35', font=黑体, fill=黑色, direction=None)
# img_raw.paste(绿块, (0, 0))


# img_raw.save('01.png', 'JPEG')


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


async def main():
    activityList = []
    res = await destiny.api.get_profile(3, 4611686018490361735, [100, 200])
    characters = res['Response']['characters']['data']
    characterIdList = list(characters.keys())
    for characterId in characterIdList:
        className = classdict[characters[characterId]['classHash']]
        activities = await destiny.api.get_activity_history(3, 4611686018490361735, characterId, 30)
        activities = activities['Response']['activities']
        for i in activities:
            i['characterId'] = characterId
            i['className'] = className
        activityList.extend(activities)
    activityList_order = sorted(
        activityList, key=lambda x: x['period'], reverse=True)
    activityListToBeUsed = activityList_order[:30]
    draw = ImageDraw.Draw(img_raw)
    for i in range(30):
        res = await destiny.decode_hash(activityListToBeUsed[i]['activityDetails']['directorActivityHash'], 'DestinyActivityDefinition')
        res2 = await destiny.decode_hash(activityListToBeUsed[i]['activityDetails']['referenceId'], 'DestinyActivityDefinition')
        模式 = res['displayProperties']['name']
        名称 = res2['displayProperties']['name']
        时间 = get_activity_time(activityListToBeUsed[i]['period'])
        K = activityListToBeUsed[i]['values']['kills']['basic']['displayValue']
        D = activityListToBeUsed[i]['values']['deaths']['basic']['displayValue']
        A = activityListToBeUsed[i]['values']['assists']['basic']['displayValue']
        进行时间 = activityListToBeUsed[i]['values']['activityDurationSeconds']['basic']['displayValue']
        Score = activityListToBeUsed[i]['values']['score']['basic']['displayValue']

        draw.text((86, 6+100*i), f'{模式}', font=标题, fill=黑色, direction=None)
        draw.text((86, 70+100*i), f'{名称} · {时间}',
                  font=黑体, fill=灰色, direction=None)
        draw.text((468, 60+100*i), f'用时：{进行时间}',
                  font=黑体, fill=黑色, direction=None)
        draw.text((468, 30+100*i), f'{activityListToBeUsed[i]["className"]}',
                  font=黑体, fill=黑色, direction=None)
        draw.text((640, 20+100*i), 'K/D/A', font=标题2, fill=黑色, direction=None)
        draw.text((640, 60+100*i), f'{K}/{D}/{A}',
                  font=黑体, fill=黑色, direction=None)
        draw.text((740, 20+100*i), 'Score', font=标题2, fill=黑色, direction=None)
        draw.text((740, 60+100*i), f'{Score}',
                  font=黑体, fill=黑色, direction=None)
        if 'standing' in activityListToBeUsed[i]['values']:
            if activityListToBeUsed[i]['values']['standing']['basic']['displayValue'] == 'Victory':
                img_raw.paste(绿块, (0, 0 + 100 * i))
            else:
                img_raw.paste(红块, (0, 0 + 100 * i))
        else:
            if activityListToBeUsed[i]['values']['completed']['basic']['displayValue'] == 'Yes':
                img_raw.paste(绿块, (0, 0 + 100 * i))
            else:
                img_raw.paste(红块, (0, 0 + 100 * i))

    img_raw.save('02.png', 'JPEG')


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
    membershipid = 4611686018501803275
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


loop = asyncio.get_event_loop()
loop.run_until_complete(main2())
loop.close()
