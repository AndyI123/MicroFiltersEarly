# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MicrofiltersAppItem(Item):
    image_urls = Field()
    images = Field()
    image_paths = Field()
    content = Field()
    minHeight = Field()
    maxHeight = Field()
    minWidth = Field()
    maxWidth = Field()
    filePath = Field()
    videoIds = Field()

    pass

