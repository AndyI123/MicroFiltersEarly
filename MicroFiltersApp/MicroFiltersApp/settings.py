# Scrapy settings for MicroFiltersApp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'MicroFiltersApp'

SPIDER_MODULES = ['MicroFiltersApp.spiders']
NEWSPIDER_MODULE = 'MicroFiltersApp.spiders'

ITEM_PIPELINES = ['MicroFiltersApp.pipelines.MicrofilterAppImagesPipeline']

#IMAGES_STORE = 'TweetSorterResults/'

IMAGES_MIN_HEIGHT = 200
IMAGES_MIN_WIDTH = 200
IMAGES_EXPIRES = 0

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'MicroFiltersApp (+http://cs.uwaterloo.ca/~msmarzouk/Andrew/)'
