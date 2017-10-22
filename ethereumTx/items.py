# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EthereumtxItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    # the sender in transaction
    s = scrapy.Field()
    # the receiver in transaction
    r = scrapy.Field()
    # the value in trasaction
    v = scrapy.Field()
    # 0: transfer 1: create contract 2: invoke contract
    t = scrapy.Field()
    # the block where the transaction existed
    b = scrapy.Field()

class BlockItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    # the number of transactions in the block
    n = scrapy.Field()
    # the block where the transaction existed
    b = scrapy.Field()
