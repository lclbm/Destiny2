import json
import pydest
import asyncio
import time
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import datetime

API_KEY = '19a8efe4509a4570bee47bd9883f7d93'
destiny = pydest.Pydest(API_KEY)


TIER_COLOR = {
    'Challenger': '#FA576F',
    'Diamond': '#048AB4',
    'Platinum': '#04B1A1',
    'Gold': '#FABC44',
    'Silver': '#9EA3B0'
}

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

def get_Activities_lowest_accountCount(Activities: list) -> int:
    accountCount = 6
    for j in Activities:
        accountCount = [accountCount, j['accountCount']
                        ][j['accountCount'] < accountCount]
    return accountCount


async def add_dungeon_data_dict(all_dungeon_data_dict, i):
    dungeonHash = i['activityHash']
    dungeonNameInfo = await destiny.decode_hash(dungeonHash, 'DestinyActivityDefinition')
    try:
        dungeonName = DUNGEON_NAEM_DICT[dungeonNameInfo['displayProperties']['name']]
    except Exception as e:
        raise Exception('某个数据丢失，请及时联系小日向开发者，感谢🤞\n{e}')
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


async def get_player_dungeon_info():
    membershipid = 4611686018508764748
    url = f'https://bolskmfp72.execute-api.us-west-2.amazonaws.com/dungeon/api/player/{membershipid}'
    async with aiohttp.request("GET", url) as r:
        response = await r.text(encoding="utf-8")
    dungeon_raw_data = json.loads(response)
    if not (dungeon_raw_data := dungeon_raw_data['response']):
        raise Exception('获取玩家信息失败')

    clears_value = dungeon_raw_data['clearsRank']['value']
    clears_tier = dungeon_raw_data['clearsRank']['tier']
    clears_subtier = dungeon_raw_data['clearsRank']['subtier'] \
        if 'subtier' in dungeon_raw_data['clearsRank'] else ''

    speed_value = get_time_text(dungeon_raw_data['speedRank']['value'])
    speed_tier = dungeon_raw_data['speedRank']['tier']
    speed_subtier = dungeon_raw_data['speedRank']['subtier'] \
        if 'subtier' in dungeon_raw_data['speedRank'] else ''

    dungeon_data_dict = {}
    for i in dungeon_raw_data['activities']:
        await add_dungeon_data_dict(dungeon_data_dict, i)

    dungeon_dict_length = len(dungeon_data_dict)
    
    for dungenonName in dungeon_data_dict:
        tag_list = []
        dungeon_now_dict = dungeon_data_dict[dungenonName]
        clears = dungeon_now_dict['clears']
        fullClears = dungeon_now_dict['fullClears']
        sherpaCount = dungeon_now_dict['sherpaCount']
        fastestFullClear = get_time_text(dungeon_now_dict['fastestFullClear'])
        if 'flawlessActivities' in dungeon_now_dict:
            flawlessActivities = dungeon_now_dict['flawlessActivities']
        else:
            flawlessActivities = 0

        if 'lowAccountCountActivities' in dungeon_now_dict:
            lowAccountCountActivities = dungeon_now_dict['lowAccountCountActivities']
        else:
            lowAccountCountActivities = 0

        if lowAccountCountActivities==1 and flawlessActivities == lowAccountCountActivities:
            tag_list.append('Flawless Solo')
        else:
            if flawlessActivities:
                tag_list.append('Flawless')
            if lowAccountCountActivities == 1:
                tag_list.append('Solo')
        print(dungenonName,tag_list)

        # get_tag_append(tag_list,records,raidname)




    print(66)


loop = asyncio.get_event_loop()
loop.run_until_complete(get_player_dungeon_info())
loop.close()
