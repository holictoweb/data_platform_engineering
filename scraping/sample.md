```py
import scrapy
from aicel_scrapy.items import DroomNaverMetaItem, TheBellListItem
from datetime import datetime, timedelta
from pytz import timezone   

from pprint import pprint 
from json import loads, dumps
import urllib
import hashlib

import pandas as pd
import time
import re

class DroomNaverMetaSpider(scrapy.Spider):
    name = 'droom_naver_meta_backup'
    allowed_domains = ['finance.naver.com']
    # start_urls = ['https://finance.naver.com/']
    
    def __init__(self) -> None:
        super().__init__()
        

    def start_requests(self):
        print('-'*20 + 'start request meta')
        while 1:
            try:
                print('GET one msg readed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                msg = next(self.consumer)
                print('one msg readed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            except Exception as e:
                print('no more to read!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(e)
                break
            recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            print('>'*60 +f"\n {recv}")
            yield scrapy.Request(
                        url='https://finance.naver.com/item/board.naver?code=005930',
                        method='POST',
                        dont_filter=True,
                        # headers=self.headers,
                        # cb_kwargs={'company_code':msg.value["company_code"]},
                        callback=self.parse
                        )
        
            
    def parse(self, response):
        # tr_list = response.xpath("//div[contains(@class, 'listBox')]/ul/li")
        # tr_list = response.xpath("//meta[contains(@property, 'og:title')]").attrib["content"]
        # tr_list = response.xpath("//head/title")
        print('callback parse start =======================================')
        tr_list = response.xpath("//table[contains(@class, 'type2')]/tbody/tr[td/a]")

        is_finished = False
        
        for tr in tr_list:
            td_list = tr.xpath("./td")

            a = td_list[1].xpath("./a")
            url = (
                "https://finance.naver.com"
                f"{a.xpath('./@href').get().split('&st=')[0]}"
            )
            # print(url)
            
            
            if tr.xpath("./td[contains(@class, 'title')]/a/span/b/text()").get() is None :
                comment = 0 
            else:
                comment = tr.xpath("./td[contains(@class, 'title')]/a/span/b/text()").get()
            
            url_parse = urllib.parse.urlparse(url)
            query = urllib.parse.parse_qs(url_parse.query)
            key_code = query['code'][0]
            key_nid = query['nid'][0]
            post_id_md5 = hashlib.md5(f"naver&{key_code}&{key_nid}".encode("utf8")).hexdigest()
            
            droom_naver_meta_item = DroomNaverMetaItem()
            droom_naver_meta_item["post_id_md5"] = post_id_md5
            droom_naver_meta_item["title"] = tr.xpath("./td[contains(@class, 'title')]/a").attrib["title"]
            droom_naver_meta_item["views"] = td_list[3].xpath("./span/text()").get()
            droom_naver_meta_item["good"] = td_list[4].xpath("./strong/text()").get()
            droom_naver_meta_item["bad"] = td_list[5].xpath("./strong/text()").get()
            droom_naver_meta_item["comment"] = str(comment)
            droom_naver_meta_item["published_at"] = published_at
            droom_naver_meta_item["crawled_at"] = now
            droom_naver_meta_item["provider"] = 'NAVER'
            droom_naver_meta_item["company_code"] = company_code
            droom_naver_meta_item["delivery_url"] = url
            
            pprint(droom_naver_meta_item)

            # yield droom_naver_meta_item

```