import scrapy
from scrapy.http.request import Request


class QuotesTableDataSpider(scrapy.Spider):
    name = "quotes_table_data"
    allowed_domains = ["quotes.toscrape.com"]
    quotes = []

    def start_requests(self):
        yield Request(url="https://quotes.toscrape.com/tableful", callback=self.parse)

    def parse(self, response):
        rows = response.xpath("//table/tr")
        quote_text = ""

        for row in rows:
            row_text = row.xpath("./td/text()").get().strip()
            link_texts = []
            if row_text == "Tags:":
                links = row.xpath("./td/a")
               
                for link in links:
                    link_texts.append(link.xpath("./text()").get())
               
                yield {
                    "quote_text": quote_text,
                    "tags": link_texts
                }
                
            elif len(row_text) != 0:
                quote_text = row_text            
        
                    
                



            
