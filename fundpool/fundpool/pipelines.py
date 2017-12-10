# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql.cursors import DictCursor
from fundpool.settings import MYSQL_CONFIG
from fundpool.dbhelper import DBHelper


class FundPipeline(object):
    def __init__(self):
        self.db = DBHelper(DictCursor, **MYSQL_CONFIG)
        self.cr = self.db.cr

    def process_item(self, item, spider):
        self.insert(item, spider)
        return item

    def insert(self, item, spider):
        """插入数据库"""
        # 数据为无效
        if not item['active']:
            sql = 'UPDATE fund_pool.FundPool SET active=0 WHERE code=%s'
            self.cr.execute(sql, (item['code'],))
            self.db.commit()
            return

        sql = 'SELECT id FROM fund_pool.FundDetail WHERE code=%s'
        self.cr.execute(sql, (item['code'], ))
        is_existed = self.cr.fetchall()

        colomns = ['code']
        if item['active'] == 1:
            colomns.extend([
                'name', 'fund_type', 'found_time', 'scale', 'fund_manager_url', 'fund_manager_name', 'fund_admin',
                'last_week_ranking', 'last_month_ranking', 'last_3months_ranking', 'last_6months_ranking',
                'from_this_year_ranking', 'last_year_ranking', 'last_2years_ranking', 'last_3years_ranking',
            ])

        if is_existed:
            sql = 'UPDATE fund_pool.FundDetail SET {0}=%s where code={1}'.\
                format('=%s,'.join(['`' + col + '`' for col in colomns]), item['code'])
        else:
            sql = 'INSERT INTO fund_pool.FundDetail ({0}) VALUES ({1})'.\
                format(','.join(['`' + col + '`' for col in colomns]), ','.join(['%s'] * len(colomns)))

        values = [item['code']]
        if item['active'] == 1:
            values.extend([
                item['name'], item['fund_type'], item['found_time'], item['scale'], item['fund_manager_url'],
                item['fund_manager_name'], item['fund_admin'], item['last_week_ranking'], item['last_month_ranking'],
                item['last_3months_ranking'], item['last_6months_ranking'], item['from_this_year_ranking'],
                item['last_year_ranking'],  item['last_2years_ranking'],  item['last_3years_ranking'],
            ])

        try:
            self.cr.execute(sql, values)
        except Exception as e:
            print(e)
            spider.logger.info('sql: %s' % sql)
            spider.logger.info('values: %s' % str(values))
        else:
            self.db.commit()

    def close_spider(self, spider):
        self.db.close()


class IdNumberPipeline(object):
    def process_item(self, item, spider):
        return item
