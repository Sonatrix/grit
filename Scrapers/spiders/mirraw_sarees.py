from datetime import datetime as dt
import scrapy
import uuid
import re
from django.utils.text import slugify
from Scrapers.items import Product

class MirrawSpider(scrapy.Spider):
    name = "mirraw_sarees"
    brandId = "49569765-88da-4ab8-99ad-5bad5b2e8d06"
    start_urls = [
        'https://www.mirraw.com/store/sarees',
        'https://www.mirraw.com/store/sarees?min_price=1350&max_price=3825&sort=bstslr&created_at=45&icn=saree_1&ici=bestsellingsarees',
        'https://www.mirraw.com/store/sarees?category_ids=144&min_price=1350&max_price=3825&sort=bstslr'
    ]

    def parse(self, response):
        # follow links to author pages
        for product in response.css('#design-row-block .listings .design_div'):
            href_link = 'https://www.mirraw.com'+product.css("a::attr('href')").extract_first()
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
        newPrice = extract_with_css('h3.new_price_label::text')
        if newPrice is not None:
            item["price"] = float(re.sub("\D", "", newPrice))

        oldPriceText = extract_with_css('div.old_price_label::text')
        if oldPriceText is not None:
            item["old_price"] = float(re.sub("\D", "", oldPriceText))
        else:
            item['old_price']=item["price"]
            

        if item["price"] is None:
            return None
        item["discount"] = int(re.sub("\D", "", extract_with_css('.discount_percent::text')))
        item["description"] = extract_with_css("td:contains('Product Description') ~ td::text")
        item["meta_description"] = item["description"]
        item["category"] = "4b628369-cf33-449b-a814-08debaeb02ba"
        item["images"] = extract_with_css('#design_gallery a::attr(data-image)')
        item["slug"] = f'{slugify(item["name"])}-{item["id"].__hash__()%100000}'
        item["sender"] = self.name
        item['code'] = extract_with_css("#specif_product_id::text")
        item["brand"] = self.brandId
        
        yield item
        