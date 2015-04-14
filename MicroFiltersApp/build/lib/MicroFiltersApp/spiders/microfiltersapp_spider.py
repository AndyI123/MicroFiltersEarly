from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from PIL import Image
from scrapy.http import Request
import os
import re
import urlparse
from shutil import *
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.http.request import Request
from scrapy.item import Item
from MicroFiltersApp.items import MicrofiltersAppItem
from Tkinter import *
from guess_language import guess_language
import ttk
import datetime
import csv
import codecs
import json
import string
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from tkFileDialog import askopenfilename

class MicroFiltersAppSpider(BaseSpider):

    name = "MicroFiltersApp"

    ERROR_STR= """Error removing %(path)s, %(error)s """
    global filterRTsGlobal
    filterRTsGlobal = 'n'
    global filterDsGlobal
    filterDsGlobal = 'n'
    global imagesToKeep
    imagesToKeep = []
    global filterEnglishGlobal
    filterEnglishGlobal = 'n'
    global sortByGlobal
    sortByGlobal = 'n'
    global filterVideosGlobal
    filterVideosGlobal = 'n'

    def filterOutRetweets(self, filePathToFilter):
        lines = []
        with open(filePathToFilter, 'r') as fileToFilter:
            lines = fileToFilter.readlines()
            fileToFilter.close()
        with open(filePathToFilter, 'w') as fileToFilter:
            for line in lines:
                if 'RT ' not in line:
                    fileToFilter.write(line)


    def filterDuplicates(self, filePathToFilter, idfun=None):
        seq = []
        with open(filePathToFilter, 'r') as fileToFilter:
            seq = fileToFilter.readlines()
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if seen.has_key(marker): continue
            seen[marker] = 1
            result.append(item)
        with open(filePathToFilter, 'w') as fileToFilter:
            for line in result:
                fileToFilter.write(line)

    def filterEnglishTweets(self, filePathToFilter):
        lines = []
        newLines = []
        with open(filePathToFilter, 'r') as fileToFilter:
            lines = fileToFilter.readlines()
        for line in lines:
            if guess_language(line.decode("utf-8")) == u"en":
                newLines.append(line)
        with open(filePathToFilter, 'w') as fileToFilter:
            for line in newLines:
                fileToFilter.write(line)


    def rmgeneric(self, path, __func__):
        try:
            __func__(path)
            print 'Removed ', path
        except OSError, (errno, strerror):
            print ERROR_STR % {'path' : path, 'error': strerror }

    def removeall(self, path):
        if not os.path.isdir(path):
            return
        files=os.listdir(path)
        for x in files:
            fullpath=os.path.join(path, x)
            if os.path.isfile(fullpath):
                f=os.remove
                self.rmgeneric(fullpath, f)
            elif os.path.isdir(fullpath):
                self.removeall(fullpath)
                f=os.rmdir
                self.rmgeneric(fullpath, f)

    def convertFormat(self, path, newPath):

        with open(path, 'rb') as f:
            reader = csv.reader(f)
            currentFormat = f.readline().split(',');
            defaultFormat = ['username', 'tweet', 'time', 'userID', 'location', 'latitute', 'longitude', 'tweetID']
            contentArray = []
            newContentArray = []
            for x in reader:
                splitLine = x
                newLine = []
                print x
                for y in defaultFormat:
                    print y
                    if (y in currentFormat) and len(splitLine) == len(currentFormat):
                        newLine.append(splitLine[currentFormat.index(y)])
                    else:
                        newLine.append('N/A')
                    print newLine
                newContentArray.append('\t'.join(newLine))
        with open(newPath, 'wb') as f:
            f.write('\n'.join(newContentArray))


    def __init__(self, *args, **kwargs):
        filePathToOpen = kwargs.get('FP')
        self.convertFormat(filePathToOpen, kwargs.get('FP2'))
        allowed_domains = ["dmoz.org"]
        global urlToContent
        urlToContent = {}
        self.rules = (
            Rule(SgmlLinkExtractor(allow=(".",)), callback='parse_item', follow=True),
        )
        filePathToOpen = kwargs.get('FP2')
        global filterRTsGlobal
        filterRTsGlobal = kwargs.get('RT')
        global filterDsGlobal
        filterDsGlobal = kwargs.get('D')
        global imagesToKeep
        imagesToKeep = ['S', 'M', 'L']
        global filterEnglishGlobal
        filterEnglishGlobal = kwargs.get('ENG')
        global sortByGlobal
        sortByGlobal = kwargs.get('SORT')
        global filterVideosGlobal
        filterVideosGlobal = kwargs.get('VID')
        print filterRTsGlobal
        if filterRTsGlobal == 'y':
            self.filterOutRetweets(filePathToOpen)
        if filterDsGlobal == 'y':
            self.filterDuplicates(filePathToOpen)
        if filterEnglishGlobal == 'y':
            self.filterEnglishTweets(filePathToOpen)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        if os.path.exists('TweetSorterResults/'):
            self.removeall('TweetSorterResults/')
        with open(filePathToOpen, 'rw+') as content_file:
            content = content_file.read()
            contentLines = content.split('\n')
            self.start_urls = []
            realLines = []
            for line in contentLines:
                a = re.findall('(http://t.co/[a-zA-z0-9]{6,12})', line)
                #import pdb; pdb.set_tracep
                if a:
                    self.start_urls.append(a[0])
                    realLines.append(line)
                    urlToContent[a[0]] = line
        super(MicroFiltersAppSpider, self).__init__(*args, **kwargs)
        print self.start_urls

    def csvFunc(self):
        content = ''
        files = os.listdir('TweetSorterResults/')
        for x in files:
            if os.path.isfile('TweetSorterResults/' +x):
                with open('TweetSorterResults/' + x, 'r') as f:
                    content = f.read()

                content = content.replace(',', '')
                content = content.replace('\t', ',')
                content = content.replace('\\t', ',')

                with open('TweetSorterResults/1' + x, 'w') as f:
                    f.write(content)
                os.renames('TweetSorterResults/1' + x, 'TweetSorterResults/' + x.split('.')[0] + '.csv')
                f = open('TweetSorterResults/' + x.split('.')[0] + '.csv', 'r')
                reader = csv.DictReader(f, fieldnames = ( "username","tweet","time","location", "latitute", "longitude", "image") )
                out = out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in reader]) + "\n]"
                with open('TweetSorterResults/1' + x + '.json', 'w') as f:
                    f.write(out)
                os.renames('TweetSorterResults/1' + x + '.json', 'TweetSorterResults/' + x.split('.')[0] + '.json')


    def mediaType(self, linkName):
        videos = ["youtube.com", "vimeo.com", "livestream.com", "metacafe.com", "/video/", "screen.yahoo.com"]
        images = ["twitpic.com", "media.photobucket.com", "flickr", "instagram", "yfrog", "/photo/", "/media/", "photo.php"]
        tweetCategory = "article_clicker"
        expanded = linkName

        for x in  videos:
            if x in expanded:
                tweetCategory = "video_clicker"
        for x in images:
            if x in expanded:
                tweetCategory = "image_clicker"

        return tweetCategory

    def parse(self, response):
        linkName = response.url
        filePath = 'TweetSorterResults/' + self.mediaType(linkName=linkName) + '.txt'
        #items = []
        #linkType = self.mediaType(linkName)
        hxs = HtmlXPathSelector(response)
        link = hxs.select("//img[not(name(..) = 'a') or contains(../@href, '.jpg') or contains(../@href, '.png') or contains(../@href, '.gif')]/@src").extract()
        videos = hxs.select("//iframe[contains(@src, 'youtube.com/') and (contains(@src, '/embed/') or contains(@src, '/v/'))]/@src").extract()
        videoIds = []
        absoluteLinks = []



        if filterVideosGlobal == 'filter':
            for video in videos:
                f = open(filePath, 'a')
                f.write(urlToContent[response.request.meta['redirect_urls'][0]])
                f.write('\t')
                f.write(video.split('/')[-1])
                f.write('\n')
                videoIds.append(video.split('/')[-1])



        #f = open('/Users/ilyas/Documents/' + linkType + '.txt', 'a')
        for x in link:
            if not x.startswith('http'):
                x = urlparse.urljoin(linkName, x)
            #f.write(contentLines[i] + '\t' + linkName + '\t' +  x + '\n \n')
            absoluteLinks.append(x)
            pass
        #import pdb; pdb.set_trace()
        minMaxData = [0, 0, 200, 200] #MINWIDTH, MINHEIGHT, MAXWIDTH, MAXHEIGHT

        S = [200, 200, 300, 300]
        M = [300, 300, 500, 500]
        L = [500, 500, 0, 0]

        if imagesToKeep == ['S', 'L']:
            minMaxData = [L[0], L[1], S[2], S[3]]
        elif imagesToKeep == []:
            pass
        else:
            minMaxData = [eval(imagesToKeep[0])[0], eval(imagesToKeep[0])[1], eval(imagesToKeep[-1])[2], eval(imagesToKeep[-1])[3]]

        filePath = 'TweetSorterResults/' + self.mediaType(linkName=linkName) + '.txt'

        loader = XPathItemLoader(item = MicrofiltersAppItem(), response = response)
        loader.add_value('videoIds', videoIds)
        loader.add_value('image_urls', absoluteLinks)
        loader.add_value('content', urlToContent[response.request.meta['redirect_urls'][0]])
        loader.add_value('filePath', filePath)
        loader.add_value('minHeight', minMaxData[1])
        loader.add_value('minWidth', minMaxData[0])
        loader.add_value('maxWidth', minMaxData[2])
        loader.add_value('maxHeight', minMaxData[3])
        return loader.load_item()

    def close_spider(self, spider):
        f = open('/Users/ilyas/Documents/Other.txt', 'rw+')
        content = f.read()
        content = content.replace(',', '')
        content = content.replace('\t', ', ')
        f.write(content)

    def sortChronologically(self):
        files = os.listdir('TweetSorterResults/')
        linesOfLines = []
        for x in files:
            if os.path.isfile('TweetSorterResults/' +x):
                with open('TweetSorterResults/' + x, 'r') as f:
                    contentLines = f.readlines()
                    for line in contentLines:
                        linesOfLines.append(line.split('\t'))
                    linesOfLines.sort(key=lambda x: int(x[2].split(' ')[2])*86400 + int(x[2].split(' ')[3].split(':')[0])*3600 + int(x[2].split(' ')[3].split(':')[1])*60 + int(x[2].split(' ')[3].split(':')[2]))
                with open('TweetSorterResults/' + x, 'w') as f:
                    strsToWrite = []
                    for bigLine in linesOfLines:
                        strsToWrite.append('\t'.join(bigLine))
                    f.write('\n'.join(strsToWrite))

    def sortByRetweets(self):
        files = os.listdir('TweetSorterResults/')
        linesOfLines = []
        for x in files:
            if os.path.isfile('TweetSorterResults/' +x):
                with open('TweetSorterResults/' + x, 'rw') as f:
                    contentLines = f.readlines()
                    content = f.read()
                    for line in contentLines:
                        linesOfLines.append([line, len([m.start() for m in re.finditer(re.escape(line.split('\t')[1]), content)])])
                    print linesOfLines
                    linesOfLines.sort(key=lambda x: int(x[1]))
                with open('TweetSorterResults/' + x, 'w') as f:
                    strsToWrite = []
                    for bigLine in linesOfLines:
                        strsToWrite.append(bigLine[0])
                    f.write('\n'.join(strsToWrite))
                    print linesOfLines


    def spider_closed(self, spider):
        self.csvFunc()
        if sortByGlobal == 'chrono':
            self.sortChronologically()
        elif sortByGlobal == 'RTs':
            self.sortByRetweets()

        return
