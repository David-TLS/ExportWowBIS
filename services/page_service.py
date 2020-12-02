from itertools import groupby

import data
from constants import (BisTrackerEnum, ClasseEnum, Global, PhaseEnum,
                       RegexEnum, SlotEnum, SpeEnum, WowHeadEnum,
                       WowIsClassicSpe)
from model import Item, Page
from tools import (FetchHtml, Item, Page, WowIsClassicBisParser, distinct,
                   extractAll, extractSingle, listEnum, log, merge)


class PageService:
    
    # Creates one Page object by WowIsClassic url generated
    # Returns a Page collection with field url and metadata ['itemUrls'] filled as a string
    @staticmethod
    def generateWowIsClassicUrls():
        pages = []
        for phase in listEnum(PhaseEnum):
            url = ''
            for classe in data.classes:
                for spe in data.classes[classe]:
                    if(spe == "all"):
                        # this classe have just once best spo for PVE
                        url = Global.URL_WOW_IS_CLASSIC + classe + '/?phase=' + phase
                    else:
                        # this classe have several spe
                        url = Global.URL_WOW_IS_CLASSIC + classe + '/?phase=' + phase + "&" + 'specialization=' + spe

                    pages.append(Page(url, { 'phase': phase, 'classe': classe, 'spe': spe}))
        return pages

    # Extracts from WowHead html page all items urls to WowHead
    # Returns a Page collection with field metadata ['itemUrls'] filled as array of string
    @staticmethod
    def getWowHeadItemUrls(pages):
        urls = [p.url for p in pages]

        # dowload all html page
        with FetchHtml(urls) as responses:
            for response in responses:
                with WowIsClassicBisParser(response['content']) as urls:

                    # search current page to include all links as metadata
                    page = next(p for p in pages if p.url == response['origin'])

                    # add all WowHead links
                    page.metadata['itemUrls'] = urls

        return pages

    # Extracts informations about all Items from a WoWHead html page
    # Returns a Page collection with field metadata ['items'] filled as an array of Item objects
    @staticmethod
    def getWowHeadItemsInformations(pages):
        lenPages = len(pages)

        for i in range(lenPages):

            page = pages[i]

            log("pages: " + str(i + 1) + '/' + str(lenPages))

            page.metadata['items'] = []

            with FetchHtml(page.metadata['itemUrls']) as responses:
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
                        item.method = extractSingle(RegexEnum.REGEX_LOOT_PNJ_NAME, html)
                        item.type = BisTrackerEnum.BY_KILLING

                    # No drop rate, the item could be loot in several boss in the instance or in quest or world drop or craft by the player or in treasure
                    else: 
                        # extract maybe several location
                        locationIds = extractAll(RegexEnum.REGEX_LOCATION_ID, html)

                        # item is contain in a treasure
                        if (bool(extractSingle(RegexEnum.REGEX_IS_CONTAINED, html))):
                            item.type = BisTrackerEnum.TYPE_BY_TREASURE
                            item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationIds[0]), html)
                            item.method = extractSingle(RegexEnum.REGEX_TREASURE_LOCATION.replace('{locationId}', locationIds[0]), html)
                            item.dropRate = BisTrackerEnum.EMPTY

                        # item have a location
                        elif(bool(locationIds)):
                            locationIds = distinct(locationIds)

                            # item on several boss in the same instance
                            if(len(locationIds) == 1):
                                item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationIds[0]), html)
                                item.type = BisTrackerEnum.BY_KILLING
                                item.method = BisTrackerEnum.METHOD_SEVERAL_BOSSESS
                                item.dropRate = BisTrackerEnum.EMPTY

                            # world drop
                            else:
                                item.location = BisTrackerEnum.TYPE_BY_WORLD_EVENT
                                item.type = BisTrackerEnum.BY_KILLING
                                item.method = BisTrackerEnum.EMPTY
                                item.dropRate = BisTrackerEnum.EMPTY
                        else:
                            profession = extractSingle(RegexEnum.REGEX_PROFESSION, html)

                            # item by craft
                            if(bool(profession)):
                                item.type = BisTrackerEnum.TYPE_BY_PROFESSION.replace('{professionName}', profession.capitalize())
                                item.dropRate = BisTrackerEnum.EMPTY
                                item.method = BisTrackerEnum.EMPTY

                                craftLocation  = extractAll(RegexEnum.REGEX_CRAFT_LOCATION.replace('{itemName}', str(item.name)), html)
                                if(craftLocation):
                                    # item have a sub locationz
                                    if(craftLocation and bool(craftLocation[0][4])):
                                        item.location = craftLocation[0][4]
                                    else:
                                        item.location  = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(craftLocation[0][7])), html)

                            # item by quest
                            else:

                                item.type = BisTrackerEnum.TYPE_BY_QUEST
                                item.dropRate = BisTrackerEnum.EMPTY


                                # extract quest location id  id by group (2 group)
                                locationIds = []
                                extractLocations = extractAll(RegexEnum.REGEX_QUEST_LOCATION_ID, html)
                                if(bool(extractLocations)):
                                    for locationId in extractLocations:
                                        if(locationId[0] == ''):
                                            locationIds.append(locationId[1])
                                        else:
                                            locationIds.append(locationId[0])

                                    # extract quest location name
                                    locations = []
                                    for locationId in locationIds:
                                        location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(locationId)), html)
                                        if(bool(location)):
                                            locations.append(location)
                                            
                                    if(len(locations) > 1):
                                        item.location = ', '.join(locations)
                                    else:
                                        item.location = locations[0]

                                # extract method (quest name)
                                extractMethods = extractAll(RegexEnum.REGEX_QUEST_NAME, html)
                                if(bool(extractMethods)):
                                    methods = distinct(extractMethods)
                                    if(len(methods) > 1):
                                        item.method = ', '.join(methods)
                                    else:
                                        item.method = methods[0]

                    page.metadata['items'].append(item)

        return pages

    # Transforms a collection of Pages into a dictionary that follows the BiSTracker data structure
    # Return a dictionnary
    @staticmethod
    def transformToBiStrackerData(pages):
        dic =  {}
        
        # group page by classe
        key_pages = lambda p: p.metadata['classe']
        sorted_pages = sorted(pages, key = key_pages)
        group_pages = groupby(sorted_pages, key = key_pages)

        for key_pages, pages_classes in group_pages:

            for page in pages_classes:

                name_classe = ClasseEnum(key_pages).name
                name_spe = (WowIsClassicSpe[page.metadata['spe']].value).name
                name_phase = PhaseEnum(page.metadata['phase']).name
                slots = {}

                # create item
                for item in page.metadata['items']:
                    log(name_classe + ' ' + name_spe + ' ' + name_phase + ' :' + item.url)
                    slot = {
                        'itemID' : item.id,
                        'Obtain': {
                            'Zone' : item.location,
                            'Type' : item.type,
                            'Method' : item.method,
                            'Drop' : item.dropRate,
                            'Url' : item.url
                        }
                    }
                    
                    slotName = item.slot.name

                    # case: several ring and trinket
                    if(item.slot in {SlotEnum.Ring, SlotEnum.Trinket}):
                        dic_found = {k: v for k, v in slots.items() if slotName in k}
                        slotName += "2" if len(dic_found) > 0 else "1"

                    # case: classe with ambidexterity
                    if(item.slot in {SlotEnum.MainHand}):
                        dic_found = {k: v for k, v in slots.items() if slotName in k}
                        slotName = SlotEnum.OffHand.name if len(dic_found) > 0 else SlotEnum.MainHand.name

                    slots = merge(slots, {slotName: slot})

                dic = merge(dic, {name_classe: {name_spe: {name_phase: slots}}})

        return dic
