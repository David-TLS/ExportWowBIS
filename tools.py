import logging
from html.parser import HTMLParser
from itertools import groupby
from time import gmtime, strftime

import regex
import urllib3

from constants import Global, RegexEnum
from fetch_urls import FetchUrls


# file in file with datetime
def log(string):
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    logging.debug(time + ' - ' + string)

# enumerate a enum
def listEnum(enum):
    return list(map(lambda _: str(_.value), enum))

# extract the first result
def extractSingle(re, text, indexGroup = 0):
    groups =  regex.search(re, text)
    if(bool(groups)):
        result = groups.group()
        if(bool(result)):
            return result.strip()
    return False

# extract all results
def extractAll(re, text):
    result =  regex.findall(re, text)
    if(bool(result)):
        return result
    return False

# disctint value in list
def distinct(array):
    return list(set(array))

# merge neested dictionnary
def merge(a, b, path=None):
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

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

# download an decode to utf8 a collection of url
class FetchHtmls(FetchUrls):
    def __enter__(self):
        responses = []
        for response in super().__enter__():
            response['content'] = response['content'].decode('utf8')
            responses.append(response)
        return responses

# Page object information
class Page(object):
    pages = None
    html = None
    metadata = {}

    def __init__(self, url, metadata):
        self.url = url
        self.metadata = metadata

# Wow item information
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
