# Page object information
class Page(object):
    pages = None
    html = None
    metadata = {}

    def __init__(self, url, metadata):
        self.url = url
        self.metadata = metadata
