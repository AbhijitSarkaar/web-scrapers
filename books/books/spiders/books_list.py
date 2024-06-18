import scrapy
from scrapy.http.request import Request
from books.items import BooksItem


class BooksListSpider(scrapy.Spider):
    name = "books_list"
    allowed_domains = ["books.toscrape.com"]

    def start_requests(self):
        yield Request(url='https://books.toscrape.com', callback=self.parse)


    def parse(self, response):
        books = response.xpath("//ol[@class='row']/li/article[@class='product_pod']")

        print(books)

        for book in books:
            picture = book.xpath("./div[@class='image_container']/a/img/@src").get()
            title = book.xpath("./h3/a/@title").get()
            price = book.xpath("./div[@class='product_price']/p[@class='price_color']/text()").get()

            yield BooksItem(title = title, picture = picture, price = price)




        
