import unittest

from constants import SlotEnum, BisTrackerEnum
from fetch_url import FetchUrl
from get_page import (extractItems, extractItemUrls, generatePage,pagesToBistracker)
from tools import Item, Page


class Mockup():
    @staticmethod
    def item_test_boss():
        #arrange
        expected = Item()
        expected.id = '16921'
        expected.name = 'Halo of Transcendence'
        expected.location = 'Onyxia\'s Lair'
        expected.type = BisTrackerEnum.BY_KILLING
        expected.method = BisTrackerEnum.METHOD_KILL.replace('{targetName}', 'Onyxia')
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
        expected.type = BisTrackerEnum.BY_KILLING 
        expected.location = BisTrackerEnum.TYPE_BY_WORLD_EVENT
        expected.slot = SlotEnum(1)
        expected.method = BisTrackerEnum.EMPTY
        expected.dropRate = BisTrackerEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=13102/gr%C3%A2ce-de-cassandre'
        return expected

    @staticmethod
    def item_several_boss():
        #arrange
        expected = Item()
        expected.id = '19147'
        expected.type = BisTrackerEnum.BY_KILLING 
        expected.method = BisTrackerEnum.METHOD_SEVERAL_BOSSESS 
        expected.name = 'Ring of Spell Power'
        expected.location = 'Molten Core'
        expected.slot = SlotEnum(11)
        expected.dropRate = BisTrackerEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=19147/ring-of-spell-power'
        return expected

    @staticmethod
    def item_by_craft_with_sublocation():
        #arrange
        expected = Item()
        expected.id = '18405'
        expected.name = 'Belt of the Archmage'
        expected.type = BisTrackerEnum.TYPE_BY_PROFESSION.replace('{professionName}', 'Tailoring')
        expected.location = 'Knot Thimblejack\'s Cache'
        expected.slot = SlotEnum(6)
        expected.dropRate = BisTrackerEnum.EMPTY
        expected.method = BisTrackerEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=18405/belt-of-the-archmage'
        return expected

    @staticmethod
    def item_by_craft_one_location():
        #arrange
        expected = Item()
        expected.id = '14154'
        expected.name = 'Truefaith Vestments'
        expected.type = BisTrackerEnum.TYPE_BY_PROFESSION.replace('{professionName}', 'Tailoring')
        expected.location = 'Stratholme'
        expected.slot = SlotEnum(5)
        expected.dropRate = BisTrackerEnum.EMPTY
        expected.method = BisTrackerEnum.EMPTY
        expected.url = 'https://classic.wowhead.com/item=14154/truefaith-vestments'
        return expected

    @staticmethod
    def item_by_quest():
        #arrange
        expected = Item()
        expected.id = '18469'
        expected.name = 'Royal Seal of Eldre\'Thalas'
        expected.type = BisTrackerEnum.TYPE_BY_QUEST
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
        expected.type = BisTrackerEnum.TYPE_BY_TREASURE
        expected.method = 'Chest of The Seven'
        expected.location = 'Blackrock Depths'
        expected.slot = SlotEnum(7)
        expected.url = 'https://classic.wowhead.com/item=11927/legplates-of-the-eternal-guardian#contained-in-object'
        return expected

    @staticmethod
    def item_by_quest_several_same_location():
        #arrange
        expected = Item()
        expected.id = '19383'
        expected.name = 'Master Dragonslayer\'s Medallion'
        expected.location = 'Stormwind City, Orgrimmar'
        expected.type = BisTrackerEnum.TYPE_BY_QUEST
        expected.method = "The Lord of Blackrock"
        expected.slot = SlotEnum(2)
        expected.url = 'https://classic.wowhead.com/item=19383/master-dragonslayers-medallion'
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
        expected8 = Mockup.item_by_quest_several_same_location()

        item1 = extractItems([Page(expected1.url, {'itemUrls': [expected1.url]})])[0].metadata['items'][0]
        item2 = extractItems([Page(expected2.url, {'itemUrls': [expected2.url]})])[0].metadata['items'][0]
        item3 = extractItems([Page(expected3.url, {'itemUrls': [expected3.url]})])[0].metadata['items'][0]
        item4 = extractItems([Page(expected4.url, {'itemUrls': [expected4.url]})])[0].metadata['items'][0]
        item5 = extractItems([Page(expected5.url, {'itemUrls': [expected5.url]})])[0].metadata['items'][0]
        item6 = extractItems([Page(expected6.url, {'itemUrls': [expected6.url]})])[0].metadata['items'][0]
        item7 = extractItems([Page(expected7.url, {'itemUrls': [expected7.url]})])[0].metadata['items'][0]
        item8 = extractItems([Page(expected8.url, {'itemUrls': [expected8.url]})])[0].metadata['items'][0]

        Assert.assert_item('item_test_boss', expected1, item1)
        Assert.assert_item('item_world_drop', expected2, item2)
        Assert.assert_item('item_several_boss', expected3, item3)
        Assert.assert_item('item_by_craft_with_sublocation', expected4, item4)
        Assert.assert_item('item_by_craft_one_location', expected5, item5)
        Assert.assert_item('item_by_quest', expected6, item6)
        Assert.assert_item('item_by_treasure', expected7, item7)
        Assert.assert_item('item_by_treasure', expected8, item8)
        
UnitTest.test_items()
