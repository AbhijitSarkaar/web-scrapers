# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksPipeline:
    def process_item(self, item, spider):

        if spider.name == 'books_category_wise':
            return {
                "category": item['category'].strip(),
                "book_title": item['book_title'],
                "price": item['price'],
                "description": item['description']
            }    
        return item
        
