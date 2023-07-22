import scrapy
from scrapy_splash import SplashRequest

class WebSiteSpider(scrapy.Spider):
    name = 'onlinekhabar'
    start_urls = ['https://english.onlinekhabar.com']


    def start_request(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait':2})

    
    def parse(self, response):
        links = response.css('#content > div > div > div > div.ok-grid-12 > div:nth-child(3) > div > a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link.self.parse_article, dont_filter=True)


    def parse_article(self, response):
        title = response.Xpath('//h2/text()').get()
        post_id =response.url.split('/')[-2]

        # Extract paragraphs from the article
        paragraphs = response.xpath('//*[@id="post-{}"]//div[@class="col colspan3 main__read--content ok18-single-post-content-wrap"]/p/text()'.format(post_id)).extract()
        yield{
            "News title":  title,
            "Post ID": post_id,
            "Paragraphs": paragraphs,
        }