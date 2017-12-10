#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scrapy.cmdline import execute

name = 'fund'
cmd = 'scrapy crawl {0}'.format(name)
execute(cmd.split())
