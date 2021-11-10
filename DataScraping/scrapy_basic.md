# pyscrapy 설치



```bash
# scrapy 설치
pip install Scrapy
pip install protego

#프로젝트 생성
scrapy start project naver_news

├── naver_news
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       └── __init__.py
└── scrapy.cfg
```

# spider class 생성

- Scrapy 프레임워크에서는 Spider 클래스를 상속해서 서브 클래스를 만들고 활용
- naver news scraping

```python
import scrapy

class NaverNewsSpider(scrapy.Spider):
    name = 'navernews'
    start_url = ["https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EB%A1%9C%EB%82%9819&oquery=%EC%BD%94%EB%A1%9C%EB%82%9819&sort=1&pd=3&ds=2021.01.01&de=2021.01.01"]

    def parse(self, response):
        # news list 
        title = response.css('#sp_nws1 > div > div > a')
        print(title)
   - 
```

```python
#settings.py 변경 
ROBOTSTXT_OBEY = True
```

- 실행

```bash
scrapy crawl [spider name] --nolog
```



# selector 사용법

```
```

