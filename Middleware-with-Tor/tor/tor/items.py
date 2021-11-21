# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GpuItem(scrapy.Item):
    gpu_name = scrapy.Field()
    store_name = scrapy.Field()
    fetch_ts = scrapy.Field()
    gpu_price = scrapy.Field()
    gpu_model = scrapy.Field()
    in_stock = scrapy.Field()
    url = scrapy.Field()
