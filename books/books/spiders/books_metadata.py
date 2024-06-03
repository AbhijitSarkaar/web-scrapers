import scrapy


class BooksMetadataSpider(scrapy.Spider):
    name = "books_metadata"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.xpath("//div/ol[@class='row']/li")

        for book in books:  
            link = book.xpath("./article/h3/a/@href").get()
            yield response.follow(url=link, callback=self.parse_book)
        
        next_page = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        yield response.follow(url=next_page, callback=self.parse)
        
    
    def parse_book(self, response):
        
        yield {
            "title": response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            "image": response.xpath("//div[@class='thumbnail']/div/div[@class='item active']/img/@src").get(),
            "price": response.xpath("//div[@class='col-sm-6 product_main']/p[@class='price_color']/text()").get(),
            "description": response.xpath("//article[@class='product_page']/p/text()").get()
        }
