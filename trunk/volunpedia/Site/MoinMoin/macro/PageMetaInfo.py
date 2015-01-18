# -*- coding: utf-8 -*-

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
        status = ''

        util = NgoWikiUtil(self.request)
        util.open_database()
        try:
            isActivityPage = False
            tag_records = util.select_page_tags_by_path(self.page.page_name)
            
            for record in tag_records:
                if record["type"] == 1:
                    tags.append(record["tag"])
                    if record["tag"] == u'志愿活动类':
                        isActivityPage = True
                if record["type"] == 2:
                    locations.append(record["tag"])

            if isActivityPage:
                status = util.select_idea_status(util.select_page_by_path(self.page.page_name)['id'])
        finally:
            util.close_database(True)
        html = []
        html.append('<script language="javascript">' + 'window.__page_meta=' + json.dumps({"tags": tags, "locations": locations, "status": status}) + '</script>')
        return self.formatter.rawHTML('\n'.join(html))


def macro_PageMetaInfo(macro):
    return PageMetaInfo(macro).execute()

