# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
from cStringIO import StringIO

from PIL import Image
from scrapy.http import Request
from scrapy.exceptions import DropItem
#TODO: from scrapy.contrib.pipeline.media import MediaPipeline
from scrapy.contrib.pipeline.images import ImageException, ImagesPipeline

class MicrofilterAppImagesPipeline(ImagesPipeline):

    global content

    MEDIA_NAME = 'image'
    MIN_WIDTH = 0
    MIN_HEIGHT = 0
    MAX_WIDTH = 0
    MAX_HEIGHT = 0
    THUMBS = {}
    DEFAULT_IMAGES_URLS_FIELD = 'image_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'images'

    def get_media_requests(self, item, info):
        global content
        content = item['content']
        minWidthReal = item['minWidth']
        minHeightReal = item['minHeight']
        maxHeightReal = item['maxHeight']
        maxWidthReal = item['maxWidth']
        for image_url in item['image_urls']:
            yield Request(image_url, meta=dict(tweetContent = content, minWidth = minWidthReal, minHeight = minHeightReal, maxWidth = maxWidthReal, maxHeight = maxHeightReal, filePath = item['filePath']))

    def file_key(self, url):
        return self.image_key(url)

    def file_downloaded(self, response, request, info):
        return self.image_downloaded(response, request, info)

    def get_images(self, response, request, info):
        key = self.file_key(request.url)
        orig_image = Image.open(StringIO(response.body))
        width, height = orig_image.size
        MIN_HEIGHT = int(request.meta.get('minHeight')[0])
        MAX_HEIGHT = int(request.meta.get('maxHeight')[0])
        MIN_WIDTH = int(request.meta.get('minWidth')[0])
        MAX_WIDTH = int(request.meta.get('maxWidth')[0])

        if width < 200 or height < 200:
            raise ImageException("Image incorrect size (%dx%d < %dx%d)" %
                                 (width, height, MIN_WIDTH, MIN_HEIGHT))
        if width/height >= 2 or height/width >= 2:
            raise ImageException("Image incorrent aspect ratio (%dx%d < %dx%d)" %
                                 (width, height, MIN_WIDTH, MIN_HEIGHT))
        if MIN_HEIGHT > MAX_HEIGHT and MIN_WIDTH > MAX_WIDTH:
            if width*height > MAX_WIDTH*MAX_HEIGHT and width*height < MIN_WIDTH*MIN_HEIGHT:
                raise ImageException("Image incorrect size (%dx%d < %dx%d)" %
                                 (width, height, MIN_WIDTH, MIN_HEIGHT))
        else:
            if width*height > MAX_WIDTH*MAX_HEIGHT or width*height < MIN_WIDTH*MIN_HEIGHT:
                raise ImageException("Image incorrect size (%dx%d < %dx%d)" %
                                 (width, height, MIN_WIDTH, MIN_HEIGHT))


        image, buf = self.convert_image(orig_image)
        yield key, image, buf
        f = open(str(request.meta.get('filePath')[0]), 'a')
        f.write(str(request.meta.get('tweetContent')[0]))
        f.write('\t')
        f.write(request.url)
        f.write('\n')
        for thumb_id, size in self.THUMBS.iteritems():
            thumb_key = self.thumb_key(request.url, thumb_id)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_key, thumb_image, thumb_buf


    def image_key(self, url):
        media_guid = hashlib.sha1(url).hexdigest()
        return 'full/%s.jpg' % (media_guid)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


