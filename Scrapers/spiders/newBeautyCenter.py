from datetime import datetime as dt
import scrapy
import uuid
from django.utils.text import slugify
from Scrapers.items import Product

class BeautyCenterSpider(scrapy.Spider):
    name = "beauty_centre"
    brandId = "9c27d1c7-d944-4ef0-bd57-281dccdf4fc3"
    start_urls = [
        'http://www.newbeautycentre.in/skin/face-cleanse/facewash-cleanser',
    ]

    def parse(self, response):
        # follow links to author pages
        for product in response.css('.product-list'):
            href_link = product.css(".product-thumb .image a::attr('href')").extract_first()
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
        item["storeUrl"] = response.url
        item["old_price"] = float(extract_with_css('[itemprop="price"]::text').replace("₹",""))
        item["price"] = item["old_price"]

        if item["price"] is None:
            return None
        item["description"] = '' #extract_with_css('[itemprop="description"]')
        item["meta_description"] = item["description"][:30]+"..."
        item["category"] = "ce867a33-fddf-4e60-89ec-179c9792889d"
        item["images"] = extract_with_css('.product-info .image a::attr(href)')
        item["slug"] = f'{slugify(item["name"])}-{item["id"].__hash__()%100000}'
        item["sender"] = self.name
        item["brand"] = self.brandId #extract_with_css("[itemprop='brand']::text")
        
        yield item