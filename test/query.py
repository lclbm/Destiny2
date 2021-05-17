import json
import asyncio
import aiohttp

def num2str(num:int)->str:
    return "{:,}".format(num)


def get_season_level_from_records(records):
    seasonLevel = records['1878734479']['intervalObjectives'][3]['progress']
    return num2str(seasonLevel)

def get_mid_height(topY:int,bottomY:int,height:int)->int:
    return int(topY+(bottomY-topY-height)/2)


async def get_dict_from_url(url:str)->dict:
    async with aiohttp.request("GET", url) as r:
        response = await r.text(encoding="utf-8")
        return json.loads(response)
    