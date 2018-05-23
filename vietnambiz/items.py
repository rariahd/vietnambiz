# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime


class CompanyItem(scrapy.Item):
    source = scrapy.Field()
    industry = scrapy.Field()
    url = scrapy.Field()
    crawled_at = scrapy.Field()

class CompanyProfileItem(scrapy.Item):
    source = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    uid = scrapy.Field()
    company_street_address = scrapy.Field()
    company_website = scrapy.Field()
    company_description = scrapy.Field()
    industry = scrapy.Field()
    company_logo = scrapy.Field()
    company_emails = scrapy.Field()
    country = scrapy.Field()
    company_phone_number = scrapy.Field()
    company_fax_number = scrapy.Field()
    number_of_employees = scrapy.Field()
    type_of_business = scrapy.Field()
    major_brands = scrapy.Field()
    revenue = scrapy.Field()
    created_at = scrapy.Field()
