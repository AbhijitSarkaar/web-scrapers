import scrapy
from scrapy.http.request import Request
import json 

class QuotesInfiniteScrollSpider(scrapy.Spider):
    name = "quotes_infinite_scroll"
    allowed_domains = ["quotes.toscrape.com"]
    current_page = 9

    def start_requests(self):
        yield Request(url=f"https://quotes.toscrape.com/api/quotes?page={self.current_page}", callback=self.parse)


    def parse(self, response):
        str = response.body.decode('utf-8')
        json_data = json.loads(str)
        yield json_data

        if json_data['has_next'] is True:
            self.current_page += 1
            yield Request(url=f"https://quotes.toscrape.com/api/quotes?page={self.current_page}", callback=self.parse)

