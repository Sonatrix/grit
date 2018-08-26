from datetime import datetime as dt
import scrapy
import uuid
import re
from django.utils.text import slugify
from Scrapers.items import Product

class MirrawSpider(scrapy.Spider):
    name = "heelsandshoes"
    brandId = "4a0a6532-b644-435d-9373-1733c010e65c"
    categoryId = "39cd5381-acb5-40f9-b8d9-2eb9146e6960"
    start_urls = [
        'http://www.heelsandshoes.com/women-shoes-online/high-heels-for-women',
        'http://www.heelsandshoes.com/women-shoes-online/womens-soft-style-shoes',
        'http://www.heelsandshoes.com/women-shoes-online/flat-shoes-sandals-for-women'
        'http://www.heelsandshoes.com/women-shoes-online/slip-ons-shoes-for-women', 
    ]

    def parse(self, response):
        # follow links to author pages
        for product in response.css('.product-layout'):
            href_link = product.css(".item-title a::attr(href)").extract_first()
            yield response.follow(href_link, self.parse_product)

    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first() 
        item = Product()
        item["id"] = uuid.uuid4()
        item["name"] = extract_with_css('h1::text')
        item["code"] = extract_with_css(".list-unstyled li:contains(Code)::text").replace("Product Code:", "").strip()
        item["storeUrl"] = response.url
        item["old_price"] = float(re.sub("\D","",extract_with_css('.old-price .price::text')))
        item["price"] = float(re.sub("\D","",extract_with_css('.special-price .price::text')))

        item["description"] = extract_with_css('#product_tabs_description::text')
        item["meta_description"] = item["description"][:50]+"..."
        item["category"] = self.categoryId
        item["images"] = response.css('.item img::attr(src)').extract_first()
        item["slug"] = slugify(item["name"]+"-"+item['code'])
        item["discount"] = int(re.sub("\D","",(extract_with_css('.sale-label::text'))))
        item["sender"] = self.name
        item["brand"] = self.brandId
        
        
        yield item
        