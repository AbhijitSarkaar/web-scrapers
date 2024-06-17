import scrapy
from scrapy.http.request import Request
from quotes.items import QuotesItem

class QuotesPaginationSpider(scrapy.Spider):
    name = "quotes_pagination"
    allowed_domains = ["quotes.toscrape.com"]

    def start_requests(self):
        yield Request(url='https://quotes.toscrape.com', callback=self.parse)


    def parse(self, response):
        
        quotes = response.xpath("//div[@class='quote']")

        for quote in quotes:
            text = quote.xpath("./span[@class='text']/text()").get()
            author = quote.xpath("//span/small[@class='author']/text()").get()
            yield QuotesItem(quote_text=text, author=author)
        
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)