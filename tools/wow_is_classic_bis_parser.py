from html.parser import HTMLParser
from constants import Global, RegexEnum
from extract_single import extractSingle

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
