#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql


class DBHelper(object):
    def __init__(self, cursor_type, **kwargs):
        self.conn = pymysql.connect(**kwargs)
        self.cr = self.conn.cursor(cursor_type)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.commit()
        self.cr.close()
        self.conn.close()
