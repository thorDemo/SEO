# -*-coding=utf-8-*-
from scrapy import Request
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from junshi_news.items import JunshiNewsItem
import re


class NovelSpider(CrawlSpider):

    name = "newsspider"
    start_urls = ['http://junshi.xilu.com/dfjs/',   # 兵器快讯
                  'http://junshi.xilu.com/rdph/',   # 军事热点
                  'http://junshi.xilu.com/jspzt/',  # 军事精选
                  'http://junshi.xilu.com/wypl/',   # 军迷评论
                  'http://junshi.xilu.com/tsjs/',   # 军事头条
                  'http://junshi.xilu.com/jsgc/',   # 军事观察
                  'http://junshi.xilu.com/shyy/',   # 军史秘闻
                  'http://junshi.xilu.com/jrt/'    # 防务新观察
                  ]
    tips = ''

    # 获取新闻
    def parse(self, response):
        sell = Selector(response)
        list_page = sell.xpath('/html/body/section/div[3]/div[2]/ul/li')
        self.tips = sell.xpath('/html/body/section/div[2]/a[3]/text()').extract()[0]
        for each in list_page:
            url = each.xpath('div[@class="newslist_tit"]/a/@href').extract()[0]
            yield Request(url, callback=self.get_content)
        # 下一页
        try:
            print('读取下级页面')
            list_url = sell.xpath('html/body/section/div[3]/div[4]/div/ul/li[8]/a/@href').extract()[0]
        except:
            print('读取首页')
            list_url = sell.xpath('/html/body/section/div[3]/div[4]/div/ul/li[6]/a/@href').extract()[0]
            print(list_url)

        yield Request(url=list_url, callback=self.parse)

    def get_content(self, response):
        item = JunshiNewsItem()
        sell = Selector(response)
        title = sell.xpath('/html/head/title/text()').extract()[0]
        content = sell.xpath('//*[@id="xilucontentid"]/p')
        news_time = sell.xpath('//div[@class="newsinfo_con"]/div[3]/text()').extract()[0]
        print(news_time)
        tips = self.tips
        text = ''
        img_url = ''
        for line in content:
            try:
                text += str(line.xpath('string(.)').extract()[0]).strip('\n') + '\n'
                img_url += line.xpath('a/img/@src').extract()[0] + '\n'
                img_alt = line.xpath('a/img/@alt').extract()[0]
                text += '<img alt="%s"></img>\n' % img_alt
            except IndexError:
                try:
                    img_url += line.xpath('img/@src').extract()[0] + '\n'
                    img_alt = line.xpath('img/@alt').extract()[0]
                    text += '<img alt="%s"></img>\n' % img_alt
                except IndexError:
                    try:
                        img_url += line.xpath('img/@data-mcesrc').extract()[0] + '\n'
                        img_alt = line.xpath('img/@alt').extract()[0]
                        text += '<img alt="%s"></img>\n' % img_alt
                    except IndexError:
                        pass
        item['img_url'] = img_url
        item['title'] = title
        item['content'] = text
        item['tips'] = tips
        item['news_time'] = news_time
        page_url = sell.xpath('//a[@class="up"]').extract()
        next_page_url = ''
        for line in page_url:
            url = re.findall('<a href="(.*?)" class="up">下一页</a>', line)[0]
            if url:
                next_page_url = url
        print('next_page_url = %s' % next_page_url)
        if next_page_url:
            yield Request(url=next_page_url, callback=self.get_next_page, meta={'item': item})

    def get_next_page(self, response):
        item = response.meta['item']
        text = item['content']
        img_url = item['img_url']
        sell = Selector(response)
        content = sell.xpath('//*[@id="xilucontentid"]/p')
        for line in content:
            try:
                text += str(line.xpath('string(.)').extract()[0]).strip('\n') + '\n'
                img_url += line.xpath('a/img/@src').extract()[0] + '\n'
                img_alt = line.xpath('a/img/@alt').extract()[0]
                text += '<img alt="%s"></img>\n' % img_alt
            except Exception as e:
                # print(e)
                pass
        item['img_url'] = img_url
        item['content'] = text
        page_url = sell.xpath('//a[@class="up"]').extract()
        next_page_url = ''
        try:
            for line in page_url:
                url = re.findall('<a href="(.*?)" class="up">下一页</a>', line)[0]
                if url:
                    next_page_url = url
            print('next_page_url = %s' % next_page_url)
            if next_page_url:
                yield Request(url=next_page_url, callback=self.get_next_page, meta={'item': item})
            else:
                yield item
        except IndexError:
            yield item
