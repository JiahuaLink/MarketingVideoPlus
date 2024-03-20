# -*- coding: utf-8 -*-
import base64
import random
import re
import time
import zlib
from urllib.parse import quote

import requests

import scrapy
from scrapy import Request
from scrapy.conf import settings
from weixin_0530.items import Weixin0530Item


def make_content_url_weixin(response):

    html = response.text

    pattern = r'content_url":"(.*?)","copyright_stat'

    url_origin = re.findall(pattern, html)

    return url_origin


def make_account_url_weixin(response):

    html = response.text
    pattern = r"url\s\+=\s\'(.+?)';"
    url = re.findall(pattern, html)
    url = ''.join(url)
    return url

def make_url_sogou(href):

    b = int(100 * random.random())
    a = href.index('url=')
    try:
        c = href.index('&k')
    except Exception:
        c = -1
    if a != -1:
        if c == -1:
            begin = a + 4 + 26 + b
            a = href[begin:begin + 1]
        else:
            pass
    else:
        pass
    real_href ='https://weixin.sogou.com'+href +'&k={}&h={}'.format(b, a)
    return real_href

def get_snuid():

    # 此url为在搜狗网站找到的可以持续生成snuid的链接，此url只是给个例子，搜狗网站里这么多网页，多翻翻会有惊喜的
    # 做爬虫要有耐心，去找规律。
    url='https://www.sogou.com'
    headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}
    rst = requests.get(url=url, headers=headers)
    pattern = r'SNUID=(.*?);'
    snuid = re.findall(pattern, str(rst.headers))[0]

    return snuid
# 此处最好放到middleware里
settings.get('DEFAULT_REQUEST_HEADERS')['Cookie']='SUV=1345;SNUID={}'.format(get_snuid())

class WeixinCrawlerSpider(scrapy.Spider):
    name = 'weixin_crawler'
    
    def __init__(self):
        
        self.key_word=quote(settings.get('KEY_WORD'))
        #self.start_urls = ['https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='.format(self.key_word)]
    
    
    def start_requests(self):
        
        for i in range(1,11):
            time.sleep(2)
            url=settings.get('WEIXIN_START_URL').format(self.key_word,str(i))
            yield Request(url=url,callback=self.parse)
        #yield Request(url=self.start_urls[0],callback=self.parse)
    
    
    def parse(self, response):
        urls_list = response.xpath('//div[@class="txt-box"]//a/@href').extract()
        for url in urls_list:
            url=make_url_sogou(url)
            headers = {
                'User-Agent':settings.get('DEFAULT_REQUEST_HEADERS')['User-Agent'],
                # 此处cookie是固定cookie,时效一年,不需要更换
                'Cookie':settings.get('WEIXIN_SOGOU_SECOND_REQUEST_COOKIE'),
                'Referer': setting.get('WEIXIN_SOGOU_SECOND_REQUEST_REFERER').format(self.key_word)
            }
            yield Request(url=url,headers=headers,callback=self.parse_real_url)
        time.sleep(1)


    def parse_real_url(self,response):

        url=make_account_url_weixin(response)
        time.sleep(1)
        yield Request(url=url,callback=self.parse_weixin_url_list,meta={'flag':'weixin'})


    def parse_weixin_url_list(self,response):

        url_origin=make_content_url_weixin(response)
        if len(url_origin) == 0:

            pass

        else:
            print('在在微信公众号spider的parse_weixin_url_list中,请求成功,得到正确响应.成功75%了!')
            # 对于请求到的url进行修改,得到最终正确的url
            for url in url_origin:
                time.sleep(1)
                url = 'https://mp.weixin.qq.com' + url.replace('&amp', '&').replace(';', '')
                try:
                    yield Request(url=url, callback=self.parse_weixin_detail,meta={'flag':'weixin'})
                except Exception as e:
                    print('在微信公众号spider的parse_weixin_url_list中,请求详情页失败:{}'.format(e))
                    
                    
    def parse_weixin_detail(self,response):
        item = Weixin0530Item()
        # 如果请求的url和响应的url相同,则收到正确响应
        print('在在微信公众号spider的parse_weixin_detail中,请求成功,得到正确响应.成功100%了!')
        item['url'] = response.url
        item['origin_length'] = str(len(response.text))
        item['compressed_html'] = str(base64.b64encode(zlib.compress(response.body)).decode())
        item['compressed_length'] = str(len(item['compressed_html']))
        yield item
