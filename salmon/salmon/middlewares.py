#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random


class RandomUserAgentDownloaderMiddleware(object):
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawlers):
        return cls(crawlers.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault(b'User-Agent', random.choice(self.user_agents))


class RandomIPProxyDownloaderMiddleware(object):
    def __init__(self, ip_list):
        self.ip_list = ip_list

    @classmethod
    def from_crawler(cls, crawlers):
        return cls(crawlers.settings.getlist('IP_LIST'))

    def process_request(self, request, spider):
        proxy = random.choice(self.ip_list)
        request.meta['proxy'] = proxy
