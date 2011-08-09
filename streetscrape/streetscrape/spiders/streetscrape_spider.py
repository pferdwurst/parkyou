#!/usr/bin/env python
# encoding: utf-8
"""
streetscrape_spider.py

Created by tanya mamedalin on 2011-07-19.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy import log

from streetscrape.items import StreetscrapeItem

import os
import sys


# 3 debug levels, 3 being the most verbose
DEBUG = 1


"""
   Good test streets in Brooklyn are
   1) Everit St. { old fulton street <-> columbia heights}
"""

class StreetscrapeSpider(BaseSpider):
   name = "Boo Ya"
   allowed_domains = ["nyc.gov"]
   start_urls = [
                "http://a841-dotvweb01.nyc.gov/ParkingRegs/ViewController/LocationValidation.aspx"
    ]

   on_street = "POPLAR STREET"
   from_street = "HENRY STREET"
   to_street = "HICKS STREET"
   file_no = 1

   if DEBUG > 1:
      file_no = 1
      out_dir = "responses/" + on_street.replace(" ", "_")
      try:
         os.mkdir(out_dir)
      except OSError:
         log.msg(" debugging directory already exists.  Overwriting...")

   def set_viewstate(self, response, form_data):
      hxs = HtmlXPathSelector(response)
      vs = hxs.select('//form/input[@name="__VIEWSTATE"]/@value').extract() 

      form_data['__VIEWSTATE']  = vs

      # check for errors
      if DEBUG > 1:
         errors = hxs.select('//div[@id="vsErrorMsg"]')
         for ul in errors.select('.//li'):
            log.msg( "errors: ", ul.extract())

      if DEBUG > 1:
         self.log_response(response, self.file_no)
         self.file_no += 1

      return hxs

   def log_response(self, response, step_no):
        # body 
        f = open(self.out_dir + "/body_" + str(self.file_no) + ".html", mode="w")
        f.write(response.body)
        f.close


   def log_request(self, response, step_no):
        # requests
        r = open(self.out_dir + "/req_" + str(step_no), mode="w")
        r.write(response.request.body)
        r.close





   def select_street(self, response, formdata):

      self.set_viewstate(response,formdata)
      formdata['iddOnstreet:txTextBox'] = self.on_street
      formdata['iddFromstreet:txTextBox'] = self.from_street
      formdata['iddTostreet:txTextBox'] = self.to_street

      return [FormRequest.from_response(response,
                        formdata=formdata, clickdata = {"name":"Button6"},
                        callback=lambda r, f = self.from_street, t = self.to_street: self.get_regs(r, f, t))]


   def get_regs(self, response, from_street, to_street):
      if DEBUG > 1: 
         self.log_response(response, self.file_no)
         self.file_no += 1
      
      hxs = HtmlXPathSelector(response)
      #from_street = hxs.select("//select[@id = 'iddFromstreet_ddlDropDown']/option/text()").extract()
      #to_street = hxs.select("//select[@id = 'iddTostreet_ddlDropDown']/option/text()").extract()

      # The regulation results are in a table with id "GridView1"
      found_regs = hxs.select('//table[@id = "GridView1"]/tr')
      n_regs = len(found_regs) - 1
      if DEBUG == 1: print "Found %d regulations for %s AND %s" % (n_regs, from_street, to_street)

      for row in found_regs:
         # The regulation id is a hyperlink with a 'onclick' call, so just grab the text
         reg_no = row.select(".//a/text()")
         if len(reg_no) == 0:
            continue
         # The reg list will contain column values
         # e.g. [Regulation Info,Side, On Street, From Street, To Street]
         reg = StreetscrapeItem(regulation = reg_no.extract())

         # For some reason, cannot grab the text directly that's encapsulated by <font> tags
         rest =  row.select(".//td/font/text()").extract()
         reg['side'] = rest[2]
         reg['onStreet'] = rest[3]
         reg['fromStreet'] = rest[4]
         reg['toStreet'] = rest[5]

         yield reg


   def parse(self, response):
      """ The main method for scrapy.  Begin the scraping here
         """
      formdata = { 'ddlOnBoro': 3, '__VIEWSTATE' : "" }
      self.set_viewstate(response, formdata)

      print "Searching for regulations around %s" % self.on_street

      # print "the form data %s " % self.form_data
      return FormRequest.from_response(response,
                        formdata=formdata, clickdata = {"name":"Button7"},
                        callback=lambda r: self.select_street(r, formdata))





