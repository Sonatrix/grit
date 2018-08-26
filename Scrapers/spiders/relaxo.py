from datetime import datetime as dt
import scrapy
import uuid
from django.utils.text import slugify
from Scrapers.items import Product

class BeautyCenterSpider(scrapy.Spider):
    name = "relaxo"
    brandId = "683973de-36b1-439f-b8f2-0723234a744a"
    start_urls = [
        'https://www.shopatrelaxo.com/women'
    ]

    def parse(self, response):
        # follow links to author pages
        for product in response.css('.product-block'):
            href_link = product.css("[itemprop='url']::attr(href)").extract_first()
            yield response.follow(href_link, self.parse_product)

        # follow pagination links
        #for href in response.css('li.next a::attr(href)'):
            #yield response.follow(href, self.parse)

    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first() 
        item = Product()
        item["id"] = uuid.uuid4()
        item["name"] = extract_with_css('h1::text')
        item["storeUrl"] = response.url
        item["old_price"] = float(extract_with_css('[itemprop=price]::attr(content)'))
        item["price"] = item["old_price"]

        if item["price"] is None:
            return None
        item["description"] = extract_with_css('[itemprop=description]::text')
        item["meta_description"] = item["description"][:30]+"..."
        item["category"] = "39cd5381-acb5-40f9-b8d9-2eb9146e6960"
        item["images"] = [response.css('.carousel-inner a::attr(href)').extract_first()]
        item["slug"] = slugify(item["name"])
        item["sender"] = self.name
        item["brand"] = self.brandId #extract_with_css("[itemprop='brand']::text")
        
        yield item
        