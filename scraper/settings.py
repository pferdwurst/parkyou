# Scrapy settings for status project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'parkyou'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['status.spiders']
#ITEM_PIPELINES = ['status.pipelines.StatusPipeline']
NEWSPIDER_MODULE = 'status.spiders'
DEFAULT_ITEM_CLASS = 'status.items.StatusItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
LOG_LEVEL = 'INFO'

