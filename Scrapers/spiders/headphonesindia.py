from datetime import datetime as dt
import scrapy
import uuid
from django.utils.text import slugify
from Scrapers.items import Product

class HeadphoneIndiaSpider(scrapy.Spider):
    name = "headphonesindia"
    brandId = "5ab369dc-3daf-4265-b1a3-c90252dadec4"
    start_urls = [
        'https://www.headphonezone.in/collections/wireless-bluetooth-headphones',
        'https://www.headphonezone.in/collections/wireless-bluetooth-earphones',
        'https://www.headphonezone.in/collections/in-ear-earphones',
        'https://www.headphonezone.in/collections/noise-cancellation',
        'https://www.headphonezone.in/collections/extra-bass'
        ]

    def parse(self, response):
        # follow links to author pages
        for product in response.css('.product-wrap'):
            href_link = 'https://www.headphonezone.in'+product.css(".hidden-product-link::attr(href)").extract_first()
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
        item["old_price"] = float(extract_with_css('.was_price .money::text').replace("₹","").replace(",",""))
        item["price"] = float(extract_with_css('.sale::attr(content)'))

        if item["price"] is None:
            yield None
        item["description"] = extract_with_css('[itemprop=description]')
        item["meta_description"] = item["description"][:50]+"..."
        item["category"] = "944a7798-0fdb-4888-bcef-d018eec8dfbf"
        item["images"] = ",".join(response.css(".product_gallery_nav .gallery-cell img::attr(src)").extract())
        item["slug"] = f'{slugify(item["name"])}-{item["id"].__hash__()%100000}'
        item["sender"] = self.name
        item["brand"] = self.brandId
        
        yield item
        