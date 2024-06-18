import pygsheets
import pandas as pd
from itemadapter import ItemAdapter


class BooksPipeline:


    def process_item(self, item, spider):

        if spider.name == 'books_category_wise':
            return {
                "category": item['category'].strip(),
                "book_title": item['book_title'],
                "price": item['price'],
                "description": item['description']
            }    
        return item
        

class GoogleSheetsPipeline:
    book_items = []

    def save_google_sheets(self):

        # authorization
        gc = pygsheets.authorize(service_file="/Users/abhijitsarkar/skills/scrapy-learning/projects/credentials_google.json")
        
        # empty dataframe 
        df = pd.DataFrame()        

        title_list = []
        image_link_list = []
        price_list = []

        # add values to columns
        for book in self.book_items:
            title_list.append(book['title'])
            image_link_list.append(book['picture'])
            price_list.append(book['price'])

        # create and update columns
        df['title'] = title_list
        df['img'] = image_link_list
        df['price'] = price_list

        # open the google spreadsheet
        sh = gc.open("Web scraper data")

        # select a sheet from list of sheets 
        wks = sh[1]

        # update the sheet 
        wks.set_dataframe(df, (1,1))





    def process_item(self, item, spider):
        self.book_items.append(item)
        return item
    
    def close_spider(self, spider):
        self.save_google_sheets()


