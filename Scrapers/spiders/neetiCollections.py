from datetime import datetime as dt
import scrapy
import uuid
import re
from django.utils.text import slugify
from Scrapers.items import Product

class NeetiSpider(scrapy.Spider):
    name = "neeti_kurti"
    brandId = "c7e5b9f4-70b1-4a39-a6c5-d6cf128196ad"
    start_urls = [
        #'https://www.neeticollections.com/Kurtis',
        'https://www.neeticollections.com/index.php?route=product/special&page=1',
        'https://www.neeticollections.com/index.php?route=product/special&page=2',
        'https://www.neeticollections.com/index.php?route=product/special&page=3',    ]

    def parse(self, response):
        # follow links to author pages
        for product in response.css('.quickview'):
            href_link = product.css("a::attr('href')").extract_first()
            yield response.follow(href_link, self.parse_author)

        # follow pagination links
        #for href in response.css('li.next a::attr(href)'):
            #yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first() 
        item = Product()
        item["id"] = uuid.uuid4()
        item["name"] = extract_with_css('h1::text')
        item["storeUrl"] = response.url+"&tracking=5a9c08c9c30f1"
        newPrice = extract_with_css('span.price-new::text')
        if newPrice is not None:
            item["price"] = float(re.sub("[^0-9.]", "", newPrice))
        else:
            item['price'] = 0
        oldPriceText = extract_with_css('span.price-old::text')
        if oldPriceText is not None:
            item["old_price"] = float(re.sub("[^0-9.]", "", oldPriceText))
        else:
            item['old_price']=item["price"]
            

        if item["price"] is None:
            return None

        item["description"] = extract_with_css('p.form-group::text')
        item["meta_description"] = item["description"][:30]+"..."
        item["category"] = "ccae8991-605d-479d-929c-899e53ccf18a"
        item["images"] = extract_with_css('div.large-image img::attr(src)')
        item["slug"] = f'{slugify(item["name"])}-{item["id"].__hash__()%100000}'
        item["sender"] = self.name
        item['discount'] = 0
        item['code']= item["id"].__hash__()%1000000
        item["brand"] = self.brandId
        
        yield item
        