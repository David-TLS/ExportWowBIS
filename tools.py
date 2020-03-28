import json
from html.parser import HTMLParser

import regex
import urllib3

import constants
from fetch_urls import FetchUrls


def extractSingle(re, text, indexGroup = 0):
    groups =  regex.search(re, text)
    if(bool(groups)):
        result = groups.group()
        if(bool(result)):
            return result.strip()
    return False

def extractAll(re, text):
    result =  regex.findall(re, text)
    if(bool(result)):
        return result
    return False


def distinct(array):
    return list(set(array))

# select all bis and return a collection of wowhead link  
class WowIsClassicBisParser(HTMLParser):
        def __init__(self, html):
            super(WowIsClassicBisParser, self).__init__()
            self.html = html

        def __enter__(self):
            self.urls = []
            self.feed(self.html)
            return self.urls
            
        def __exit__(self, type, value, traceback):
            return

        def handle_starttag(self, tag, attrs):
            if tag != 'a':
                return
            attr = dict(attrs)
            if(constants.DATA_WH_ICON_SIZE not in attr and bool(extractSingle(constants.REGEX_BIS_WOWHEAD_LINK, attr['href']))):
                self.urls.append(attr['href'])
            return

class FetchHtmls(FetchUrls):
    def __enter__(self):
        htmls = []
        for html in super().__enter__():
            htmls.append(html.decode('utf8'))
        return htmls

class Phase:
    def __init__(self, name, classes):
        self.name = name
        self.classes = classes

class Classe:
    def __init__(self, name, spes):
        self.name = name
        self.classes = spes

class spe:
    items = None
    def __init__(self, name):
        self.name = name
    
class Item:
    id = None
    name = None
    type = None
    location = None
    dropRate = None
    method = None
    slot = None
    url = None
