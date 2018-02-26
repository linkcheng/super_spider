#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import time
import logging
from scrapy.spiders import Spider
from scrapy.http import Request
from salmon.items import SalMonItem
from salmon.common import loads_jsonp, get_mobiles

logger = logging.getLogger(__name__)


class JiekuanwangSpider(Spider):
    name = 'jiekuanwang'
    allowed_domains = [
        'yytaomeng.com',
    ]

    def __init__(self, name=None, **kwargs):
        super(JiekuanwangSpider, self).__init__(name=name, **kwargs)
        self.url = 'http://new.yytaomeng.com/api/user/login'
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'new.yytaomeng.com',
            'Referer': 'http://new.yytaomeng.com/dkw/HTML/login/login.html',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.params = {'callback': 'successCallback'}

    def start_requests(self):
        """获取要爬的 mobile"""

        for mobiles in get_mobiles():
            for mobile in mobiles:
                if not mobile:
                    continue

                url = self.url + '?callback=successCallback&phone=' + mobile + '&passwd=' + mobile + '&_=' + str(int(time.time() * 1000))
                yield Request(url, headers=self.headers)

    def parse(self, response):
        """解析页面"""
        mobiles = re.findall('phone=(.+?)&', response.url)
        mobile = mobiles[0] if mobiles else response.url

        text_json = loads_jsonp(response.text)
        message = text_json.get('msg', '')

        item = SalMonItem()
        item['name'] = self.name
        item['url'] = self.url
        item['mobile'] = mobile
        item['message'] = message

        # 未注册
        if message in ('该手机号码未注册', ):
            item['result'] = 0
        # 已注册
        elif message in ('密码错误', ):
            item['result'] = 1
        # 其他
        else:
            item['result'] = -1

        yield item
