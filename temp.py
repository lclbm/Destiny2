import json
import pydest
import asyncio
import time
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

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
