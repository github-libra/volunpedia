# -*- coding: utf-8 -*-

import re
import os
import sys
from MoinMoin.Page import Page

class NGOWIKI_NEWPAGE:

    def __init__(self, macro):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter

    def execute(self):
        reload(sys) 
        sys.setdefaultencoding('utf-8') 

        path = os.path.split(os.path.realpath(__file__))[0]
        path = path + os.sep + 'NGOWIKI_NEWPAGE.html'

        html = []
        with open(path) as f:
            for line in f:
                html.append(line)

        content = self.formatter.rawHTML(u'\n'.join(html))

        copyrightPage = Page(self.request, 'copyright')
        copyrightText = copyrightPage.getPageText()
        copyrightText = copyrightText[:].strip()

        content = content.replace('{copyright}', copyrightText)
        return content


def macro_NGOWIKI_NEWPAGE(macro):
    return NGOWIKI_NEWPAGE(macro).execute()

