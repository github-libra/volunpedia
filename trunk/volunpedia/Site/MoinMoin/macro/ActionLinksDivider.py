# -*- coding: utf-8 -*-
from MoinMoin.ngowikiutil import NgoWikiUtil

class ActionLinksDivider:

    def __init__(self, macro):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.page = macro.request.page

    def execute(self):
        if self.request.user == None or not self.request.user.valid or not self.request.user.may.write(self.page.page_name):
            return ''
        return self.formatter.rawHTML('<hr>')


def macro_ActionLinksDivider(macro):
    return ActionLinksDivider(macro).execute()

