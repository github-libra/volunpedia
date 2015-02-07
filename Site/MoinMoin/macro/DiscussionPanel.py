# -*- coding: iso-8859-1 -*-

class DiscussionPanel:

    def __init__(self, macro):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter

    def execute(self):
        # TODO: better abstract this using the formatter
        html = [
            u'<script language="javascript">render_discussionpanel()</script>',
        ]
        return self.formatter.rawHTML('\n'.join(html))


def macro_DiscussionPanel(macro):
    return DiscussionPanel(macro).execute()

