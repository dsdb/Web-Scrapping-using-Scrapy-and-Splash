# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# use SQLAlchemy for database storage
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class SqllitePipeline:
    def __init__(self):
        engine = create_engine('sqllite://news_articles.db')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

# Modify the process_item (default) method to use SQLAlchemy to create and insert the extracted data
class WebScrapyProjPipeline:
    def process_item(self, item, spider):
        # new insertion
        session = self.Session()
        news_article = NewsArticle(
            title = item.get(' News title'),
            post_id=item.get('Post ID'),
            paragraphs='\n'.join(item.get('Paragraphs'))
        )
        session.add(news_article)
        session.commit()
        session.close()
        return item
    

class NewsArticle(base):
    __tablename__ = 'news_articles'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    title=Column(String(255), nullable=False)
    post_id=Column(Integer, nullable=False)
    paragraphs=Column(Text, nullable=False)

