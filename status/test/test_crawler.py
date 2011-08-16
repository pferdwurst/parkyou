#!/usr/bin/env python
# encoding: utf-8
"""
test_crawler.py

Created by tanya mamedalin on 2011-08-09.
Copyright (c) 2011 Kittybooboo. All rights reserved.
"""

import os
import sys
import optparse
import inspect

import unittest

from scrapy import log, signals, project
#from scrapy.xlib.pydispatch import dispatcher

from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import inside_project
from scrapy.utils.misc import walk_modules
from scrapy.command import ScrapyCommand
import scrapy.commands.crawl


#from multiprocessing import Process, Queue



class TestSpider(unittest.TestCase):

    def setUp(self):
        crawler = CrawlerProcess(settings)
        crawler.install()
        # what does this do?
        inproject = inside_project()

        self.crawl_cmd = scrapy.commands.crawl.Command() 

        self.crawl_cmd.set_crawler(crawler)
        self.parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), \
            conflict_handler='resolve')
        self.crawl_cmd.add_options(self.parser)

        #self.crawler.configure()
        #self.items = []
        #dispatcher.connect(self._item_passed, signals.item_passed)
 


        
    def _crawl(self, queue, spider_name):
        spider = self.crawler.spiders.create(spider_name)
        if spider:
            self.crawler.queue.append_spider(spider)
        self.crawler.start()
        self.crawler.stop()
        queue.put(self.items)

    def crawl(self, spider_path):
        queue = Queue()
        p = Process(target=self._crawl, args=(queue, spider,))
        p.start()
        p.join()
        return queue.get(True)

    def test_crawl(self):
       opts, args = self.parser.parse_args(['regscraper']) 
       self.crawl_cmd.process_options(args, opts)
       self.crawl_cmd.run(args, opts)

# Usage
if __name__ == "__main__":
    log.start()
    unittest.main()