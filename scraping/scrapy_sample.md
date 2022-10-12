```py
import scrapy
from aicel_scrapy.items import TheBellListItem, TheBellNewsItem
from datetime import datetime 
from pytz import timezone
import pymysql
from pymysql.constants import CLIENT
from pprint import pprint 
import urllib
import hashlib

from scrapy.http import Request

import kafka

class ThebellSpider(scrapy.Spider):
    name = 'thebell'
    allowed_domains = ['www.thebell.co.kr']
    # start_urls = ['https://www.thebell.co.kr/free/content/Search.asp?page=&sdt=7&period=7&part=A&keyword=']

    def start_requests(self):
        # consumer = kafka.KafkaConsumer(
        #     'news.thebell.newslist',
        #     bootstrap_servers=['b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092'],
        #     group_id='thebell-consumer-group',
        #     enable_auto_commit=True
        #     # auto_offset_reset='earliest',
        #     #  value_deserializer=lambda x: loads(x.decode('utf-8')),
        #     #  consumer_timeout_ms=1000
        # )
        # for msg in consumer:
        #     recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        #     print(recv)

        # MySQL 상에 연결된 대상에 대한 수집 진행
        tickers = ['CNS']

        for ticker in tickers:
            yield scrapy.Request(
                            url='https://www.thebell.co.kr/free/content/Search.asp?page=&sdt=7&period=7&part=A&keyword=' + ticker,
                            method='POST',
                            dont_filter=True,
                            # headers=self.headers,
                            # cb_kwargs=self.body,
                            callback=self.parse
                            )
    
    def parse(self, response):
        # content_list = response.xpath('//*[@id="contents"]/div[3]/div/div[1]/div[1]/div[2]/ul/li')
        content_list = response.xpath("//div[contains(@class, 'listBox')]/ul/li")
        # pprint(content_list)
        for sel in content_list :
            # print(sel)

            post_url_query = sel.xpath('dl/a/@href').get().strip()
            title = sel.xpath('dl/a/dt/text()').get().strip()
            summary = sel.xpath('dl/a/dd/text()').get().strip()
            create_date = sel.xpath("dl/dd[contains(@class, 'userBox')]/span[contains(@class, 'date')]/text()").get().strip()
            
            # https://www.thebell.co.kr/free/content/ArticleView.asp?key=202206270822321560109086&lcode=00&page=1&svccode=00

            # 상세 페이지 url을 통해 md5 계산 
            url_parse = urllib.parse.urlparse(post_url_query)
            query = urllib.parse.parse_qs(url_parse.query)
            key_id = query['key'][0]
            news_url_md5 = hashlib.md5(f"thebell&{key_id}".encode("utf8")).hexdigest()

            thebell_list_item = TheBellListItem()
            thebell_list_item["news_url_md5"] = news_url_md5
            thebell_list_item["url"] = 'https://www.thebell.co.kr/free/content/' + post_url_query
            thebell_list_item["title"] = title
            thebell_list_item["published_at"] = create_date
            thebell_list_item["crawled_at"] = datetime.strftime( datetime.now(timezone("Asia/Seoul")), '%Y-%m-%d %H:%M:%S')
            
            yield thebell_list_item

        # 상세 페이지 주소 
        # https://www.thebell.co.kr/free/content/ArticleView.asp?key=202206160824450220105694&lcode=00&page=1&svccode=00

        # search page url
        # https://www.thebell.co.kr/free/content/Search.asp?page=&sdt=&period=180&part=A&keyword=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90

        # 현재 페이지 정보에 있는 페이지는 모두 확인 필요 

        #  https://www.thebell.co.kr/free/content/Search.asp?page=&sdt=90&period=90&part=A&keyword=삼성전자

        
        next_page_id = response.xpath("//div[contains(@class, 'paging')]/em/following-sibling::a[contains(@class, 'btnPage')][1]/text()").get()

        if next_page_id is not None:
            print('='*60 + next_page_id)
            next_page_url = f"https://www.thebell.co.kr/free/content/Search.asp?page={next_page_id}&sdt=7&period=7&part=A&keyword=CNS"
            yield response.follow(next_page_url, callback=self.parse)




```


# pipeline 
```py
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from aicel_scrapy.items import TheBellListItem, TheBellNewsItem

from kafka import KafkaProducer
import json

import asyncio
# from scrapy.utils.defer import maybe_deferred_to_future
# https://doc.scrapy.org/en/latest/topics/item-pipeline.html#take-screenshot-of-item

class AicelScrapyPipeline:
    def process_item(self, item, spider):
        print('>>> Pipeline')
        return item




class TheBellListPipeline:
    def __init__(self):
        # connect to mysql dev
        self.bootstrap =['b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092']
        # connect to msk

    async def process_item(self, item, spider):
        if not isinstance(item, TheBellListItem):
            return item
        
        print(20*'-' + 'TheBellListPipeline ' + 20*'-')

        # def serializer(message):
        #     return json.dumps(message).encode('utf-8')

        # Kafka Producer
        producer = KafkaProducer(
            bootstrap_servers=['b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092'],
            value_serializer=lambda x : json.dumps(x).encode()
        )

        producer.send('news.thebell.newslist', dict(item))
        producer.close()

        return item
        # yield item


class TheBellNewsPipeline:
    def __init__(self):
        print('init')

    async def process_item(self, item, spider):
        if not isinstance(item, TheBellNewsItem):
            return item
        print(20*'-' + 'TheBellNewsPipeline ' + 20*'-')

        # Kafka Producer
        producer = KafkaProducer(
            bootstrap_servers=['b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092'],
            value_serializer=lambda x : json.dumps(x).encode()
        )

        producer.send('news.thebell.newspage', dict(item))
        producer.close()

        # mongo db상에 데이터 저장 

        return item

```
