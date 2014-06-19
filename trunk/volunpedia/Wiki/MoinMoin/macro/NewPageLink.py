# -*- coding: utf-8 -*-
from MoinMoin.ngowikiutil import NgoWikiUtil

class NewPageLink:

    def __init__(self, macro, text, type, style=''):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.text = text
        self.type = type
        self.style= style
        if self.style == None:
            self.style = ''
        self.page = macro.request.page
        self.organization = None

    def execute(self):
        if self.request.user == None or not self.request.user.valid or not self.request.user.may.write(self.page.page_name):
            return ''
        ngowikiutil = NgoWikiUtil(self.request)
        pageinfo = ngowikiutil.parse_page(self.page)
        if '公益机构类' in pageinfo['categories'] or '机构类' in pageinfo['categories'] or '企业志愿组织类' in pageinfo['categories'] or '企业类' in pageinfo['categories'] or '企业组织类' in pageinfo['categories'] or '志愿组织类' in pageinfo['categories'] or '服务基地类' in pageinfo['categories'] or '服务站点类' in pageinfo['categories']:
            self.organization = self.page.page_name

        html = []
        html.append('<a class="' + self.style + '" href="' + './_NGO_NEWPAGE?pagetype=' + self.type)
        if self.organization != None:
            html.append('&organization=' + self.organization)
        html.append('">' + self.text + '</a>')
        return self.formatter.rawHTML(''.join(html))


def macro_NewPageLink(macro, text, type, style=''):
    return NewPageLink(macro, text, type, style).execute()

