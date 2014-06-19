# -*- coding: iso-8859-1 -*-

import os, uuid

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil 

def execute(pagename, request):
    util = NgoWikiUtil(request)

    if not util.is_super_user():
        return

    util.open_database()

    try:
        util.init_database()

        pages = request.rootpage.getPageList(user='', exists='')
        for name in pages:
            if name.find(u'Category') == -1:
                page = Page(request, name)
                page_uuid = util.insert_page(page)["id"]

                pageinfo = util.parse_page(page)
                pageinfo["id"] = page_uuid
                util.update_page_meta(pageinfo)
    finally:
        util.close_database(True)
