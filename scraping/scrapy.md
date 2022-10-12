


### scrapy 프로젝트 기본 구조
- item.py: 크롤링할 데이터를 저장하는 기능을 하는 객체의 클래스를 정의하는 곳입니다.
- middlewares.py: scrapy의 커스텀 middleware의 기능을 정의하는 곳입니다. middleware는 다시 한 번 이야기하자면 engine에서 다른 모듈로 request와 response 정보가 교환될 때 지나가는 중간 통로입니다.
- pipelines.py: item pipelines의 커스텀 모듈을 정의하는 곳입니다. pipeline은 item이 다른 저장소로 저장될 때 거치는 통로라고 생각하면 됩니다.
- settings.py: 현재 scrapy 프로젝트의 설정을 하는 파이썬 파일입니다.
- scrapy.cfg: scrapy 프로젝트들의 전체적인 설정을 하는 곳입니다. 어떤 프로젝트가 어떤 설정을 따를 것인지 배포는 어떤 식으로 할 것인지를 정합니다.

출처: https://engkimbs.tistory.com/897 [새로비:티스토리]

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FnMywK%2FbtqEbuwSIK8%2F0mhmM8tG1YEvWjZ51IvWO1%2Fimg.png)


## 프로젝트 생성
```bash
pip install scrapy

# 1. 프로젝트 생성
scrapy startproject aicel_scrapy 

# 2. 스파이더 생성
# 뒤에 path 는 포함되지 않음. 
scrapy genspider thebell https://www.thebell.co.kr/free/content/Search.asp?keyword=삼성전자

scrapy genspider droom_naver_meta https://finance.naver.com/item/board.naver?code=005930


# 3. robot.txt 
settings.py 에서 ROBOTSTXT_OBEY 설정을 False로 변경
scrapy crawl thebell
# 혹은 실행 시 설정
scrapy crawl --set=ROBOTSTXT_OBEY='False' thebell

```

# scrapy 실행
### 1. spider 구성 
```py
import scrapy
from aicel_scrapy.items import TheBellListItem, TheBellPostItem


import pymysql
from pymysql.constants import CLIENT
from pprint import pprint 

class ThebellSpider(scrapy.Spider):
    name = 'thebell'
    allowed_domains = ['www.thebell.co.kr']
    start_urls = ['https://www.thebell.co.kr/free/content/Search.asp?keyword=삼성전자']

    def parse(self, response)
        # content_list = response.xpath('//*[@id="contents"]/div[3]/div/div[1]/div[1]/div[2]/ul/li')
        content_list = response.xpath("//div[contains(@class, 'listBox')]/ul/li")
        # pprint(content_list)
        for sel in content_list :
            # print(sel)

            post_url = sel.xpath('dl/a/@href').get().strip()
            title = sel.xpath('dl/a/dt/text()').get().strip()
            summary = sel.xpath('dl/a/dd/text()').get().strip()
            create_date = sel.xpath("dl/dd[contains(@class, 'userBox')]/span[contains(@class, 'date')]/text()").get().strip()
            
            thebell_list_item = TheBellListItem()
            thebell_list_item["url"] = 'https://www.thebell.co.kr/free/content/' + post_url
            thebell_list_item["date"] = create_date

            yield thebell_list_item

        # 상세 페이지 주소 
        # https://www.thebell.co.kr/free/content/ArticleView.asp?key=202206160824450220105694&lcode=00&page=1&svccode=00

        pass

```

### 2. item 구성 

```py
class TheBellListItem(Item):
    url = Field()
    date = Field()


class TheBellNewsItem(Item):
    url = Field()  # string
    body = Field()  # JSON
    created_at = Field()  # datetime
```
### 3. pipeline 구성
- 파이프라인에서 실제 처리 해야하는 item 유형을 체크 하여 처리 파이프라인 skip
```py
class TheBellListPipeline:
    def __init__(self):
        print('init')

    def process_item(self, item, spider):
        if not isinstance(item, TheBellListItem):
            return item
        print(20*'-' + 'TheBellListPipeline ' + 20*'-')
        print(item['url'])2

        return item

class TheBellNewsPipeline:
    def __init__(self):
        print('init')

    def process_item(self, item, spider):
        if not isinstance(item, TheBellNewsItem):
            return item
        print(20*'-' + 'TheBellNewsPipeline ' + 20*'-')
        return item 
```



#### 다이나믹 페이지 액션 처리
- https://stackoverflow.com/questions/36874494/simulating-a-javascript-button-click-with-scrapy




### scrapy asyncio
- https://docs.scrapy.org/en/latest/topics/asyncio.html

```bash

```


# 부가 기능

## scrapyd 설치 
- rest api 제공 및 web 관리 화면 제공


```py
pip install scrapyd
# config 변경
# /home/ubuntu/anaconda3/envs/dev_scrapy/lib/python3.8/site-packages/scrapyd
# default_scrapyd.conf 파일 수정  
bind_address = 0.0.0.0

```

### csv 로 내보내기
- setting.py 설정
```py
FEED_FORMAT = "csv"
FEED_URI = "naver_news.csv"
```

### 크롤링 작업과 동시에 파일 저장
```py
scrapy crawl dmoz -o items.json
```


# sample code

# selector
- https://docs.scrapy.org/en/latest/topics/selectors.html

```py
```