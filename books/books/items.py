# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    
    title = scrapy.Field()
    picture = scrapy.Field()
    price = scrapy.Field()

