# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class ProductPipeline(object):

    collection_name = 'products'

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('host', 'localhost'),
            user=crawler.settings.get('username', 'postgres'),
            password=crawler.settings.get('password', '12345'),
            database=crawler.settings.get('database', 'locator')
        )

    def open_spider(self, spider):
        self.client = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.db = self.client.cursor()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.db.execute("INSERT into product(id, name, description, meta_description, category_id, price, old_price, store_url, images, slug, sender, brand_id, sku, discount) values('{id}','{name}', '{description}','{meta_description}', '{category}', '{price}', '{old_price}', '{storeUrl}', '{images}', '{slug}', '{sender}', '{brand}','{sku}', '{discount}')".format(id=item["id"], name=item["name"], description=item["description"], meta_description=item["meta_description"], category=item["category"], price=item["price"], old_price=item["old_price"], slug=item["slug"], storeUrl=item["storeUrl"], images="{"+item["images"]+"}", sender=item["sender"], brand=item["brand"], sku=item['code'], discount=item['discount']))
            #print("product count {}".format(Product.objects.count()))
        except (Exception, psycopg2.DatabaseError) as error:
            print("error creating database: {0},".format(error))
            print(item["storeUrl"])
        finally:
            self.client.commit()
            #return item
