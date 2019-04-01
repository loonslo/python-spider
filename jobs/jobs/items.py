# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LaGouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_incline(self):
    return self.replace('/', '')


def split_time(self):
    return self.split(' ', 1)[0]


def remove_tags_blank(self):
    return remove_tags(self).replace(' ', '')


def deal_job_addr(self):
    addr_list = self.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip() != '查看地图']
    return ''.join(addr_list)


class LaGouJobItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(input_processor=MapCompose(remove_incline))
    work_years = scrapy.Field(input_processor=MapCompose(remove_incline))
    degree_need = scrapy.Field(input_processor=MapCompose(remove_incline))
    job_type = scrapy.Field()
    publish_time = scrapy.Field(input_processor=MapCompose(split_time))
    tags = scrapy.Field(
        input_processor=Join(','))
    job_advantage = scrapy.Field()
    job_detail = scrapy.Field(input_processor=MapCompose(remove_tags_blank))
    job_addr = scrapy.Field(input_processor=MapCompose(remove_tags_blank, deal_job_addr))
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()

    # company_scale = scrapy.Field()
    # company_employ = scrapy.Field()

    # def get_insert_sql(self):
    #     insert_sql = """
    #     insert into jobs (url, title, salary, job_city, work_years, degree_need, job_type, publish_time, tags, job_detail, job_addr, company_url, company_name, crawl_time)
    #     values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update salary=VALUES (salary),
    #     job_detail= VALUES (job_detail)
    #     """
    #
    #     params = {
    #         self['url'], self['title'], self['salary'], self['job_city'],
    #         self['work_years'], self['degree_need'], self['job_type'], self['publish_time'],
    #         self['tags'], self['job_detail'], self['job_addr'], self['company_url'],
    #         self['company_name'], self['crawl_time'],
    #     }
    #
    #     return insert_sql, params
