from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import logging 

"""
 Base spider to use for the street crawling and regulation scraping
"""

class StatusSpider(BaseSpider):
    name = "statusspider"
    allowed_domains = ["nyc.gov"]
    start_urls = (
        'http://www.nyc.gov/',
        )

    def __init__(self, start_street = "POPLAR STREET"):
        self.on_street = start_street
        self.logger = self.setupLogging()
 
    def parse(self, response):
        pass 

    def setupLogging(self):
       logger = logging.getLogger("statusSpider")
       fileLogger = logging.FileHandler("status_spider.log")
       fileLogger.setLevel(logging.INFO)
       logger.addHandler(fileLogger)
       return logger

    def set_viewstate(self, response, formdata):
        """Extract the viewstate from the response and store it in the formdata
           """
        hxs = HtmlXPathSelector(response)
        vs = hxs.select('//form/input[@name="__VIEWSTATE"]/@value').extract() 
        formdata['__VIEWSTATE']  = vs
        return hxs

       
