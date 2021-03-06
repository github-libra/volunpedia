# -*- coding: utf-8 -*-

import sqlite3, re, os, uuid, datetime, time

from MoinMoin import wikiutil

class NgoWikiUtil:
    def __init__(self, request):
        self.request = request

    def parse_page(self, page): 
        text = page.getPageText()
        header = page.getPageHeader()

        title = page.page_name
        summary = ''
        logo = ''

        title_end_idx = None
        summary_end_idx = None
        match = re.search('<<Logo\\(attachment=([^)]+)\\)>>', text)
        if match != None:
            logo = match.group(1)
        match = re.search('= (.*) =', text)
        if match != None:
            title = match.group(1)
            title_end_idx = match.end(0)
            summary_end_idx1 = text.find('== ')
            summary_end_idx2 = text.find('{{')
            summary_end_idx = summary_end_idx1
            if summary_end_idx2 != -1 and summary_end_idx2 < summary_end_idx1:
                summary_end_idx = summary_end_idx2
            summary = text[title_end_idx:summary_end_idx]
            summary = summary.strip()

        categories = []
        locations = []

        if not wikiutil.isTemplatePage(self.request, page.page_name):
            match = re.search(u'## 关键字:([^\r\n]*)\r?\n?', header)
            if match != None:
                categories = match.group(1).split()
            match = re.search(u'## 地域标签:([^\r\n]*)\r?\n?', header)
            if match != None:
                locations = match.group(1).split()

        return {'title': title, 'summary': summary, 'logo': logo, 'categories': categories, 'locations': locations, 'lastmodified': page.mtime_usecs()}

    def is_super_user(self):
        return self.request.user.isSuperUser()

    def open_database(self):
        path = os.path.join(self.request.cfg.data_dir, "database", "ngowiki.dat")
        self.db = sqlite3.connect(path)
        return self.db

    def close_database(self, commit):
        if commit:
            self.db.commit()
        self.db.close()

    def commit_database(self):
        self.db.commit()

    def init_database(self):
        createdb_sql_file = os.path.join(self.request.cfg.data_dir, "database", "createDb.sql")
        with open(createdb_sql_file, 'r') as f:
            for line in f:
                try:
                    self.db.execute(line)
                    self.db.commit()
                except:
                    pass

    def fixup_database_001(self):
        fixupdb_sql_file = os.path.join(self.request.cfg.data_dir, "database", "fixup001.sql")
        with open(fixupdb_sql_file, 'r') as f:
            for line in f:
                try:
                    self.db.execute(line)
                    self.db.commit()
                except:
                    pass

    def fixup_database_002(self):
        fixupdb_sql_file = os.path.join(self.request.cfg.data_dir, "database", "fixup002.sql")
        with open(fixupdb_sql_file, 'r') as f:
            for line in f:
                try:
                    self.db.execute(line)
                    self.db.commit()
                except:
                    pass

    def fixup_database_003(self):
        fixupdb_sql_file = os.path.join(self.request.cfg.data_dir, "database", "fixup003.sql")
        with open(fixupdb_sql_file, 'r') as f:
            for line in f:
                try:
                    self.db.execute(line)
                    self.db.commit()
                except:
                    pass

    def insert_tag(self, tag, type):
        uid = str(uuid.uuid1())
        self.db.execute('''
            INSERT OR IGNORE INTO TAGS(ID, TAG, TYPE) VALUES(?, ?, ?) 
            ''', (uid, tag, type))
        return self.select_tag_by_name(tag)

    def update_tag_hitcount(self, tag):
        self.db.execute('''
             UPDATE TAGS SET HITCOUNT = HITCOUNT + 1 WHERE TAG = ?
            ''', (tag,))

    def select_tag_by_name(self, tag):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, TAG, TYPE FROM TAGS WHERE TAG = ?
            ''', (tag,))
        for row in cursor:
            return {"id": row[0], "tag": row[1], "type": row[2]}

    def select_tag_by_id(self, uid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, TAG, TYPE FROM TAGS WHERE ID = ?
            ''', (uid,))
        for row in cursor:
            return {"id": row[0], "tag": row[1], "type": row[2]}
    
    def remove_tag_by_name(self, tag):
        self.db.execute('''
            DELETE FROM TAGS WHERE TAG = ?
            ''', (tag,))

    def remove_tag_by_id(self, uid):
        self.db.execute('''
            DELETE FROM TAGS WHERE ID = ?
            ''', (uid,))
    
    def insert_page(self, page):
        path = page.page_name
        uid = str(uuid.uuid1())
        pageinfo = self.parse_page(page)
        self.db.execute('''
            INSERT OR IGNORE INTO PAGES(ID, PATH, TITLE, LOGO, SUMMARY, LASTMODIFIED, DATECREATED) VALUES(?, ?, ?, ?, ?, ?, ?)
            ''', (uid, path, pageinfo['title'], pageinfo['logo'], pageinfo['summary'], pageinfo['lastmodified'], pageinfo['lastmodified']))
        return self.select_page_by_path(path)

    def update_page(self, uid, page):
        path = page.page_name
        pageinfo = self.parse_page(page)
        self.db.execute('''
            UPDATE PAGES SET PATH = ?, TITLE = ?, LOGO = ?, SUMMARY = ?, LASTMODIFIED = ? WHERE ID = ?
            ''', (path, pageinfo['title'], pageinfo['logo'], pageinfo['summary'], pageinfo['lastmodified'], uid))
        return self.select_page_by_id(uid)

    def update_idea_status(self, uid, status):
        self.db.execute('''
            UPDATE PAGES SET IDEA_STATUS = ? WHERE ID = ?
            ''', (status, uid))

    def select_idea_status(self, uid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT IDEA_STATUS FROM PAGES WHERE ID = ?
            ''', (uid,))
        for row in cursor:
            return row[0]

    def select_page_by_path(self, path):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, PATH, TITLE, LOGO, SUMMARY, LASTMODIFIED, DATECREATED, HITCOUNT, COMMENTCOUNT, LIKECOUNT, SUPERRECOMMEND FROM PAGES WHERE PATH = ?
            ''', (path,))
        for row in cursor:
            return {"id": row[0], "path": row[1], "title": row[2], "logo": row[3], "summary": row[4], "lastmodified": row[5], "datecreated": row[6], "hitcount": row[7], "commentcount": row[8], "likecount": row[9], "superrecommend": row[10]}
    
    def select_page_by_id(self, uid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, PATH, TITLE, LOGO, SUMMARY, LASTMODIFIED, DATECREATED, HITCOUNT, COMMENTCOUNT, LIKECOUNT, SUPERRECOMMEND FROM PAGES WHERE ID = ?
            ''', (uid,))
        for row in cursor:
            return {"id": row[0], "path": row[1], "title": row[2], "logo": row[3], "summary": row[4], "lastmodified": row[5], "datecreated": row[6], "hitcount": row[7], "commentcount": row[8], "likecount": row[9], "superrecommend": row[10]}
    
    def remove_page_by_path(self, path):
        record = self.select_page_by_path(path)
        if record:
            self.remove_page_by_id(record["id"])
            self.update_page_tags(record["id"], [])

    def remove_page_by_id(self, uid):
        self.db.execute('''
            DELETE FROM PAGES WHERE ID = ?
            ''', (uid,))

    def super_recommend(self, page, comment):
        pageid = self.select_page_by_path(page.page_name)["id"]
        comment = comment.strip()
        if len(comment) == 0:
            self.db.execute('''
                UPDATE PAGES SET SUPERRECOMMEND = NULL WHERE ID = ?
                ''', (pageid,))
        else:
            self.db.execute('''
                UPDATE PAGES SET SUPERRECOMMEND = ? WHERE ID = ?
                ''', (comment, pageid))

    def update_page_meta(self, pageinfo):
        pageid = pageinfo["id"]
        tags = pageinfo["categories"]
        locations = pageinfo["locations"]
        for tag in tags:
            self.insert_tag(tag, 1)
        for location in locations:
            self.insert_tag(location, 2)
        self.update_page_tags(pageid, tags + locations)

    def update_page_tags(self, pageid, tags):
        self.db.execute('''
            DELETE FROM PAGE_TAGS WHERE PAGE_ID = ?
            ''', (pageid,))
        for tag in tags:
            self.db.execute('''
                INSERT INTO PAGE_TAGS(ID, PAGE_ID, TAG_ID) 
                  SELECT ? as ID, ? as PAGE_ID, ID as TAG_ID
                  FROM TAGS
                  WHERE TAG = ?
                ''', (str(uuid.uuid1()), pageid, tag))

    def select_page_tags_by_id(self, page_uuid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT TAGS.ID, TAGS.TAG, TAGS.TYPE
            FROM TAGS TAGS INNER JOIN PAGE_TAGS PAGE_TAGS ON TAGS.ID = PAGE_TAGS.TAG_ID
            WHERE PAGE_TAGS.PAGE_ID = ?
            ''', (page_uuid, ))
        ret = []
        for row in cursor:
            ret.append({"id": row[0], "tag": row[1], "type": row[2]})
        return ret

    def select_page_tags_by_path(self, page_path):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT TAGS.ID, TAGS.TAG, TAGS.TYPE
            FROM TAGS TAGS 
                INNER JOIN PAGE_TAGS PAGE_TAGS ON TAGS.ID = PAGE_TAGS.TAG_ID
                INNER JOIN PAGES PAGES ON PAGES.ID = PAGE_TAGS.PAGE_ID
            WHERE PAGES.PATH = ?
            ''', (page_path, ))
        ret = []
        for row in cursor:
            ret.append({"id": row[0], "tag": row[1], "type": row[2]})
        return ret
    
    def update_page_hitcount_by_id(self, pageid, increase):
        self.db.execute('''
            UPDATE PAGES SET HITCOUNT = HITCOUNT + ? WHERE ID = ?
            ''', (increase, pageid))

    def update_page_hitcount_by_path(self, path, increase):
        self.db.execute('''
            UPDATE PAGES SET HITCOUNT = HITCOUNT + ? WHERE PATH = ?
            ''', (increase, path))

    def update_page_commentcount_by_id(self, pageid, increase):
        self.db.execute('''
            UPDATE PAGES SET COMMENTCOUNT = COMMENTCOUNT + ? WHERE ID = ?
            ''', (increase, pageid))

    def update_page_commentcount_by_path(self, path, increase):
        self.db.execute('''
            UPDATE PAGES SET COMMENTCOUNT = COMMENTCOUNT + ? WHERE PATH = ?
            ''', (increase, path))
    
    def update_page_likecount_by_id(self, pageid, increase):
        self.db.execute('''
            UPDATE PAGES SET LIKECOUNT = LIKECOUNT + ? WHERE ID = ?
            ''', (increase, pageid))

    def update_page_likecount_by_path(self, path, increase):
        self.db.execute('''
            UPDATE PAGES SET LIKECOUNT = LIKECOUNT + ? WHERE PATH = ?
            ''', (increase, path))

    def insert_comment(self, page, userid, comment):
        pageid = self.select_page_by_path(page.page_name)["id"]

        uid = str(uuid.uuid1())
        self.db.execute('''
            INSERT OR IGNORE INTO COMMENTS(ID, PAGE_ID, USER_ID, COMMENT, POSTTIME) VALUES(?, ?, ?, ?, ?) 
            ''', (uid, pageid, userid, comment, long(time.time())))

        self.update_page_commentcount_by_id(pageid, 1)
        return uid

    def select_comment_by_id(self, uid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, PAGE_ID, USER_ID, COMMENT, POSTTIME FROM COMMENTS WHERE ID = ?
            ''', (uid,))
        for row in cursor:
            return {"id": row[0], "page_id": row[1], "user_id": row[2], "comment": row[3], "posttime": row[4]}

    def select_comments_by_page(self, page, offset, length):
        pageid = self.select_page_by_path(page.page_name)["id"]

        sql = '''
            SELECT ID, PAGE_ID, USER_ID, COMMENT, POSTTIME FROM COMMENTS WHERE PAGE_ID = ? ORDER BY POSTTIME DESC LIMIT %s, %s 
            ''' % (str(offset), str(length))

        cursor = self.db.cursor()
        cursor.execute(sql, (pageid,))
        ret = []
        for row in cursor:
            ret.append({"id": row[0], "page_id": row[1], "user_id": row[2], "comment": row[3], "posttime": row[4]})
        return ret
    
    def remove_comments_by_id(self, uid):
        record = self.select_comment_by_id(uid)
        if not record:
            return
        pageid = record["page_id"]

        self.db.execute('''
            DELETE FROM COMMENTS WHERE ID = ?
            ''', (uid,))

        self.update_page_commentcount_by_id(pageid, -1)

    def remove_comments_by_page(self, page):
        pageid = self.select_page_by_path(page.page_name)["id"]

        self.db.execute('''
            DELETE FROM COMMENTS WHERE PAGE_ID = ?
            ''', (pageid,))

    def insert_like(self, page, userid, comment):
        pageid = self.select_page_by_path(page.page_name)["id"]

        uid = str(uuid.uuid1())
        self.db.execute('''
            INSERT OR IGNORE INTO LIKES(ID, PAGE_ID, USER_ID, COMMENT, POSTTIME) VALUES(?, ?, ?, ?, ?) 
            ''', (uid, pageid, userid, comment, long(time.time())))

        self.update_page_likecount_by_id(pageid, 1)
        return uid

    def select_like_by_id(self, uid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, PAGE_ID, USER_ID, COMMENT, POSTTIME FROM LIKES WHERE ID = ?
            ''', (uid,))
        for row in cursor:
            return {"id": row[0], "page_id": row[1], "user_id": row[2], "comment": row[3], "posttime": row[4]}

    def select_like_by_page_and_userid(self, pageid, userid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, PAGE_ID, USER_ID, COMMENT, POSTTIME FROM LIKES WHERE PAGE_ID = ? AND USER_ID = ?
            ''', (pageid, userid))
        for row in cursor:
            return {"id": row[0], "page_id": row[1], "user_id": row[2], "comment": row[3], "posttime": row[4]}
    
    def has_user_liked_page(self, userid, page):
        pageid = self.select_page_by_path(page.page_name)["id"]
        
        record = self.select_like_by_page_and_userid(pageid, userid)
        if not record:
            return False

        return True

    def select_likes_by_page(self, page, offset, length):
        pageid = self.select_page_by_path(page.page_name)["id"]

        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, PAGE_ID, USER_ID, COMMENT, POSTTIME FROM LIKES WHERE PAGE_ID = ? ORDER BY POSTTIME DESC LIMIT %s, %s 
            ''' % (str(offset), str(length)), (pageid,))
        ret = []
        for row in cursor:
            ret.append({"id": row[0], "page_id": row[1], "user_id": row[2], "comment": row[3], "posttime": row[4]})
        return ret
    
    def remove_likes_by_id(self, uid):
        record = self.select_like_by_id(uid)
        if not record:
            return
        pageid = record["page_id"]

        self.db.execute('''
            DELETE FROM LIKES WHERE ID = ?
            ''', (uid,))

        self.update_page_likecount_by_id(pageid, -1)

    def remove_likes_by_page(self, page):
        pageid = self.select_page_by_path(page.page_name)["id"]

        self.db.execute('''
            DELETE FROM LIKES WHERE PAGE_ID = ?
            ''', (pageid,))

    def select_latest_created_pages(self, tags, offset, length):
        p_orderby_clause = "PAGES.DATECREATED DESC"
       
        tagfilter_sql_part = '''
           SELECT PAGE_TAGS.PAGE_ID
           FROM PAGE_TAGS PAGE_TAGS INNER JOIN TAGS TAGS ON PAGE_TAGS.TAG_ID = TAGS.ID
           WHERE TAGS.TAG = ?
           '''
        tagfilter_sql_parts = []
        for tag in tags:
            tagfilter_sql_parts.append(tagfilter_sql_part)

        sql = '''
           SELECT PAGES.ID, PAGES.PATH, PAGES.TITLE, PAGES.LOGO, PAGES.SUMMARY, PAGES.LASTMODIFIED, PAGES.DATECREATED, PAGES.HITCOUNT, PAGES.COMMENTCOUNT, PAGES.LIKECOUNT, PAGES.SUPERRECOMMEND
           FROM PAGES PAGES 
           WHERE PAGES.ID IN (%s)
           ORDER BY %s
           LIMIT %s, %s
           ''' % (" UNION ".join(tagfilter_sql_parts), p_orderby_clause, str(offset), str(length))

        cursor = self.db.cursor()
        cursor.execute(sql, tuple(tags))

        ret = []
        for row in cursor:
            ret.append({"id": row[0], "path": row[1], "title": row[2], "logo": row[3], "summary": row[4], "lastmodified": row[5], "datecreated": row[6], "hitcount": row[7], "commentcount": row[8], "likecount": row[9], "superrecommend": row[10]})
        return ret

    def select_pages_by_tag(self, tags, sortby, order, offset, length):
        p_orderby_clause = ""
        if sortby == "hitcount":
            p_orderby_clause = "PAGES.HITCOUNT " + order
        elif sortby == "commentcount":
            p_orderby_clause = "PAGES.COMMENTCOUNT " + order
        elif sortby == "likecount":
            p_orderby_clause = "PAGES.LIKECOUNT " + order
        elif sortby == "title":
            p_orderby_clause = "PAGES.TITLE " + order
        elif sortby == "popularity":
            p_orderby_clause = "PAGES.COMMENTCOUNT + PAGES.LIKECOUNT DESC, PAGES.HITCOUNT DESC"
        elif sortby == "featured":
            p_orderby_clause = "(2.0 - 2.0/(PAGES.commentcount + 2.0) - 1.0/(PAGES.likecount + 1.0) + (random() % 16 + 25.0)/5.3) DESC"
        else:
            p_orderby_clause = "PAGES.LASTMODIFIED " + order

        p_featured_where_clause = ""
        if sortby == "featured":
            p_featured_where_clause = " AND PAGES.SUPERRECOMMEND IS NOT NULL "

        tagfilter_sql_part = '''
           SELECT PAGE_TAGS.PAGE_ID
           FROM PAGE_TAGS PAGE_TAGS INNER JOIN TAGS TAGS ON PAGE_TAGS.TAG_ID = TAGS.ID
           WHERE TAGS.TAG = ?
           '''
        tagfilter_sql_parts = []
        for tag in tags:
            tagfilter_sql_parts.append(tagfilter_sql_part)

        sql = '''
           SELECT PAGES.ID, PAGES.PATH, PAGES.TITLE, PAGES.LOGO, PAGES.SUMMARY, PAGES.LASTMODIFIED, PAGES.DATECREATED, PAGES.HITCOUNT, PAGES.COMMENTCOUNT, PAGES.LIKECOUNT, PAGES.SUPERRECOMMEND
           FROM PAGES PAGES 
           WHERE PAGES.ID IN (%s) %s
           ORDER BY %s
           LIMIT %s, %s
           ''' % (" INTERSECT ".join(tagfilter_sql_parts), p_featured_where_clause, p_orderby_clause, str(offset), str(length))

        cursor = self.db.cursor()
        cursor.execute(sql, tuple(tags))

        ret = []
        for row in cursor:
            ret.append({"id": row[0], "path": row[1], "title": row[2], "logo": row[3], "summary": row[4], "lastmodified": row[5], "datecreated": row[6], "hitcount": row[7], "commentcount": row[8], "likecount": row[9], "superrecommend": row[10]})
        return ret

    def select_pages_with_one_of_tags(self, tags, sortby, order, offset, length):
        p_orderby_clause = ""
        if sortby == "hitcount":
            p_orderby_clause = "PAGES.HITCOUNT " + order
        elif sortby == "commentcount":
            p_orderby_clause = "PAGES.COMMENTCOUNT " + order
        elif sortby == "likecount":
            p_orderby_clause = "PAGES.LIKECOUNT " + order
        elif sortby == "title":
            p_orderby_clause = "PAGES.TITLE " + order
        elif sortby == "popularity":
            p_orderby_clause = "PAGES.COMMENTCOUNT + PAGES.LIKECOUNT DESC, PAGES.HITCOUNT DESC"
        elif sortby == "featured":
            p_orderby_clause = "(2.0 - 2.0/(PAGES.commentcount + 2.0) - 1.0/(PAGES.likecount + 1.0) + (random() % 16 + 25.0)/5.3) DESC"
        else:
            p_orderby_clause = "PAGES.LASTMODIFIED " + order

        p_featured_where_clause = ""
        if sortby == "featured":
            p_featured_where_clause = " AND PAGES.SUPERRECOMMEND IS NOT NULL "

        tagfilter_sql_part = '''
           SELECT PAGE_TAGS.PAGE_ID
           FROM PAGE_TAGS PAGE_TAGS INNER JOIN TAGS TAGS ON PAGE_TAGS.TAG_ID = TAGS.ID
           WHERE TAGS.TAG = ?
           '''
        tagfilter_sql_parts = []
        for tag in tags:
            tagfilter_sql_parts.append(tagfilter_sql_part)

        sql = '''
           SELECT PAGES.ID, PAGES.PATH, PAGES.TITLE, PAGES.LOGO, PAGES.SUMMARY, PAGES.LASTMODIFIED, PAGES.DATECREATED, PAGES.HITCOUNT, PAGES.COMMENTCOUNT, PAGES.LIKECOUNT, PAGES.SUPERRECOMMEND
           FROM PAGES PAGES 
           WHERE PAGES.ID IN (%s) %s
           ORDER BY %s
           LIMIT %s, %s
           ''' % (" UNION ".join(tagfilter_sql_parts), p_featured_where_clause, p_orderby_clause, str(offset), str(length))

        cursor = self.db.cursor()
        cursor.execute(sql, tuple(tags))

        ret = []
        for row in cursor:
            ret.append({"id": row[0], "path": row[1], "title": row[2], "logo": row[3], "summary": row[4], "lastmodified": row[5], "datecreated": row[6], "hitcount": row[7], "commentcount": row[8], "likecount": row[9], "superrecommend": row[10]})
        return ret
    
    def count_pages_by_tag(self, tags):
        tagfilter_sql_part = '''
           SELECT PAGE_TAGS.PAGE_ID
           FROM PAGE_TAGS PAGE_TAGS INNER JOIN TAGS TAGS ON PAGE_TAGS.TAG_ID = TAGS.ID
           WHERE TAGS.TAG = ?
           '''
        tagfilter_sql_parts = []
        for tag in tags:
            tagfilter_sql_parts.append(tagfilter_sql_part)

        sql = '''
           SELECT COUNT(PAGES.ID) 
           FROM PAGES PAGES 
           WHERE PAGES.ID IN (%s)
           ''' % (" INTERSECT ".join(tagfilter_sql_parts))

        cursor = self.db.cursor()
        cursor.execute(sql, tuple(tags))

        for row in cursor:
            return row[0]

    def select_related_tags(self, tags):
        tagfilter_sql_part = '''
           SELECT PAGE_TAGS.PAGE_ID
           FROM PAGE_TAGS PAGE_TAGS INNER JOIN TAGS TAGS ON PAGE_TAGS.TAG_ID = TAGS.ID
           WHERE TAGS.TAG = ?
           '''
        tagfilter_sql_parts = []
        for tag in tags:
            tagfilter_sql_parts.append(tagfilter_sql_part)

        sql = '''
           SELECT DISTINCT RELATED_TAGS.ID, RELATED_TAGS.TAG, RELATED_TAGS.TYPE
           FROM PAGE_TAGS RELATED_PAGE_TAGS INNER JOIN TAGS RELATED_TAGS ON RELATED_PAGE_TAGS.TAG_ID = RELATED_TAGS.ID 
           WHERE RELATED_PAGE_TAGS.PAGE_ID IN (%s) ORDER BY RELATED_TAGS.HITCOUNT DESC
           ''' % (" INTERSECT ".join(tagfilter_sql_parts))

        cursor = self.db.cursor()
        cursor.execute(sql, tuple(tags))

        ret = []
        for row in cursor:
            ret.append({"id": row[0], "tag": row[1], "type": row[2]})
        return ret

    def insert_spec_image(self, uid, definition):
        if len(uid.strip()) == 0 or self.select_spec_image_by_id(uid) == None:
            uid = str(uuid.uuid1())
        self.db.execute('''
            INSERT OR IGNORE INTO SPEC_IMAGE(ID, DEFINITION) VALUES(?, ?) 
            ''', (uid, definition))

        return uid

    def select_spec_image_by_id(self, uid):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT ID, DEFINITION FROM SPEC_IMAGE WHERE ID = ?
            ''', (uid,))
        for row in cursor:
            return {"id": row[0], "definition": row[1]}