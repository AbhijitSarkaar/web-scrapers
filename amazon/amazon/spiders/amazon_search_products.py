import scrapy
from scrapy.http.request import Request 


class AmazonSearchProductsSpider(scrapy.Spider):
    name = "amazon_search_products"

    def start_requests(self):
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        yield Request(url="https://www.amazon.com/s?k=ipad&crid=2I6AWPB670ZDS&sprefix=ip%2Caps%2C314&ref=nb_sb_noss_2", method='GET', callback=self.parse, headers=headers)

    
    def parse(self, response):
        products = response.xpath("//div[@class='s-main-slot s-result-list s-search-results sg-row']/div[@data-component-type='s-search-result']/div[@class='sg-col-inner']")

        for product in products:
            product_name = product.xpath(".//div[@data-cy='title-recipe']/h2/a/span[@class='a-size-medium a-color-base a-text-normal']/text()").get()
            
            yield {
                "product_name": product_name
            }

        last_page = response.xpath("//span[@class='s-pagination-item s-pagination-next s-pagination-disabled ']")
        if last_page is not None:
            pass

        next_page_button = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
        if next_page_button is not None:
            url = next_page_button.xpath("./@href").get()
            if url is not None:        
                yield response.follow(url=url, callback=self.parse)
            

