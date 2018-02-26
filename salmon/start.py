#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from salmon.spiders.zhijiandai_spider import ZhijiandaiSpider
from salmon.spiders.jiekuanwang_spider import JiekuanwangSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(ZhijiandaiSpider)
process.crawl(JiekuanwangSpider)
process.start()
