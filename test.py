import unittest

from constants import SlotEnum, TypeEnum
from fetch_urls import FetchUrls
from hello import extractItems
from tools import Item


class Mockup():
    @staticmethod
    def item_test_boss():
        #arrange
        expected = Item()
        expected.id = '16921'
        expected.name = 'Halo of Transcendence'
        expected.location = 'Onyxia\'s Lair'
        expected.type = TypeEnum.BY_KILLING
        expected.method = TypeEnum.METHOD_KILL.replace('{targetName}', 'Onyxia')
        expected.dropRate = '18.19%'
        expected.slot = SlotEnum(1)
        expected.url = 'https://classic.wowhead.com/item=16921/halo-of-transcendence'
        return expected

    @staticmethod
    def item_world_drop():
        #arrange
        expected = Item()
        expected.id = '13102'
        expected.name = 'Cassandra\'s Grace'
        expected.type = TypeEnum.BY_KILLING 
        expected.location = TypeEnum.TYPE_BY_WORLD_EVENT
        expected.slot = SlotEnum(1)
        expected.method = TypeEnum.EMPTY
        expected.dropRate = TypeEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=13102/gr%C3%A2ce-de-cassandre'
        return expected

    @staticmethod
    def item_several_boss():
        #arrange
        expected = Item()
        expected.id = '19147'
        expected.type = TypeEnum.BY_KILLING 
        expected.method = TypeEnum.METHOD_SEVERAL_BOSSESS 
        expected.name = 'Ring of Spell Power'
        expected.location = 'Molten Core'
        expected.slot = SlotEnum(11)
        expected.dropRate = TypeEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=19147/ring-of-spell-power'
        return expected

    @staticmethod
    def item_by_craft_with_sublocation():
        #arrange
        expected = Item()
        expected.id = '18405'
        expected.name = 'Belt of the Archmage'
        expected.type = TypeEnum.TYPE_BY_PROFESSION.replace('{professionName}', 'Tailoring')
        expected.location = 'Knot Thimblejack\'s Cache'
        expected.slot = SlotEnum(6)
        expected.dropRate = TypeEnum.EMPTY
        expected.method = TypeEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=18405/belt-of-the-archmage'
        return expected

    @staticmethod
    def item_by_craft_one_location():
        #arrange
        expected = Item()
        expected.id = '14154'
        expected.name = 'Truefaith Vestments'
        expected.type = TypeEnum.TYPE_BY_PROFESSION.replace('{professionName}', 'Tailoring')
        expected.location = 'Stratholme'
        expected.slot = SlotEnum(5)
        expected.dropRate = TypeEnum.EMPTY
        expected.method = TypeEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=14154/truefaith-vestments'
        return expected

    @staticmethod
    def item_by_quest():
        #arrange
        expected = Item()
        expected.id = '18469'
        expected.name = 'Royal Seal of Eldre\'Thalas'
        expected.type = TypeEnum.TYPE_BY_QUEST
        expected.method = 'Holy Bologna: What the Light Won\'t Tell You'
        expected.location = 'Dire Maul'
        expected.slot = SlotEnum(12)
        expected.url = 'https://classic.wowhead.com/item=18469/royal-seal-of-eldrethalas'
        return expected

    @staticmethod
    def item_by_treasure():
        #arrange
        expected = Item()
        expected.id = '11927'
        expected.name = 'Legplates of the Eternal Guardian'
        expected.type = TypeEnum.TYPE_BY_TREASURE
        expected.method = 'Chest of The Seven'
        expected.location = 'Blackrock Depths'
        expected.slot = SlotEnum(7)
        expected.url = 'https://classic.wowhead.com/item=11927/legplates-of-the-eternal-guardian#contained-in-object'
        return expected

class Assert():
    @staticmethod
    def assert_item(methodName, expected, item):
        if(item.id != expected.id):
            print(methodName, 'bad id', item.id, 'instead of', expected.id)

        if(item.name != expected.name):
            print(methodName, 'bad name', item.name, 'instead of', expected.name)

        if(item.location != expected.location):
            print(methodName, 'bad location', item.location, 'instead of', expected.location)

        if(item.type != expected.type):
            print(methodName, 'bad type', item.type, 'instead of', expected.type)

        if(item.method != expected.method):
            print(methodName, 'bad type', item.method, 'instead of', expected.method)

        if(item.slot != expected.slot):
            print(methodName, 'bad type', item.method, 'instead of', expected.method)

class UnitTest():
    @staticmethod
    def test_fetch_url():
        test = FetchUrls(['https://www.youtube.com', 'https://www.google.com'])
        if(len(test.__enter__()) != 2):
            print('FetchUrls not work :/')

    @staticmethod
    def test_items():
        
        expected1 = Mockup.item_test_boss()
        expected2 = Mockup.item_world_drop()
        expected3 = Mockup.item_several_boss()
        expected4 = Mockup.item_by_craft_with_sublocation()
        expected5 = Mockup.item_by_craft_one_location()
        expected6 = Mockup.item_by_quest()
        expected7 = Mockup.item_by_treasure()

        item1 = extractItems([expected1.url])[0]
        item2 = extractItems([expected2.url])[0]
        item3 = extractItems([expected3.url])[0]
        item4 = extractItems([expected4.url])[0]
        item5 = extractItems([expected5.url])[0]
        item6 = extractItems([expected6.url])[0]
        item7 = extractItems([expected7.url])[0]

        Assert.assert_item('item_test_boss', expected1, item1)
        Assert.assert_item('item_world_drop', expected2, item2)
        Assert.assert_item('item_several_boss', expected3, item3)
        Assert.assert_item('item_by_craft_with_sublocation', expected4, item4)
        Assert.assert_item('item_by_craft_one_location', expected5, item5)
        Assert.assert_item('item_by_quest', expected6, item6)
        Assert.assert_item('item_by_treasure', expected7, item7)
        
UnitTest.test_items()
