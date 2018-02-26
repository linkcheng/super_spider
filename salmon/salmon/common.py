#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import json
from functools import partial
from pymysql.cursors import DictCursor

from salmon.dbhelper import DBHelper
from salmon.settings import DB_CONFIG


def loads_jsonp(jsonp):
    if jsonp:
        try:
            return json.loads(re.match(".*?({.*}).*", jsonp, re.S).group(1))
        except Exception:
            return {}
    else:
        return {}


def _get_mobiles(limit=1000, offset=0, length=None):
    """
    数据源为 mysql 的取数据入口
    :param limit: int
    :param offset: int 偏移量
    :param length: int 读取数据的长度
    :return:
    """
    count = 0

    db = DBHelper(DictCursor, **DB_CONFIG)
    cr = db.cr

    if length and length < limit:
        limit = length

    while 1:
        sql = 'SELECT mobile FROM User LIMIT %s OFFSET %s'
        result = cr.execute(sql, (limit, offset))
        values = cr.fetchall()
        mobiles = [val.get('mobile') for val in values]
        yield mobiles

        count += result
        offset += result
        if result < limit:
            break

        if length and count >= length:
            break

    db.close()


get_mobiles = partial(_get_mobiles, offset=10, length=5)


if __name__ == '__main__':
    pass
