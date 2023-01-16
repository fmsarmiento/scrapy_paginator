# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging, pymongo
import sqlite3

class MongodbPipeline:
    collection_name = 'transcripts'

    def open_spider(self, spider):
        '''Called when a spider is running.'''
        logging.warning("Spider Opened - Pipeline")
        self.client = pymongo.MongoClient("mongodb+srv://francis:francis@cluster0.hmiyoho.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['My_Database']

    def close_spider(self, spider):
        '''Called when a spider is closed.'''
        logging.warning("Spider Closed - Pipeline")
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLitePipeline:
    def open_spider(self, spider):
        '''Called when a spider is running.'''
        logging.warning("Spider Opened - Pipeline")
        self.connection = sqlite3.connect('transcripts.db')
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE transcript (
                    title TEXT,
                    plot TEXT,
                    url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError: pass

    def close_spider(self, spider):
        '''Called when a spider is closed.'''
        logging.warning("Spider Closed - Pipeline")
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO transcript (title,plot,url) VALUES (?,?,?)
        ''', (
            item.get('title'),
            item.get('plot'),
            item.get('url'),
        ))
        self.connection.commit()
        return item
