from html.parser import HTMLParser

import regex
import urllib3

from constants import Global, RegexEnum
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

def printGroupedData(groupedData):
    for k, v in groupedData:
        print("Group {} {}".format(k, list(v)))

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
            if(Global.DATA_WH_ICON_SIZE not in attr and bool(extractSingle(RegexEnum.REGEX_BIS_WOWHEAD_LINK, attr['href']))):
                self.urls.append(attr['href'])
            return

class FetchHtmls(FetchUrls):
    def __enter__(self):
        responses = []
        for response in super().__enter__():
            response['content'] = response['content'].decode('utf8')
            responses.append(response)
        return responses

class Page(object):
    pages = None
    html = None
    metadata = {}

    def __init__(self, url, metadata):
        self.url = url
        self.metadata = metadata

class Item(object):
    id = None
    name = None
    type = None
    location = None
    dropRate = None
    method = None
    slot = None
    url = None
    phase = None
    classes = None
    spe = None
