# -*- coding: iso-8859-1 -*-

import json
from MoinMoin.ngowikiutil import NgoWikiUtil 

class PageMetaInfo:

    def __init__(self, macro):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.page = macro.request.page

    def execute(self):
        tags = []
        locations = []

        util = NgoWikiUtil(self.request)
        util.open_database()
        try:
            tag_records = util.select_page_tags_by_path(self.page.page_name)
            
            for record in tag_records:
                if record["type"] == 1:
                    tags.append(record["tag"])
                if record["type"] == 2:
                    locations.append(record["tag"])
        finally:
            util.close_database(True)
        html = []
        html.append('<script language="javascript">' + 'window.__page_meta=' + json.dumps({"tags": tags, "locations": locations}) + '</script>')
        return self.formatter.rawHTML('\n'.join(html))


def macro_PageMetaInfo(macro):
    return PageMetaInfo(macro).execute()

