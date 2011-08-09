# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class StreetscrapeItem(Item):
    # define the fields for your item here like:
    # name = Field()
    regulation = Field()
    side = Field()
    onStreet = Field()
    toStreet = Field()
    fromStreet = Field()
