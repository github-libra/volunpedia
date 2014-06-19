# -*- coding: iso-8859-1 -*-

class NgoNewPage:

    def __init__(self, macro, organization=None, pagetype=None):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.organization = organization
        self.pagetype = pagetype

    def execute(self):
        # TODO: better abstract this using the formatter
        html = [
            u'<div class="pageTitle">%s</div>' % self.title,
        ]
        return self.formatter.rawHTML('\n'.join(html))


def macro_NgoNewPage(macro, organization=None, pagetype=None):
    return NgoNewPage(macro, organization, pagetype).execute()

