import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest

class OnlinescraperSpider(CrawlSpider):
    name = 'onlineScraper'
    allowed_domains = ['onlinekhabar.com', 'www.onlinekhabar.com']
    start_urls = ['https://www.onlinekhabar.com/content/news/']

    rules = (
        Rule(LinkExtractor(allow=r'/\d{4}/\d{2}/\d+'), callback='parse_news_article', follow=True),
    )

class WebSiteSpider(scrapy.Spider):
    name = 'onlinekhabar'
    allowed_domains = ['onlinekhabar.com', 'www.onlinekhabar.com']
    start_urls = ['https://www.onlinekhabar.com/content/news/']

    # hanfle specific HTTP status code
    handle_httpstatus_list = [404]

    def start_request(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait':2})

    
    def parse(self, response):
        #links = response.css('#content > div > div > div > div.ok-grid-12 > div:nth-child(3) > div > a::attr(href)').extract()
        links = response.xpath('//div[@class="item"]/div[@class="item__wrap"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, self.parse_article, dont_filter=True)

    def parse_article(self, response):
        title = response.xpath('//h2/text()').get()        
        post_id = response.url.split('/')[-2]        
    # Use the provided XPath to extract paragraphs from the article
        #paragraphs = response.xpath('//*[@id="post-{}"]//div[@class="col colspan3 main__read--content ok18-single-post-content-wrap"]/p/text()'.format(post_id)).extract()
        paragraphs = response.xpath('//div[@class="col colspan3 main__read--content ok18-single-post-content-wrap"]/p/text()').getall()

        article_text = ''.join(paragraphs)
        yield {
            #"News title": title,
            #"Post ID": post_id,
            #"Paragraphs": paragraphs,
            'News title': title.strip(),
            'Post ID': post_id,
            'Paragraphs': paragraphs,
            'Article Text': article_text.strip()
    }