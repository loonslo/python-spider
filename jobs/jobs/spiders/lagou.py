# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import LaGouJobItemLoader, LaGouJobItem

import hashlib


def get_md5(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=r'gongsi/\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+\.html'), callback='parse_job', follow=True),

    )

    def parse_job(self, response):
        item_loader = LaGouJobItemLoader(item=LaGouJobItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('title', '.job-name::attr(title)')
        item_loader.add_xpath('salary', '//*[@class="job_request"]/p/span[1]/text()')
        item_loader.add_xpath('job_city', '//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath('work_years', '//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath('degree_need', '//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('job_type', '//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css('publish_time', '.publish_time::text')
        selector = scrapy.Selector(text=response.text)
        if not selector.css('.labels::text'):
            item_loader.add_css('tags', [''])
        else:
            item_loader.add_css('tags', '.labels::text')

        item_loader.add_css('job_advantage', '.job-advantage p::text')
        item_loader.add_css('job_detail', '.job-detail')
        item_loader.add_css('job_addr', '.work_addr')
        item_loader.add_css('company_url', '.c_feature li a::attr(title)')
        item_loader.add_css('company_name', '#job_company dt a img::attr(alt)')
        item_loader.add_value('crawl_time', str(datetime.now().timestamp()))
        # item_loader.add_xpath('company_scale', '//*[@class="c_feature"]/li[3]')
        # item_loader.add_xpath('company_employ', '
        job_item = item_loader.load_item()
        return job_item
