import scrapy
from scrapy.http.request import Request

class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]

    def start_requests(self):
        yield Request(url=f"https://www.quotes.toscrape.com", callback=self.parse)

    def parse(self, response):
        pass
