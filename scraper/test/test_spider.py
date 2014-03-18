#!/usr/bin/env python
# encoding: utf-8
"""
test_spider.py

Created by tanya mamedalin on 2011-08-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest

import sys
import os
import subprocess

from tempfile import mkdtemp

from os.path import exists, join, dirname, abspath
import scrapy

from scrapy.commands.crawl import Command
from scrapy.crawler import Crawler

from scrapy.command import ScrapyCommand

class TestStatusSpider(unittest.TestCase):
    
    def proc(self, *new_args, **kwargs):
        args = (sys.executable, '-m', 'scrapy.cmdline') + new_args
        return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
            cwd=self.cwd, env=self.env, **kwargs)
    
    def setUp(self):
        self.temp_path = mkdtemp()
        self.cwd = self.temp_path
        self.env = os.environ.copy()
        self.env['PYTHONPATH'] = dirname(scrapy.__path__[0])
        self.c = ScrapyCommand()
        self.c.requires_project = False



    def test_OnStreet(self):
        test_street = "MAIN STREET"
        p = self.proc("runspider", "/Users/tanya/Work/personal-workspace/parkyou/status/spiders/regscraper.py")
        log = p.stdout.read()
        print log
        print p.stderr.read()
        #self.assert_("[scrapy] INFO: Searching for regulations around " in log)


    
if __name__ == '__main__':
    unittest.main()