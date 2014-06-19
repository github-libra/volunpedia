# -*- coding: utf-8 -*-

import tenjin, os
from tenjin.helpers import *
from MoinMoin.Page import Page

class FrontpageSampleMacro:

    def __init__(self, macro):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter

    def execute(self):
        context = {
        }
        engine = tenjin.Engine(path=[os.path.dirname(__file__) + '/views'])
        html = engine.render('FrontpageSample.pyhtml', context)

        return self.formatter.rawHTML(html)


def macro_FrontpageSampleMacro(macro):
    return FrontpageSampleMacro(macro).execute()

