# Scrapy settings for regulationscrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'regulationscrape'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['regulationscrape.spiders']
NEWSPIDER_MODULE = 'regulationscrape.spiders'
DEFAULT_ITEM_CLASS = 'regulationscrape.items.RegulationscrapeItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

