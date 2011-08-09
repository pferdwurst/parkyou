from scrapy.spider import BaseSpider

class StreetscrapeSpider(BaseSpider):
    name = "streetscrape"
    allowed_domains = ["nyc.gov"]
    start_urls = (
        'http://www.nyc.gov/',
        )

    def parse(self, response):
        pass 
