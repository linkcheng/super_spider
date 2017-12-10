#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
from pymysql.cursors import DictCursor
from scrapy import signals
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from fundpool.items import FundItem, IdNumberItem
from fundpool.settings import MYSQL_CONFIG
from fundpool.dbhelper import DBHelper

RANKING = {
    '优秀': 4,
    '良好': 3,
    '一般': 2,
    '不佳': 1,
}

sql = """
select code, name, found_time, scale, 
last_week_ranking+last_month_ranking+last_3months_ranking+last_6months_ranking+from_this_year_ranking+last_year_ranking+last_2years_ranking+last_3years_ranking as total
from FundDetail where fund_type = '债券型' and scale between 2 and 100 order by  total desc, scale desc 
"""

class FundSpider(Spider):
    name = 'fund'
    allowed_domains = ['http://fund.eastmoney.com', 'http://fund.eastmoney.com/manager']

    # 定义了 start_requests 后失效。可以测试使用
    start_urls = [
        # 'http://fund.eastmoney.com/000000.html',
    ]

    def __init__(self, name=None, **kwargs):
        self.db = DBHelper(DictCursor, **MYSQL_CONFIG)

        super(FundSpider, self).__init__(name=name, **kwargs)

    def start_requests(self):
        """获取要爬去的 url"""

        cr = self.db.cr

        limit = 1000
        offset = 1000
        sql = 'SELECT url FROM FundPool WHERE active=1 LIMIT %s OFFSET %s'

        while 1:
            count = cr.execute(sql, (limit, offset))
            records = cr.fetchall()
            urls = [r.get('url') for r in records]

            for url in urls:
                yield Request(url, dont_filter=True)

            offset += count
            if count < limit:
                break

    def closed(self, reason):
        self.db.close()

    def parse(self, response):
        """解析页面"""
        item = FundItem()
        selector = Selector(response)

        item['active'] = 0

        # 首先判断会否是重定向 url
        location_href = selector.xpath('//script[contains(text(),"location.href = ")]/text()').extract()

        tmp_code = selector.xpath('//span[@class="ui-num"]/text()').extract()

        if location_href:
            item['code'] = re.split(r'/|\.', response.url)[-2]
        elif not tmp_code:
            item['code'] = re.split(r'/|\.', response.url)[-2]
            item['active'] = -1
        else:
            code = selector.xpath('//span[@class="ui-num"]/text()').extract()[0]
            name = selector.xpath('//div[@style="float: left"]/text()').extract()[0]

            ft = selector.xpath('//td[contains(text(), "基金类型：")]').extract()[0]
            if 'href' in ft:
                fund_type = selector.xpath('//td[text()="基金类型："]/a/text()').extract()[0]
            else:
                fund_type = re.split(r'\xa0|：', ft)[1]
            fund_manager_name = selector.xpath('//td[text()="基金经理："]/a/text()').extract()[0]

            tmp = selector.xpath('//tr[@class="noBorder"]').extract()
            if tmp:
                fund_manager_url = tmp[0].split('<a href="')[1].split('">')[0]
            else:
                fund_manager_url = selector.xpath('//td[text()="基金经理："]/a/@href').extract()[0]

            # selector.xpath('//a[text()="基金规模"]/../text()').extract() -> ['：33.33亿元（2017-09-30）']
            scale = selector.xpath('//a[text()="基金规模"]/../text()').extract()[0][1:].split('亿元')[0]
            # selector.xpath('//span[text()="成 立 日"]/../text()').extract() -> ['：2013-03-04']
            found_time = selector.xpath('//span[text()="成 立 日"]/../text()').extract()[0][1:]
            fund_admin = selector.xpath('//span[text()="管 理 人"]/../a/text()').extract()[0]

            tmp = selector.xpath('//tr/td/h3/text()').extract()
            last_week_ranking = RANKING.get(tmp[0], 0)
            last_month_ranking = RANKING.get(tmp[1], 0)
            last_3months_ranking = RANKING.get(tmp[2], 0)
            last_6months_ranking = RANKING.get(tmp[3], 0)
            from_this_year_ranking = RANKING.get(tmp[4], 0)
            last_year_ranking = RANKING.get(tmp[5], 0)
            last_2years_ranking = RANKING.get(tmp[6], 0)
            last_3years_ranking = RANKING.get(tmp[7], 0)

            item['name'] = name
            item['code'] = code
            item['fund_type'] = fund_type
            item['fund_admin'] = fund_admin
            item['fund_manager_name'] = fund_manager_name
            item['fund_manager_url'] = fund_manager_url
            item['scale'] = float(scale)
            item['found_time'] = found_time
            item['last_week_ranking'] = last_week_ranking
            item['last_month_ranking'] = last_month_ranking
            item['last_3months_ranking'] = last_3months_ranking
            item['last_6months_ranking'] = last_6months_ranking
            item['from_this_year_ranking'] = from_this_year_ranking
            item['last_year_ranking'] = last_year_ranking
            item['last_2years_ranking'] = last_2years_ranking
            item['last_3years_ranking'] = last_3years_ranking
            item['active'] = 1
        yield item


class IdNumberSpider(Spider):
    name = 'id_number'
    allowed_domains = ['http://tool.bridgat.com']

    # 定义了 start_requests 后失效。可以测试使用
    urls = [
        'http://tool.bridgat.com/id/index.php',
    ]
    formdata = {
        'id': '37112119920902041X',
        'Submit': '+%CC%E1%BD%BB+',
        'a': 'search',
    }

    def start_requests(self):
        """获取要爬去的 url"""
        for url in self.urls:
            yield FormRequest(url, formdata=self.formdata)

    def parse(self, response):
        """解析页面"""
        print(response)
        item = IdNumberItem()
        selector = Selector(response)

        # yield item
