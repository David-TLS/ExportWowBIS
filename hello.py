from constants import RegexEnum, SlotEnum, TypeEnum
from tools import (
    Classe, FetchHtmls, Item, Phase, Spe, WowIsClassicBisParser, distinct,
    extractAll, extractSingle)


def extractItemUrls():
    with FetchHtmls(['https://www.wowisclassic.com/en/best-in-slot/rogue/?phase=1&specialization=sword']) as wicPages:
        for wicPage in wicPages:
            with WowIsClassicBisParser(wicPage) as urls:
                return urls 

def extractItemInformations(urls):
    items = []
    with FetchHtmls(urls) as cwhPages:
        for cwhPage in cwhPages:
            item = Item()

            # extract id and name
            item.id = extractSingle(RegexEnum.REGEX_ITEM_ID, cwhPage)
            item.name = extractSingle(RegexEnum.REGEX_ITEM_NAME.replace('{itemId}', item.id), cwhPage)
            item.slot = SlotEnum(int(extractSingle(RegexEnum.REGEX_SLOT_ID, cwhPage)))
            # extract drop rate
            dropRate = extractSingle(RegexEnum.REGEX_DROP_CHANGE, cwhPage)

            # extract item on boss
            if (bool(dropRate)):
                item.dropRate = dropRate
                locationId = extractSingle(RegexEnum.REGEX_LOCATION_ID, cwhPage)
                item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationId), cwhPage)
                item.method = TypeEnum.METHOD_KILL.replace('{targetName}', extractSingle(RegexEnum.REGEX_LOOT_PNJ_NAME, cwhPage))
                item.type = TypeEnum.BY_KILLING

            # No drop rate, the item could be loot in several boss in the instance or in quest or world drop or craft by the player
            else:
                             
                # extract maybe several location
                locationIds = extractAll(RegexEnum.REGEX_LOCATION_ID, cwhPage)

                # item is contain in a treasure
                if (bool(extractSingle(RegexEnum.REGEX_IS_CONTAINED, cwhPage))):
                    item.type = TypeEnum.TYPE_BY_TREASURE
                    item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationIds[0]), cwhPage)
                    item.method = extractSingle(RegexEnum.REGEX_TREASURE_LOCATION.replace('locationId', locationIds[0]), cwhPage)
                    item.dropRate = TypeEnum.EMPTY

                # item have a location
                elif(bool(locationIds)):
                    locationIds = distinct(locationIds)

                    # item on several boss in the same instance
                    if(len(locationIds) == 1):
                        item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', locationIds[0]), cwhPage)
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
                    profession = extractSingle(RegexEnum.REGEX_PROFESSION, cwhPage)

                    # item by craft
                    if(bool(profession)):
                        item.type = TypeEnum.TYPE_BY_PROFESSION.replace('{professionName}', profession.capitalize())
                        craftLocation  = extractAll(RegexEnum.REGEX_CRAFT_LOCATION.replace('{itemName}', str(item.name)), cwhPage)[0]
                        item.dropRate = TypeEnum.EMPTY
                        item.method = TypeEnum.EMPTY
                        
                        # item have a sub locationz
                        if(bool(craftLocation[3])):
                            item.location = craftLocation[3]
                        else:
                            item.location  = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(craftLocation[5])), cwhPage)

                    # item by quest
                    else:
                        locationId = extractSingle(RegexEnum.REGEX_QUEST_LOCATION_ID, cwhPage)
                        item.location = extractSingle(RegexEnum.REGEX_LOCATION_NAME.replace('{locationId}', str(locationId)), cwhPage)
                        item.type = TypeEnum.TYPE_BY_QUEST
                        item.method = extractSingle(RegexEnum.REGEX_QUEST_NAME, cwhPage)
                        item.dropRate = TypeEnum.EMPTY

            items.append(item)
        return items

def extract():
    urls = extractItemUrls()
    items = extractItemInformations(urls)

 
# extract()

# extractItems(['https://classic.wowhead.com/item=19147/ring-of-spell-power'])

# extractItemInformations(['https://classic.wowhead.com/item=18500/tarnished-elven-ring#dropped-by'])
