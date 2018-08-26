# -*- coding: utf-8 -*-
import scrapy


class CrawlSpider(scrapy.Spider):
    name = 'crawl'
    allowed_domains = ['isharya']
    start_urls = ['http://isharya/']

    def parse(self, response):
        pass
