# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class FundItem(Item):
    code = Field()
    name = Field()
    fund_type = Field()
    found_time = Field()
    scale = Field()
    fund_manager_name = Field()
    fund_manager_url = Field()
    fund_admin = Field()
    last_week_ranking = Field()
    last_month_ranking = Field()
    last_3months_ranking = Field()
    last_6months_ranking = Field()
    from_this_year_ranking = Field()
    last_year_ranking = Field()
    last_2years_ranking = Field()
    last_3years_ranking = Field()
    active = Field()


class IdNumberItem(Item):
    code = Field()
    name = Field()
    address = Field()
