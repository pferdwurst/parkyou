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

from multiprocessing import Process
from scrapy.xlib.pydispatch import dispatcher



class TestSpider(unittest.TestCase):

    def setUp(self):
        crawler = CrawlerProcess(settings)
        crawler.install()
        # what does this do?
        inside_project()
        self.items = []

        self.crawl_cmd = scrapy.commands.crawl.Command() 
        self.crawl_cmd.set_crawler(crawler)

        self.parser = optparse.OptionParser()
        self.crawl_cmd.add_options(self.parser)
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
       self.items.append(item)

    def _doCrawl(self, spider_name, **kwargs):
       opts, args = self.parser.parse_args([spider_name]) 
       opts.spargs = ["on_street=POPLAR STREET"]
       self.crawl_cmd.process_options(args, opts)
       self.crawl_cmd.run(args, opts)
    '''    
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
   '''

    def test_crawl(self):
        ### Figure out how to pass the spider kwargs to the doCrawl method
        self._doCrawl('regscraper')
        print "This many items were collected %d" % len(self.items)
        self.assertEqual(len(self.items), 6)

# Usage
if __name__ == "__main__":
    log.start()
    unittest.main()