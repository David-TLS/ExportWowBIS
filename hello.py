import json
from itertools import groupby
from operator import itemgetter

import jsonpickle

import data
from constants import Global, RegexEnum, SlotEnum, TypeEnum
from tools import (FetchHtmls, Item, Page, WowIsClassicBisParser, distinct,
                   extractAll, extractSingle, printGroupedData)


# return all urls for all phase/classes/spe
def generatePage():
    pages = []
    for phase in data.phases:
        url = ''
        for classe in data.classes:
            for spe in data.classes[classe]:
                if(spe == "all"):
                    #this classe have just once best spo for PVE
                    url = Global.URL_WOW_IS_CLASSIC + classe + '/?phase=' + phase
                else:
                    #this classe have several spe
                    url = Global.URL_WOW_IS_CLASSIC + classe + '/?phase=' + phase + "&" + 'specialization=' + spe

                pages.append(Page(url, { 'phase': phase, 'classe': classe, 'spe': spe }))
    return pages

def extractItemUrls(pages):
    urls = [p.url for p in pages]
    with FetchHtmls(urls) as responses:
        for response in responses:
            with WowIsClassicBisParser(response['content']) as urls:
                # search current page to include all links as metadata
                page = next(p for p in pages if p.url == response['origin'])

                page.metadata['itemUrls'] = urls
    return pages

def extractItems(pages):
    for page in pages:
        page.metadata['items'] = []
        with FetchHtmls(page.metadata['itemUrls']) as responses:
            for response in responses:
                html = response['content']

                # item global information
                item = Item()
                item.id = extractSingle(RegexEnum.REGEX_ITEM_ID, html)
                item.name = extractSingle(RegexEnum.REGEX_ITEM_NAME.replace('{itemId}', item.id), html)
                item.url = response['origin']
                item.slot = SlotEnum(int(extractSingle(RegexEnum.REGEX_SLOT_ID, html)))
                item.phase = page.metadata.get('phase', '')
                item.classe = page.metadata.get('classe', '')
                item.spe = page.metadata.get('spe','')

                # extract drop rate
                dropRate = extractSingle(RegexEnum.REGEX_DROP_CHANGE, html)

                # extract item on boss
                if (bool(dropRate)):
                    item.dropRate = dropRate
                    locationId = extractSingle(RegexEnum.REGEX_LOCATION_ID, html)
                    item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationId), html)
                    item.method = TypeEnum.METHOD_KILL.replace('{targetName}', extractSingle(RegexEnum.REGEX_LOOT_PNJ_NAME, html))
                    item.type = TypeEnum.BY_KILLING

                # No drop rate, the item could be loot in several boss in the instance or in quest or world drop or craft by the player or in treasur
                else: 
                    # extract maybe several location
                    locationIds = extractAll(RegexEnum.REGEX_LOCATION_ID, html)

                    # item is contain in a treasure
                    if (bool(extractSingle(RegexEnum.REGEX_IS_CONTAINED, html))):
                        item.type = TypeEnum.TYPE_BY_TREASURE
                        item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationIds[0]), html)
                        item.method = extractSingle(RegexEnum.REGEX_TREASURE_LOCATION.replace('locationId', locationIds[0]), html)
                        item.dropRate = TypeEnum.EMPTY

                    # item have a location
                    elif(bool(locationIds)):
                        locationIds = distinct(locationIds)

                        # item on several boss in the same instance
                        if(len(locationIds) == 1):
                            item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationIds[0]), html)
                            item.type = TypeEnum.BY_KILLING
                            item.method = TypeEnum.METHOD_SEVERAL_BOSSESS
                            item.dropRate = TypeEnum.EMPTY

                        # world drop
                        else:
                            item.location = TypeEnum.TYPE_BY_WORLD_EVENT
                            item.type = TypeEnum.BY_KILLING
                            item.method = TypeEnum.EMPTY
                            item.dropRate = TypeEnum.EMPTY
                    else:
                        profession = extractSingle(RegexEnum.REGEX_PROFESSION, html)

                        # item by craft
                        if(bool(profession)):
                            item.type = TypeEnum.TYPE_BY_PROFESSION.replace('{professionName}', profession.capitalize())
                            craftLocation  = extractAll(RegexEnum.REGEX_CRAFT_LOCATION.replace('{itemName}', str(item.name)), html)[0]
                            item.dropRate = TypeEnum.EMPTY
                            item.method = TypeEnum.EMPTY
                            
                            # item have a sub locationz
                            if(bool(craftLocation[3])):
                                item.location = craftLocation[3]
                            else:
                                item.location  = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(craftLocation[5])), html)

                        # item by quest
                        else:
                            locationId = extractSingle(RegexEnum.REGEX_QUEST_LOCATION_ID, html)
                            item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(locationId)), html)
                            item.type = TypeEnum.TYPE_BY_QUEST
                            item.method = extractSingle(RegexEnum.REGEX_QUEST_NAME, html)
                            item.dropRate = TypeEnum.EMPTY

                page.metadata['items'].append(item)
    return pages

def pagesToBistracker(pages):
    sorted_animals = sorted(pages, key = lambda p: p.metadata['classe'])
    printGroupedData(groupby(sorted_animals, key = lambda p: p.metadata['classe']))


pages = extractItems(extractItemUrls([Page('https://www.wowisclassic.com/en/best-in-slot/priest/?phase=4&specialization=holy', { 'phase': 4, 'classe': 'priest', 'spe': 'holy' })]))
pagesToBistracker(pages)

# print(json.dumps([ob.__dict__ for

#  ob in aaaa]))
    

 
# extract()

# extractItems(['https://classic.wowhead.com/item=19147/ring-of-spell-power'])

# extractItemInformations(['https://classic.wowhead.com/item=18500/tarnished-elven-ring#dropped-by'])
