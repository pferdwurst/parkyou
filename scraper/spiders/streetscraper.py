from scrapy.spider import BaseSpider

class StreetscraperSpider(BaseSpider):
    name = "streetscraper"
    allowed_domains = ["nyc.gov"]
    start_urls = (
        'http://www.nyc.gov/',
        )

    def __init__(self, start_street = ""):
          self.on_street = start_street


    def parse(self, response):
        pass 
