import json
import asyncio
from typing import Dict, Tuple
import aiohttp
from weekly_milestones import destiny
import os
import copy
import numpy as np
from PIL import Image, ImageDraw, ImageFont



def read_json(file):
    dict_temp = {}
    try:
        with open(file, 'r', encoding='utf-8') as f:
            dict_temp = json.load(f)
            return dict_temp
    except:
        return dict_temp

def write_json(dict_temp, path):
    with open(path, 'w', encoding='utf-8') as f:
        # 设置不转换成ascii  json字符串首缩进
        f.write(json.dumps(dict_temp, ensure_ascii=False, indent=2))




def num2str(num: int) -> str:
    return "{:,}".format(num)


def get_season_level_from_records(records):
    seasonLevel = records['1878734479']['intervalObjectives'][3]['progress']
    return num2str(seasonLevel)


def get_mid_height(topY: int, bottomY: int, height: int) -> int:
    return int(topY+(bottomY-topY-height)/2)


async def get_dict_from_url(url: str) -> dict:
    async with aiohttp.request("GET", url) as r:
        response = await r.text(encoding="utf-8")
        return json.loads(response)


async def dowload_img(url, path):
    if os.path.exists(path):
        return

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        content = await response.read()
    with open(path, 'wb') as f:
        f.write(content)


def seconds_to_hours(seconds: int) -> float:
    return int(seconds/3600*10)/10


def get_grey_img(img):
    a = np.array(img.convert("L"))
    c = (100/255) * a + 80
    img = Image.fromarray(c.astype('uint8'))
    return img


async def get_activitiesModeTime_dict(membershipType, membershipId, characterId):
    print('start')
    timeDict = {'crucible': 0,
                'gambit': 0,
                'raid': 0,
                'story': 0,
                'strikes': 0,
                'total': 0}
    page = 0
    while 1:
        res = await destiny.api.get_activity_history(membershipType, membershipId, characterId, count=250, mode=None,page=page)
        try:
            res = res['Response']['activities']
        except:
            res = []
        #熔炉 剧情
        for activity in res:
            modes = activity['activityDetails']['modes']
            seconds = activity['values']['timePlayedSeconds']['basic']['value']
            if 18 in modes:
                timeDict['strikes'] += seconds
            elif 4 in modes:
                timeDict['raid'] += seconds
            elif 5 in modes or 32 in modes :
                timeDict['crucible'] += seconds
            elif 64 in modes:
                timeDict['gambit'] += seconds
            else:
                timeDict['story'] += seconds

        if len(res) < 250:
            
            timeDict['total'] += timeDict['story'] + timeDict['strikes'] + \
                timeDict['raid'] + timeDict['crucible']+timeDict['gambit']
            print(timeDict)
            break
        page += 1
    return timeDict

seasonsAndYearsDict = {
    '年三': {1743682818: '不朽赛季', 1743682819: '黎明赛季', 2809059425: '英杰赛季', 2809059424: '影临赛季'},
    '年四': {2809059427: '狂猎赛季', 2809059426: '天选赛季', 2809059429: '永夜赛季'}
}

classDict = {3655393761: '泰坦', 671679327: '猎人', 2271682572: '术士',
             '泰坦': 3655393761, '猎人': 671679327, '术士': 2271682572}

activitiesDictUrl = 'https://api.wastedondestiny.com/activities?membershipType={}&membershipId={}&gameVersion=2'
timeDictUrl = 'https://api.wastedondestiny.com/breakdown?membershipType={}&membershipId={}&gameVersion=2&characterId={}&page={}'


basicDataNameToImgName = {'传承成就分': '账户banner',
                          '当前成就分': '账户banner',
                          '熔炉胜场': '熔炉banner',
                          '智谋胜场': '智谋banner',
                          '打击列表场次': '打击banner',
                          '公会经验值': '账户banner'}

# basicDataNameToImgColor = {'传承成就分': '#454545',
#                           '当前成就分': '#C6C6C6',
#                           '熔炉胜场': '#C9352E',
#                           '智谋胜场': '#4B997F',
#                           '打击列表场次': '#606DB2',
#                           '公会经验值': '账户banner'}


basicDataNameToImgColor = {'传承成就分': '#E7D1AC',
                           '当前成就分': '#DEA089',
                           '熔炉胜场': '#D46D68',
                           '智谋胜场': '#84A091',
                           '打击列表场次': '#4D809D',
                           '公会经验值': '账户banner'}


modeColorDict = {
    '熔炉': '#FF5D39',
    '智谋': '#239A72',
    '突袭': '#7F54A2',
    '打击': '#545F9C',
    '剧情': '#DCCE58', }


