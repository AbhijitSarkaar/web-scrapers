import scrapy


class BooksCategoryWiseSpider(scrapy.Spider):
    name = "books_category_wise"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        categories = response.xpath("//div[@class='side_categories']/ul[@class='nav nav-list']/li/ul/li")

        for category in categories:
            category_title = category.xpath(".//a/text()").get()
            link = category.xpath(".//a/@href").get()

            yield response.follow(url=link, callback=self.parse_category, meta={'title': category_title})

    
    def parse_category(self, response):
        
        category_title = response.request.meta['title']
        
        books = response.xpath("//div/ol[@class='row']/li")
        for book in books:
            link = book.xpath(".//article/h3/a/@href").get()
            yield response.follow(url=link, callback=self.parse_book, meta={'category_title': category_title})

    def parse_book(self, response):
        
        yield {
            "category": response.request.meta['category_title'],
            "book_title": response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            "price": response.xpath("//div[@class='col-sm-6 product_main']/p[@class='price_color']/text()").get(),
            "description": response.xpath("//article[@class='product_page']/p/text()").get()
        }


