# REGEX_EXTRACT_JSON = "{(?:[^{}]|(?R))*\}"
# REGEX_IS_DROPPED = "(?:id)(.*?)(?:'dropped-by')"
# REGEX_COUNT_OUTOF = '(?<="count":)(.*?)(?=,)(.*?)(?<="outof":)(.*?)(?=,)'
from enum import Enum


class RegexEnum():
    REGEX_BIS_WOWHEAD_LINK = '(?<=item=)(.*)'
    REGEX_ITEM_ID = '(?<=item=)(.*?)(?=\/)'
    REGEX_ITEM_NAME = '(?<=typeId: {itemId}, name: ")(.*?)(?=")'
    REGEX_DROP_CHANGE = '(?<=Drop Chance:)(.*%)'
    REGEX_LOCATION_ID = '(?<=location":\[)(.*?)(?=\])'
    REGEX_LOCATION_NAME = '(?<=\[{locationId},")(.*?)(?="\])'
    REGEX_LOOT_PNJ_NAME = '(?<=Dropped by: )(.*?)(?=\<)'
    REGEX_CREATED_BY = 'created-ny'
    REGEX_PROFESSION = '(?<=guides\/)(.*?)(?=-classic-wow-1-300)'
    REGEX_QUEST_NAME = '(?<="name":")(.*)(?=","reprewards":)'
    REGEX_QUEST_LOCATION_ID = '(?<=data: \[{"category":)(.*?)(?=,")'
    REGEX_CRAFT_LOCATION = '("name":"Pattern: {itemName}")((.*)(?<="n":")(.*)(?=",))?(.*)(?<="z":)(.*?)(?=})(.*)'
    REGEX_SLOT_ID = '(?<=,"slot":)(.*?)(?=,"slotbak)'
    REGEX_IS_CONTAINED = 'id: \'contained-in-object\''
    REGEX_TREASURE_LOCATION ='(?<=location":\[locationId\],"name":")(.*?)(?=")'

class AttributeEnum():
    DATA_WH_ICON_SIZE = 'data-wh-icon-size'


class TypeEnum():
    BY_KILLING = "By Killing"
    TYPE_BY_PROFESSION = "by Profession ({professionName})"
    TYPE_BY_QUEST = "By Quest"
    TYPE_BY_TREASURE = "By Treasure"
    TYPE_BY_WORLD_EVENT = "By World Event"
    METHOD_BY_QUEST = "By quest: {questName}"
    METHOD_KILL = "Kill: {targetName}"
    METHOD_SEVERAL_BOSSESS = "Several bosses"
    EMPTY = "UNKNOW"

class SlotEnum(Enum):
    Head = 1
    Neck = 2
    Shoulder = 3
    Cloak = 16
    Chest = 5
    Wrist = 9
    Gloves = 10
    Waist = 6
    Legs = 7
    Boots = 8
    Ring = 11
    Trinket = 12
    MainHand = 21
    OffHand = 23
    Ranged= 15
