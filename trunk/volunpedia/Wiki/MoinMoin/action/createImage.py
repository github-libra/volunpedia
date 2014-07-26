# -*- coding: iso-8859-1 -*-

import os, uuid, json, math

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil 
from PIL import Image
from AttachFile import getAttachDir
from MoinMoin import config, packages

def image_resize(img, size=(1500, 1100)):  
    try:  
        if img.mode not in ('L', 'RGB'):  
            img = img.convert('RGB')  
        img = img.resize(size)  
    except Exception, e:  
        pass  
    return img 

def execute(pagename, request):
    attach_dir = getAttachDir(request, pagename, create=1)
    form = request.values
    img_id = form['name']
    layout = json.loads(form['layout'])

    if len(layout['images']) == 1:
        request.write(layout['images'][0])
        return

    util = NgoWikiUtil(request)
    util.open_database()

    try:
        img_id = util.insert_spec_image(img_id, form['layout'])
    finally:
        util.close_database(True)

    width = int(layout['width'])
    height = int(layout['height'])

    cols = 2
    if len(layout['images']) > 4:
        cols = 3
    rows = int(math.ceil((len(layout['images']) + 0.0) / (cols + 0.0)));
    picWidth = int(math.floor((width - (cols - 1.0) * 3.0) / cols))
    picHeight = int(math.floor((height - (rows - 1.0) * 3.0) / rows))
    
    width = picWidth * cols + 3 * (cols - 1)
    height = picHeight * rows + 3 * (rows - 1)
    
    new_img = Image.new('RGB', (width, height), (255, 255, 255))

    row_idx = 0
    col_idx = 0
    for img_file in layout['images']:
        img = Image.open(os.path.join(attach_dir, img_file).encode(config.charset))
        new_img.paste(image_resize(img, (picWidth, picHeight)), (col_idx * picWidth + col_idx * 3, row_idx * picHeight + row_idx * 3))

        col_idx = col_idx + 1
        if col_idx >= cols:
            col_idx = 0
            row_idx = row_idx + 1

    new_img.save(os.path.join(attach_dir, img_id + '.jpg').encode(config.charset)) 
    request.write(img_id + '.jpg')	