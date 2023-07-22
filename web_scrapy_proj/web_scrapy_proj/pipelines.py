# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
# use SQLAlchemy for database storage
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()

# SQLite Class
class SqlitePipeline:
    def __init__(self):
        engine = create_engine('sqlite:///news_articles.db')
        base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

# JsonWritePipeline Class
class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('scrapd_data.json', 'w')
    
    def close_spider(self, spider):
        self.file.close()

# Modify the process_item (default) method to use SQLAlchemy to create and insert the extracted data
class WebScrapyProjPipeline:
    def process_item(self, item, spider):
        # new insertion:SQLite
        session = self.Session()
        news_article = NewsArticle(
            title = item.get(' News title'),
            post_id=item.get('Post ID'),
            paragraphs='\n'.join(item.get('Paragraphs'))
        )
        session.add(news_article)
        session.commit()
        session.close()
        # new insertion:JsonWriter
        line = json.dump(dict(item)) + "\n"
        self.file.write(line)
        return item
    

class NewsArticle(base):
    __tablename__ = 'news_articles'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    title=Column(String(255), nullable=False)
    post_id=Column(Integer, nullable=False)
    paragraphs=Column(Text, nullable=False)

