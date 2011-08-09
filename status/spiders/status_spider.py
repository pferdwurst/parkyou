from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest

import logging

from status.items import StatusItem
from scrapy import log

DEBUG = 1
"""
 activate by > scrapy crawl http://a841-dotvweb01.nyc.gov/ParkingRegs/ViewController/LocationValidation.aspx --set FEED_URI=scraped_data.json --set FEED_FORMAT=json

"""
class StatusSpider(BaseSpider):
   name = "Boo Ya"
   allowed_domains = ["nyc.gov"]
   start_urls = [
                "http://a841-dotvweb01.nyc.gov/ParkingRegs/ViewController/LocationValidation.aspx"
    ]

   on_street = "POPLAR STREET"

   logger = logging.getLogger("statusSpider")
   fileLogger = logging.FileHandler("parkyou.log")
   fileLogger.setLevel(logging.DEBUG)
   logger.addHandler(fileLogger)

   streamer = logging.StreamHandler()
   streamer.setLevel(logging.INFO)
   logger.addHandler(streamer)

   def log_response(self, response, step_no):
        # body 
        calling_fcn =  inspect.stack()[1][3]
        f = open(self.out_dir + "/body_" + calling_fcn + "_" +  str(self.file_no) + ".html", mode="w")
        f.write(response.body)
        f.close

   def get_viewstate(self, response):
      hxs = HtmlXPathSelector(response)
      vs = hxs.select('//form/input[@name="__VIEWSTATE"]/@value').extract()
      return vs

   def set_viewstate(self, response, formdata):
      """Extract the viewstate from the response and store it in the formdata"""
      hxs = HtmlXPathSelector(response)
      vs = hxs.select('//form/input[@name="__VIEWSTATE"]/@value').extract() 
      formdata['__VIEWSTATE']  = vs

      return hxs

   def select_boro(self, response):
      viewstate = self.get_viewstate(response)

      formdata = { 'ddlOnBoro': 3, '__VIEWSTATE' : viewstate }
      return [FormRequest.from_response(response,
                        formdata=formdata, clickdata = {"name":"Button7"},
                        callback=self.select_street)]
    
   def select_street(self, response):
      formdata = { 'ddlOnBoro': 3, 'iddOnstreet:txTextBox':self.on_street }
      self.set_viewstate(response, formdata)

      return [FormRequest.from_response(response,
                        formdata=formdata, clickdata = {"name":"Button6"},
                        callback=self.select_crossstreet1)]


   def select_crossstreet1(self, response):
      formdata = {}
      hxs = self.set_viewstate(response, formdata)

      option_values = hxs.select('//select[@name = "iddFromstreet:ddlDropDown"]/option/@value').extract()

      from_streets = hxs.select('//select[@name = "iddFromstreet:ddlDropDown"]/option/text()').extract()
      self.logger.info( "Found %d cross streets for %s", len(from_streets), self.on_street)
      
      for option, from_street in zip(option_values, from_streets):
         if option == '0': continue
         self.logger.info("(from streets) %s" , from_street)
         formdata['iddFromstreet:ddlDropDown'] = option

         yield FormRequest.from_response(response,
                        formdata=formdata, 
                        clickdata = {"name":"Button7"},
                        callback=self.select_crossstreet2) 


   def select_crossstreet2(self, response):      
      formdata = {}
      hxs = self.set_viewstate(response, formdata)
      
      option_values = hxs.select('//select[@name = "iddTostreet:ddlDropDown"]/option/@value').extract()
      to_streets = hxs.select('//select[@name = "iddTostreet:ddlDropDown"]/option/text()').extract()
      
      for option, to_street  in zip(option_values,to_streets):
         if option == '0': continue
         formdata['iddTostreet:ddlDropDown'] = option
         yield FormRequest.from_response(response,
                        formdata=formdata, 
                        clickdata = {"name":"Button7"},
                        callback=self.step_four)

   def step_four(self, response):
      hxs = HtmlXPathSelector(response)
      from_street = hxs.select("//select[@id = 'iddFromstreet_ddlDropDown']/option[@selected = 'selected']/text()").extract()
      the_to_street = hxs.select("//select[@name = 'iddTostreet:ddlDropDown']/option[@selected = 'selected']/text()").extract()
    
      found_regs = hxs.select('//table[@id = "GridView1"]/tr')
      n_regs = len(found_regs) - 1
      self.logger.info( "STEP FIVE: Found %d regulations for %s AND %s", n_regs, from_street, the_to_street)
      for row in found_regs:
         # The regulation id is a hyperlink with a 'onclick' call, so just grab the text
         reg_no = row.select(".//a/text()")
         if len(reg_no) == 0:
            continue
         # The reg list will contain column values
         # e.g. [Regulation Info,Side, On Street, From Street, To Street]
         reg = StatusItem(regulation = reg_no.extract())

         # For some reason, cannot grab the text directly that's encapsulated by <font> tags
         rest =  row.select(".//td/font/text()").extract()
         reg['side'] = rest[2]
         reg['onStreet'] = rest[3]
         reg['fromStreet'] = rest[4]
         reg['toStreet'] = rest[5]

         yield reg


   def parse(self, response):
      viewstate = self.get_viewstate(response)
      self.logger.info( "Searching for regulations around %s", self.on_street)

      formdata = { 'ddlOnBoro': 3, '__VIEWSTATE' : viewstate }
      return [FormRequest.from_response(response,
                        formdata=formdata, clickdata = {"name":"Button7"},
                        callback=self.select_boro)]
#                       callback=lambda r: self.select_boro(r, viewstate))]

   def __init__(self, start_street = "POPLAR STREET"):
      self.on_street = start_street

def main():
	spider = StatusSpider("POPLAR STREET")

if __name__ == '__main__':
	main()
