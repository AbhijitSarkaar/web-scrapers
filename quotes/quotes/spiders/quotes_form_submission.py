import scrapy
from scrapy.http.request import Request
import requests
from urllib.parse import urljoin
from lxml import html

class QuotesFormSubmissionDataSpider(scrapy.Spider):
    name = "quotes_form_submission"
    allowed_domains = ["quotes.toscrape.com"]

    # start the request to /search.aspx
    
    def start_requests(self):
        yield Request(url="https://quotes.toscrape.com/search.aspx", callback=self.parse)
 

    # parse the website and fetch the url and token
    # start a request to get tags for an author 

    def parse(self, response):

        url_value = response.xpath("//form/@action").get()
        token = response.xpath("//input[@name='__VIEWSTATE']/@value").get()
        authors = response.xpath("//select[@name='author']/option/text()").getall()

        quotes = {}

        for author in authors:
            author_name = author.strip()
            if author_name != '----------':
                quotes[author_name] = self.get_tags(url_value, author_name, token)
        
        yield quotes

    
    def get_tags(self, url_value, author, token):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        payload = {
            'author': author,
            'tag': '----------',
            '__VIEWSTATE': token
        }

        new_page = requests.post(url=urljoin("https://quotes.toscrape.com", url_value), headers=headers, data=payload)
        page_source = html.fromstring(new_page.content.decode())
        print(page_source)
        
        new_token = [str(p) for p in page_source.xpath("//input[@name='__VIEWSTATE']/@value")][0]
        payload['__VIEWSTATE'] = new_token

        options = page_source.xpath('//select[@name="tag"]/option/text()')
        options_text = [str(p) for p in options]

        tag_quotes = {}

        for option in options_text:
            tag = option.strip()
            if tag != '----------':
                tag_quotes[tag] = self.get_quotes(url_value, author, new_token, option.strip())
        
        return tag_quotes
        
    
    def get_quotes(self, url_value, author, token, tag):
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        payload = {
            'author': author,
            'tag': tag,
            '__VIEWSTATE': token
        }

        quotes = []

        new_page = requests.post(url=urljoin("https://quotes.toscrape.com", url_value), headers=headers, data=payload)
        page_source = html.fromstring(new_page.content.decode())
        options = page_source.xpath("//div[@class='results']/div[@class='quote']/span[@class='content']/text()")
        options_text = [str(p) for p in options]

        for option in options_text:
            quotes.append(option)

        return quotes





        
        
        