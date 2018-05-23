# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from vietnambiz.items import CompanyItem, CompanyProfileItem
import json

class CompanyPipeline(object):
    def open_spider(self, spider):
        self.file = open('company_index.json', 'w')
        header = '['
        self.file.write(header)

    def close_spider(self, spider):
        footer = ']'
        self.file.write(footer)
        self.file.close()

    def process_item(self, item, spider):
        if type(item) is CompanyItem:
            line = json.dumps(dict(item)) + ",\n"
            self.file.write(line)
        return item

class CompanyProfilePipeline(object):
    def open_spider(self, spider):
        self.file = open('company_profiles.json', 'w')
        header = '['
        self.file.write(header)

    def close_spider(self, spider):
        footer = ']'
        self.file.write(footer)
        self.file.close()

    def process_item(self, item, spider):
        if type(item) is CompanyProfileItem:
            line = json.dumps(dict(item)) + ",\n"
            self.file.write(line)
        return item
