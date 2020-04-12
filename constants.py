# REGEX_EXTRACT_JSON = "{(?:[^{}]|(?R))*\}"
# REGEX_IS_DROPPED = "(?:id)(.*?)(?:'dropped-by')"
# REGEX_COUNT_OUTOF = '(?<="count":)(.*?)(?=,)(.*?)(?<="outof":)(.*?)(?=,)'
from enum import Enum, auto


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
    REGEX_CRAFT_LOCATION = '("name":"Pattern: {itemName}")(((.*)(?<="n":")(.*)(?=",))|((.*)(?<="z":)(.*?)(?=})(.*)))'
    REGEX_SLOT_ID = '(?<=,"slot":)(.*?)(?=,"slotbak)'
    REGEX_IS_CONTAINED = 'id: \'contained-in-object\''
    REGEX_TREASURE_LOCATION ='(?<=location":\[{locationId}\],"name":")(.*?)(?=")'

class Global():
    DATA_WH_ICON_SIZE = 'data-wh-icon-size'
    URL_WOW_IS_CLASSIC = 'https://www.wowisclassic.com/en/best-in-slot/'


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
    Head = auto()
    Neck = auto()
    Shoulder = auto()
    Cloak = auto()
    Chest = auto()
    Wrist = auto()
    Gloves = auto()
    Waist = auto()
    Legs = auto()
    Boots = auto()
    Ring = auto()
    Trinket = auto()
    OneHand = auto()
    MainHand = auto()
    OffHand = auto()
    Back = auto()
    Ranged = auto()
    TwoHand = auto()
    HeldInOffHand = auto()
    Relic = auto()

WowHeadEnum = {
    '1'  : SlotEnum.Head,
    '2'  : SlotEnum.Neck,
    '3'  : SlotEnum.Shoulder,
    '16'  : SlotEnum.Back,
    '5'  : SlotEnum.Chest,
    '9'  : SlotEnum.Wrist,
    '10'  : SlotEnum.Gloves,
    '6'  : SlotEnum.Waist,
    '7'  : SlotEnum.Legs,
    '8'  : SlotEnum.Boots,
    '11'  : SlotEnum.Ring,
    '12'  : SlotEnum.Trinket,
    '13'  : SlotEnum.OneHand,
    '21'  : SlotEnum.MainHand,
    '14'  : SlotEnum.OffHand,
    '22'  : SlotEnum.OffHand,
    '23'  : SlotEnum.HeldInOffHand,
    '15'  : SlotEnum.Ranged,
    '17'  : SlotEnum.TwoHand,
    '28'  : SlotEnum.Relic
}

class PhaseEnum(Enum):
    # Phase1 = '1'
    # Phase2PreRaid = 'pre-raid'
    # Phase2 = '2'
    Phase3 = '3'
    Phase4 = '4'
    Phase5 = '5'
    Phase6 = '6'

class ClasseEnum(Enum):
    Druid = 'druid'
    Hunter = 'hunter'
    Mage = 'mage'
    Paladin = 'paladin'
    Priest = 'priest'
    Rogue = 'rogue'
    Shaman = 'shaman'
    Warrior = 'warrior'
    Warlock = 'warlock'


class SpeEnum(Enum):
    All = auto()
    Fury = auto()
    Protection = auto()
    Elemental = auto()
    Enhancement = auto()
    Restoration = auto()
    Swords = auto()
    Dagger = auto()
    Holy  = auto()
    Shadow = auto()
    Retribution = auto()
    FeralTank = auto()
    FeralDps = auto()
    Balance = auto()

class WowIsClassicSpe(Enum):
    all = SpeEnum.All
    prot = SpeEnum.Protection
    fury = SpeEnum.Fury
    elem = SpeEnum.Elemental
    resto = SpeEnum.Restoration
    enhan = SpeEnum.Enhancement
    dagger = SpeEnum.Dagger
    sword = SpeEnum.Shadow
    holy = SpeEnum.Holy
    shadow = SpeEnum.Shadow
    ret = SpeEnum.Retribution
    protection = SpeEnum.Protection
    heal = SpeEnum.Holy
    tank = SpeEnum.FeralTank
    balance = SpeEnum.Balance
    cat = SpeEnum.FeralDps
