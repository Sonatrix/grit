from datetime import datetime as dt
import scrapy
import uuid
from django.utils.text import slugify
from Scrapers.items import Product

class IsharyaSpider(scrapy.Spider):
    name = "isharya.com"
    brandId = "6f863e08-29a0-4212-99f3-6f39cb350226"
    start_urls = [
        'https://www.isharya.com/fashion-necklaces/page/1/',
        'https://www.isharya.com/fashion-necklaces/page/2/',
        'https://www.isharya.com/fashion-necklaces/page/3/',
        'https://www.isharya.com/fashion-necklaces/page/4/'
    ]

    def parse(self, response):
        # follow links to author pages
        for href_link in response.css("ul.products .wrap-img::attr(href)").extract():
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
        item["old_price"] = float(extract_with_css('.woocommerce-Price-amount::text').replace(",",""))
        item["price"] = float(extract_with_css('.woocommerce-Price-amount::text').replace(",",""))

        if item["price"] is None:
            yield None
        item["description"] = extract_with_css('#tab-description')
        item["meta_description"] = item["description"][:50]+"..."
        item["category"] = "521d5806-0b5f-43ca-9a80-4851bbc703b7"
        item["images"] = ",".join(response.css(".woocommerce-product-gallery__image img::attr(src)").extract())
        item["slug"] = f'{slugify(item["name"])}-{item["id"].__hash__()%100000}'
        item["sender"] = self.name
        item["brand"] = self.brandId
        item['code'] = extract_with_css(".sku") 
        
        yield item
        