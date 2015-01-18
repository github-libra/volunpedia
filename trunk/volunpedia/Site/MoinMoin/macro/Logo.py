# -*- coding: iso-8859-1 -*-
from MoinMoin.action.AttachFile import getAttachUrl
from MoinMoin.action.AttachFile import exists

class Logo:

    def __init__(self, macro, attachment=u''):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.attachment = attachment
        self.page = macro.request.page

    def execute(self):
        # TODO: better abstract this using the formatter
        html = []
        if exists(self.request, self.page.page_name, self.attachment):
            html.append('<img class="pagelogo" src="')
            html.append(getAttachUrl(self.page.page_name, self.attachment, self.request))
            html.append('" >')
        return self.formatter.rawHTML('\n'.join(html))


def macro_Logo(macro, attachment=u''):
    return Logo(macro, attachment).execute()

