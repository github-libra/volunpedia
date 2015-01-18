# -*- coding: iso-8859-1 -*-

import os, uuid, json, math

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil 
from PIL import Image
from MoinMoin.action.AttachFile import getAttachDir
from MoinMoin.action.AttachFile import getAttachUrl
from MoinMoin import config, packages

def execute(pagename, request):
    form = request.values
    img_id = form['name'][0:-4]

    imgs = []

    util = NgoWikiUtil(request)
    util.open_database()

    try:
        data = util.select_spec_image_by_id(img_id)
        if data == None:
            imgs.append(form['name'])
        else:
            imgs = json.loads(data['definition'])['images']
    finally:
        util.close_database(True)

    request.write(json.dumps(imgs))

    