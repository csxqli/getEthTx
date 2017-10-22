# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
txNum = 0
class EthereumtxPipeline(object):
    def open_spider(self, spider):
        self.file = open('txs.jl', 'w')
        self.blockFile = open('block.jl', 'w')

    def close_spider(self, spider):
        global txNum
        print(txNum)
        self.file.close()
        self.blockFile.close()
        pass

    def process_item(self, item, spider):
        global txNum
        if item['name'] == 'tx':
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        if item['name'] == 'block':
            txNum += int(item['n'])
            line = json.dumps(dict(item)) + "\n"
            self.blockFile.write(line)
        return item
