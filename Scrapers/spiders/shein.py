from datetime import datetime as dt
import scrapy
import uuid
from django.utils.text import slugify
from Scrapers.items import Product

class HeadphoneIndiaSpider(scrapy.Spider):
    name = "shein"
    brandId = "9e43b50c-4331-4bd8-9da8-90f9c828812a"
    start_urls = [
        'https://www.shein.in/Tank-Tops-c-1779.html?icn=tanktopscamis&ici=in_navbar04menu08dir02',
        ]

    def parse(self, response):
        # follow links to author pages
        for product in response.css('.c-goodsli .j-item-msg-a::attr(href)'):
            href_link = 'https://www.shein.in'+product.extract_first()
            yield response.follow(href_link, self.parse_product)

        # follow pagination links
        #for href in response.css('li.next a::attr(href)'):
            #yield response.follow(href, self.parse)

    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first() 
        item = Product()
        item["id"] = uuid.uuid4()
        item["name"] = response.css(".name::text")[1].extract()
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
        