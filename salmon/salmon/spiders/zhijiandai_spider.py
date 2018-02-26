#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import json
import hashlib
import logging
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from salmon.items import SalMonItem
from salmon.common import get_mobiles

logger = logging.getLogger(__name__)


class ZhijiandaiSpider(Spider):
    name = 'zhijiandai'
    allowed_domains = [
        'yizhenmoney.com',
    ]

    def __init__(self, name=None, **kwargs):
        super(ZhijiandaiSpider, self).__init__(name=name, **kwargs)
        self.url = 'https://i.yizhenmoney.com/esb/account/login'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.yizhenmoney.com',
            'Origin': 'https://credit.yizhenmoney.com',
            'Referer': 'https://credit.yizhenmoney.com/login.html',
            'version': '2.2',
        }
        self.params = {
            'deviceType': 'weixin',
        }

    def start_requests(self):
        """获取要爬的 mobile"""
        form_data = self.params.copy()
        for mobiles in get_mobiles():
            for mobile in mobiles:
                if not mobile:
                    continue
                form_data.update({
                    'mobile': mobile,
                    'password': hashlib.md5(mobile.encode()).hexdigest(),
                })
                yield FormRequest(self.url, headers=self.headers, formdata=form_data)

    def parse(self, response):
        """解析页面"""
        logger.info(response.request.headers.get(b'User-Agent'))
        logger.info(response.request.meta.get('proxy'))

        request_body_str = response.request.body.decode()
        mobiles = re.findall('mobile=(.+?)&', request_body_str)
        mobile = mobiles[0] if mobiles else request_body_str

        ret_json = json.loads(response.text)
        message = ret_json.get('message', '')

        item = SalMonItem()
        item['name'] = self.name
        item['url'] = self.url
        item['mobile'] = mobile
        item['message'] = message

        # 未注册
        if message in ('不存在该登录名', ):
            item['result'] = 0
        # 已注册
        elif message in ('密码错误', ):
            item['result'] = 1
        # 其他
        else:
            item['result'] = -1

        yield item
