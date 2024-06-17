from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class QuotesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('author'):
            author = adapter['author']

            if author == 'Marilyn Monroe' or author == 'Albert Einstein':
                adapter['author'] = adapter['author'].lower()
                return item

            else:
                raise DropItem('Author is not einstein or marylin monroe')