async def get_shengya_data(records: dict, profile: dict, charactersDict: dict, membershipType, membershipId) -> tuple:
    """
    检索玩家的生涯数据，并返回一些处理好的dict数据类型

    Args:
        records (dict): 
                    getProfile - 900
        profile (dict): 
                    getProfile - 100
        characterDict (dict): 
                    getProfile - 200
        membershipType ([int,str]):
                    类型
        membershipId ([int,str]):
                    id

    Returns:
        返回玩家tuple数据，包含:
            basicDataToReturn (dict):
                            一些基本的生涯数据
            seasonsDictToReturn (dict):
                            玩家赛季历程(bool)
            activitiesTimeToReturn (dict):
                            最近15天每日活动时间(小时)
            characterTimeDictToReturn (dict):
                            每个职业每个模式的活动时长(小时)
    """

    profileRecordsData = records['data']
    userInfo = profile['data']
    传承成就分 = profileRecordsData['legacyScore']
    当前成就分 = profileRecordsData['activeScore']
    熔炉胜场 = profileRecordsData['records']['3561485187']['intervalObjectives'][0]['progress']
    智谋胜场 = profileRecordsData['records']['1676011372']['objectives'][0]['progress'] + \
        profileRecordsData['records']['2129704137']['objectives'][0]['progress'] + \
        profileRecordsData['records']['89114360']['objectives'][0]['progress']
    打击列表 = profileRecordsData['records']['2780814366']['objectives'][2]['progress']
    公会经验值 = profileRecordsData['records']['2505589392']['intervalObjectives'][0]['progress']

    basicDataToReturn = {
        '当前成就分': num2str(当前成就分),
        '传承成就分': num2str(传承成就分),
        '熔炉胜场': num2str(熔炉胜场),
        '智谋胜场': num2str(智谋胜场),
        '打击列表场次': num2str(打击列表),
        # '公会经验值': num2str(公会经验值),
    }

    seasonHashes = userInfo['seasonHashes']
    seasonsDictToReturn = {}
    for yearName in seasonsAndYearsDict:
        seasonsDictToReturn[yearName] = {}
        seasonsDict = seasonsAndYearsDict[yearName]
        for seasonHash in seasonsDict:
            seasonName = seasonsDict[seasonHash]
            if seasonHash in seasonHashes:
                seasonsDictToReturn[yearName][seasonName] = True
            else:
                seasonsDictToReturn[yearName][seasonName] = False

    activities = await get_dict_from_url(activitiesDictUrl.format(membershipType, membershipId))
    activitiesTimeToReturn = {'response': {},
                              'max': 0.0, 'min': 0.0, 'total': 0.0}

    for key in activities['response'].keys():
        # return Hour
        max = activitiesTimeToReturn['max']
        min = activitiesTimeToReturn['min']
        hours = seconds_to_hours(activities['response'][key])
        activitiesTimeToReturn['total'] += hours
        activitiesTimeToReturn['response'][key] = hours
        max = max if max > hours else hours
        min = min if min < hours else hours
        activitiesTimeToReturn['max'] = max
        activitiesTimeToReturn['min'] = min

    characterTimeDictToReturn = {}

    characterTimeDictToReturn['综合'] = {
        '熔炉': 0,
        '智谋': 0,
        '突袭': 0,
        '剧情': 0,
        '打击': 0,
        '总计': 0
    }
    for characterId in charactersDict:
        className = classDict[charactersDict[characterId]['classHash']]
        characterTimeDictToReturn[className] = {
            '熔炉': 0,
            '智谋': 0,
            '突袭': 0,
            '剧情': 0,
            '打击': 0,
            '总计': 0
        }

        timeDict = await get_activitiesModeTime_dict(membershipType, membershipId, characterId)
        print(timeDict)
        characterTimeDictToReturn[className]['熔炉'] = timeDict['crucible']
        characterTimeDictToReturn[className]['智谋'] = timeDict['gambit']
        characterTimeDictToReturn[className]['突袭'] = timeDict['raid']
        characterTimeDictToReturn[className]['剧情'] = timeDict['story']
        characterTimeDictToReturn[className]['打击'] = timeDict['strikes']
        characterTimeDictToReturn[className]['总计'] = timeDict['total']



        
    for value in characterTimeDictToReturn.values():
        for mode in value:
            seconds = value[mode]
            characterTimeDictToReturn['综合'][mode] += seconds
            value[mode] = seconds_to_hours(seconds)

    for mode in characterTimeDictToReturn['综合']:
        seconds = characterTimeDictToReturn['综合'][mode]
        characterTimeDictToReturn['综合'][mode] = seconds_to_hours(seconds)

    return basicDataToReturn, seasonsDictToReturn, activitiesTimeToReturn, characterTimeDictToReturn

