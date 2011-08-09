#!/usr/bin/env python
# encoding: utf-8
"""
test_viewstate.py

Created by tanya mamedalin on 2011-08-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest


from scrapy.http import HtmlResponse
from scrapy.spiders import BaseSpider

from status.spiders.status_spider import StatusSpider

class TestViewstate(unittest.TestCase):
	
	def spider_factory(self, start_urls = []):
		
		
		class MockSpider(BaseSpider):
			def parse(self, response):
				return response
				
	return MockSpider()
	
    def setUp(self):
        self.spyder = StatusSpider()
        self.mock_spyder = spider_factory(start_urls = "http://a841-dotvweb01.nyc.gov/ParkingRegs/ViewController/LocationValidation.aspx")
        url = self.spyder.start_urls[0]
        print "this is the url %s" % url
        self.response = HtmlResponse(url)
        
    def test_get_viewstate(self):
        viewstate = self.spyder.get_viewstate(self.response)
        self.assertRegexpMatches(viewstate, "/w", "This does not look like a viewstate.")
    
if __name__ == '__main__':
    unittest.main()