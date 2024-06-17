import scrapy
from scrapy.http.request import Request


class ProductDescriptionSpider(scrapy.Spider):
    name = "product_description"
    allowed_domains = ["amazon.com"]

    def start_requests(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "X-Requested-With:": "XMLHttpRequest"
        }
        yield Request(url=f"https://www.amazon.com/s?k=shirts&crid=2SQMA9VUPP964&ref=nb_sb_noss_2", headers=headers, method="GET", callback=self.parse)
        
    def parse(self, response):
        products = response.xpath("//div[@data-component-type='s-search-result']//div/span[@data-component-type='s-product-image']")

        for product in products:
            link = product.xpath("./a/@href").get()

            yield response.follow(url=link, callback=self.parse_product_description)

    def parse_product_description(self, response):
        
        title = response.xpath('//span[@id="productTitle"]/text()').get().strip()
        image_link = response.xpath('//div[@id="imgTagWrapperId"]/img/@src').get()
        ratings = response.xpath('//span[@class="a-size-base a-color-base"]/text()').get().strip()
        price = response.xpath('//span[@class="a-price-range"]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[@class="a-offscreen"]/text()').getall()
        
        yield {
            "title": title,
            "image_link": image_link,
            "ratings": ratings,
            "price": price
        }

