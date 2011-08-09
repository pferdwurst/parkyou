# Scrapy settings for streetscrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'streetscrape'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['streetscrape.spiders']
NEWSPIDER_MODULE = 'streetscrape.spiders'
DEFAULT_ITEM_CLASS = 'streetscrape.items.StreetscrapeItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

