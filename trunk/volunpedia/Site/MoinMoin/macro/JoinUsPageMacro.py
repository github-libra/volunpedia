# -*- coding: utf-8 -*-

import tenjin, os, time
from tenjin.helpers import *
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil
from MoinMoin.action.AttachFile import exists
from MoinMoin.action.AttachFile import getAttachUrl

class JoinUsPageMacro:

    lastupdated = None

    def __init__(self, macro):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter

    def execute(self):

        if JoinUsPageMacro.lastupdated == None or long(time.time()) - JoinUsPageMacro.lastupdated > 3600L:
            ngowikiutil = NgoWikiUtil(self.request)
            try:
                ngowikiutil.open_database()
            finally:
                ngowikiutil.close_database(True)
            JoinUsPageMacro.lastupdated = long(time.time())

        context = {
        }

        engine = tenjin.Engine(path=[os.path.dirname(__file__) + '/views'])
        html = engine.render('JoinUsPage.pyhtml', context)

        return self.formatter.rawHTML(html)


def macro_JoinUsPageMacro(macro):
    return JoinUsPageMacro(macro).execute()

