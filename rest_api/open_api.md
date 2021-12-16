# open api 



- 공공데이터 포탈

https://www.data.go.kr/index.do

- 인증키 

```
BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D
```



# DART 인증

5e99205e2b9885da9519dd55c253d9a7d70fbab3

```bash
# 코드 정보 조회
https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=5e99205e2b9885da9519dd55c253d9a7d70fbab3
```





# open api -> database

```python
# -*- conding:utf-8 -*-'
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
import pymysql

startpg = 1
endpg = 1000
rows = []
key = '5e99205e2b9885da9519dd55c253d9a7d70fbab3'
for _ in range(12):
    url = f"http://openapi.seoul.go.kr:8088/[api key]/xml/busStopLocationXyInfo/{startpg}/{endpg}"

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    for i in soup.find_all('row'):
        rows.append({"stop_no": i.stop_no.string,
                     "stop_nm": i.stop_nm.string,
                     "xcode": i.xcode.string,
                     "ycode": i.ycode.string})
    startpg = endpg + 1
    endpg = endpg + 1000

columns = ["stop_no", "stop_nm", "xcode", "ycode"]
bus_stop_df = pd.DataFrame(rows, columns=columns)
# bus_stop_df
# bus_stop_df.to_csv("bus_stop.csv", mode='w', encoding='utf-8-sig', index=False)

engine = create_engine("mysql+mysqldb://<db id>:"+"<password>" +
                       "@<ip_address>/<db_name>?charset=utf8", encoding='utf8')
conn = engine.connect()

bus_stop_df.to_sql(name='<table_name>', con=engine,
                   if_exists='replace', index=False)
```





# 공시 정보 조회 ( 공시 문서 번호 확인 )



```python
bgn_date = '20190101'
end_date = '20201231'


# load mysql TABLE 
db_connection_str = 'mysql+pymysql://admin:finance2016!@fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/news'
db_connection = create_engine(db_connection_str)

bigf_db_connection_str = 'mysql+pymysql://fngo:fngofinance@bigfinance-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/fngo'
bigf_db_connection = create_engine(bigf_db_connection_str)


sql = '''
select * from dart_corp_code
where length(stock_code) > 0
order by modify_date desc
'''

df = pd.read_sql_query(sql , db_connection )
df = df.astype({'corp_code':'object'})

sql_company = 'select SUBSTR(company_code,2) as company_code from fngo.company where is_trading = 1 '
df_company = pd.read_sql_query(sql_company , bigf_db_connection )
company_list = df_company['company_code'].to_list()

# print(company_list)
#display(df)

logger.info("target_report started ")


df_result = pd.DataFrame()
for idx, row in df.iterrows():
    stock_code = str(round(row.stock_code))
    if len(stock_code) != 6:
        for i in range(6 - len(stock_code)):
            stock_code = '0' + stock_code
    
    #print(stock_code)
    
    if stock_code in company_list:
        #print(stock_code)
        
        #print(row.corp_code)
        corp_code = str(row.corp_code)
        if len(corp_code) != 8:
            for i in range(8 - len(corp_code)):
                corp_code = '0' + corp_code
                
        # 기재정정 문서가 존재 하지 않는 현상으로 last가 아닌 전체 사업보고서 다운로드
        # last_reprt_at=Y 
        remote_url = f"https://opendart.fss.or.kr/api/list.json?crtfc_key={crtfc_key}&corp_code={corp_code}&bgn_de={bgn_date}&end_de={end_date}&pblntf_ty=A&last_reprt_at=N&page_count=100"
        #local_file = row.corp_code+'.zip'
        data = requests.get(remote_url)
        #pprint(data.text)
        json_data = json.loads(data.text)
        if json_data['status'] == '000':
            df_result = df_result.append(json_data['list'], ignore_index=True)    
    
    time.sleep(0.5)
    
print(len(df_result))
display(df_result.head(100))
df_result.to_csv('../data/target_report.csv')
logger.info("target_report finished ")
```



# 공시 서류 원본 파일 다운로드

```python
########################################################### elastic search
host = 'search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'ap-northeast-2' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

oss_client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# for idx, row in df_crawled.iterrows():
#     #print(row.to_json(force_ascii=False))
#     search.index(index="naver_news", doc_type="_doc", body=row.to_json(force_ascii=False))
########################################################### elastic search

# csv 파일 읽을 경우 발생 하는 타입 차이에 대한 확인 필요 
df_result = pd.read_csv('../data/target_report.csv')

df_report = pd.DataFrame()
for idx, row in df_result.iterrows():
    
    if idx < 13486:
        continue
    
    # 1. open dart api 호출
    rcept_no = row.rcept_no
    remote_url = f"	https://opendart.fss.or.kr/api/document.xml?crtfc_key={crtfc_key}&rcept_no={rcept_no}"
    data = requests.get(remote_url)
    
    # 2. corp code 로 파일명을 생성하여 파일 생성 
    # csv 데이터 이상에 따른 처리 개선 시 제거 
    corp_code = str(row.corp_code)
    if len(corp_code) != 8:
        for i in range(8 - len(corp_code)):
            corp_code = '0' + corp_code

    local_file = str(row.rcept_dt) + corp_code + '.zip'
    
    with open(local_path + local_file, 'wb')as file:
        file.write(data.content)
    
    try:
        # 3. 다운 받은 파일을 unzip 후 zip 파일 삭제 
        res = os.system(f'unzip {local_path + local_file} -d {local_path}' )
        os.system(f'rm {local_path + local_file}' )
        
        # 4. 압축 푼 xml 파일 중 사업보고서 파일만 확인 
        # 실제 다운 받은 경우 [첨부 정정]의 경우 사업보고서 이외 파일만 있는 경우도 발생
        report_file = local_path + str(row.rcept_no) + '.xml'
        if os.path.exists(report_file):
            # read xml file ( euc-kr )
            with open(report_file, mode="r", encoding="euc-kr") as fp:
                soup = BeautifulSoup(fp, 'xml')
            report_text = soup.find_all(text=True)
            report_text = ' '.join(report_text)
            #print(report_text[:1000])
            row['report'] = report_text
            
            oss_client.index(index="dart_report_prod", doc_type="_doc", id = rcept_no, body=row.to_json(force_ascii=False))
            
            # delete uploaded file
            os.system(f'rm {local_path + str(row.rcept_no)}*')
            
            df_report = df_report.append(row)
            logger.info(f'index : {idx}, corp_code : {corp_code}, rcept_no : {rcept_no}, rcept_dt : {row.rcept_dt}')
    except:
        print(f'rcept_no : {rcept_no}')
        logger.info(f'error rcept_no : {rcept_no}')
        
    time.sleep(0.5)
    
display(df_report)

    
    
```



# api 사용방법





## 기업개황 API

https://opendart.fss.or.kr/api/company?crtfc_key=BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D

https://opendart.fss.or.kr/api/company.json?crtfc_key=BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D





https://opendart.fss.or.kr/api/corpCode.xml/BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D

