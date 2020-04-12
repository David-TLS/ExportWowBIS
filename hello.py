import json
import logging
from itertools import groupby

import data
from constants import (ClasseEnum, Global, PhaseEnum, RegexEnum, SlotEnum,
                       SpeEnum, TypeEnum, WowHeadEnum, WowIsClassicSpe)
from tools import (FetchHtmls, Item, Page, WowIsClassicBisParser, distinct,
                   extractAll, extractSingle, listEnum, log, merge)

logging.basicConfig(filename='hello.log',level=logging.DEBUG)

# return all urls for all phase/classes/spe
def generatePage():
    pages = []
    for phase in listEnum(PhaseEnum):
        url = ''
        for classe in data.classes:
            for spe in data.classes[classe]:
                if(spe == "all"):
                    #this classe have just once best spo for PVE
                    url = Global.URL_WOW_IS_CLASSIC + classe + '/?phase=' + phase
                else:
                    #this classe have several spe
                    url = Global.URL_WOW_IS_CLASSIC + classe + '/?phase=' + phase + "&" + 'specialization=' + spe

                pages.append(Page(url, { 'phase': phase, 'classe': classe, 'spe': spe}))
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
    lenPages = len(pages)
    for i in range(lenPages):
        page = pages[i]

        log("pages: " + str(i + 1) + '/' + str(lenPages))

        page.metadata['items'] = []
        with FetchHtmls(page.metadata['itemUrls']) as responses:
            for response in responses:
                html = response['content']

                # item global information
                item = Item()
                item.id = extractSingle(RegexEnum.REGEX_ITEM_ID, html)
                item.name = extractSingle(RegexEnum.REGEX_ITEM_NAME.replace('{itemId}', item.id), html)
                item.url = response['origin']
                item.slot = WowHeadEnum[extractSingle(RegexEnum.REGEX_SLOT_ID, html)]
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
                        item.method = extractSingle(RegexEnum.REGEX_TREASURE_LOCATION.replace('{locationId}', locationIds[0]), html)
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
                            item.dropRate = TypeEnum.EMPTY
                            item.method = TypeEnum.EMPTY

                            craftLocation  = extractAll(RegexEnum.REGEX_CRAFT_LOCATION.replace('{itemName}', str(item.name)), html)
                            if(craftLocation):
                                # item have a sub locationz
                                if(craftLocation and bool(craftLocation[0][4])):
                                    item.location = craftLocation[0][4]
                                else:
                                    item.location  = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(craftLocation[0][7])), html)

                        # item by quest
                        else:

                            locationIds = []

                            # get location id by group (2 group)
                            for locationId in extractAll(RegexEnum.REGEX_QUEST_LOCATION_ID, html):
                                if(locationId[0] == ''):
                                    locationIds.append(locationId[1])
                                else:
                                    locationIds.append(locationId[0])
                                    
                            item.type = TypeEnum.TYPE_BY_QUEST
                            item.dropRate = TypeEnum.EMPTY

                            locations = []
                            for locationId in locationIds:
                                location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(locationId)), html)
                                if(bool(location)):
                                    locations.append(location)

                            if(len(locations) > 1):
                                item.location = ', '.join(locations)
                            else:
                                item.location = locations[0]

                            
                            methods = distinct(extractAll(RegexEnum.REGEX_QUEST_NAME, html))
                            
                            if(bool(methods) and len(methods) > 1):
                                item.method = ', '.join(methods)
                            else:
                                item.method = methods[0]

                page.metadata['items'].append(item)
    return pages

def pagesToBistracker(pages):
    dic =  {}
    
    key_pages = lambda p: p.metadata['classe']
    sorted_pages = sorted(pages, key = key_pages)
    group_pages = groupby(sorted_pages, key = key_pages)

    for key_pages, pages_classes in group_pages:

        for page in pages_classes:

            name_classe = ClasseEnum(key_pages).name
            name_spe = (WowIsClassicSpe[page.metadata['spe']].value).name
            name_phase = PhaseEnum(page.metadata['phase']).name
            slots = []

            for item in page.metadata['items']:

                slot = {
                    'itemID' : item.id,
                    'obtain': {
                        'Zone' : item.location,
                        'Type' : item.type,
                        'Method' : item.method,
                        'Drop' : item.dropRate,
                        'Url' : item.url
                    }
                }

                slots.append({item.slot.name: slot})

            dic = merge(dic, {name_classe: {name_spe: {name_phase: slots}}})

    return dic

# log('--start generatePage')
# pages = generatePage()
# log('--end generatePage')

# log('--start extractItemUrls')
# extractItemUrls(pages)
# log('--end extractItemUrls')

# log('--start extractItems')
# extractItems(pages)
# log('--start extractItems')

# log('--start pagesToBistracker')
# extract = pagesToBistracker(pages)
# log('--end pagesToBistracker')

# with open('out.txt', 'w') as f:
#     print(json.dumps(extract), file=f)


# pages = extractItems(
#     extractItemUrls(
#         [
#             Page('https://www.wowisclassic.com/en/best-in-slot/priest/?phase=4&specialization=holy', 
#             { 
#                 'phase': '4',
#                 'classe': 'priest', 
#                 'spe': 'holy'

#             }),
#             Page('https://www.wowisclassic.com/en/best-in-slot/priest/?phase=5&specialization=holy', 
#             { 
#                 'phase': '5',
#                 'classe': 'priest', 
#                 'spe': 'holy'

#             }),
#             Page('https://www.wowisclassic.com/en/best-in-slot/priest/?phase=3&specialization=shadow', 
#             { 
#                 'phase': '3',
#                 'classe': 'priest', 
#                 'spe': 'shadow'

#             }),
#             Page('https://www.wowisclassic.com/en/best-in-slot/warrior/?phase=3&specialization=prot', 
#             { 
#                 'phase': '3',
#                 'classe': 'warrior', 
#                 'spe': 'prot'

#             })
#         ]
#     )
# )
