# 기업 집단 정보 (공정거래위원회)

```py
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.2f}'.format
pd.set_option('mode.chained_assignment',  None)

remote_url = f"http://apis.data.go.kr/1130000/appnGroupSttusList/appnGroupSttusListApi?serviceKey={service_encoding_key}&pageNo=1&numOfRows=200&presentnYear=202105"
data = requests.get(remote_url)
soup = BeautifulSoup(data.text, "html.parser")
# print(soup)

unity_group = []
for item in soup.find_all("appngroupsttus"):
    unitygrupnm = item.find("unitygrupnm").text
    unitygrupcode = item.find("unitygrupcode").text
    smernm = item.find("smernm").text
    reprecmpny = item.find("reprecmpny").text
    sumcmpnyco = item.find("sumcmpnyco").text
    
    unity_group.append([unitygrupnm, unitygrupcode, smernm, reprecmpny, sumcmpnyco])
    

df_group = pd.DataFrame(unity_group, columns=['unitygrupnm', 'unitygrupcode', 'smernm', 'reprecmpny', 'sumcmpnyco'])

# display(df_group)
data_list = []
for idx, row in df_group.iterrows():
    unitygrupcode = row['unitygrupcode']
    remote_url = f"http://apis.data.go.kr/1130000/affiliationCompSttusList/affiliationCompSttusListApi?serviceKey={service_encoding_key}&pageNo=1&numOfRows=200&presentnYear=202105&unityGrupCode={unitygrupcode}"
    data = requests.get(remote_url)
    soup = BeautifulSoup(data.text, "html.parser")
    # print(soup)
    
    for item in soup.find_all("affiliationcompsttus"):
        row_list = []
        data_column = []
        for tag in item.find_all():
            row_list.append(item.find(tag.name).text)
            data_column.append(tag.name)
        
        data_list.append(  [row['unitygrupnm'], row['unitygrupcode'] , row['smernm'], row['reprecmpny']] + row_list)
        
df_group_company = pd.DataFrame(data_list, columns =  ['unitygrupnm', 'unitygrupcode', 'smernm', 'reprecmpny' ] + data_column)

display(df_group_company)
```

# 자회사 기업 (공정거래위원회)
```py


news_con = pymysql.connect(host='fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com',
            user='admin',
            password='finance2016!',
            database='news',
            cursorclass=pymysql.cursors.DictCursor
            )

sql_company = '''
select * from news.gn_company_overview
'''

news_cur = news_con.cursor()
news_cur.execute(sql_company)
res = news_cur.fetchall()

df_overview = pd.DataFrame(res)
df_overview = df_overview.loc[df_overview.jurir_no != '' , ['jurir_no', 'stock_name', 'stock_code', 'corp_cls']]
# display(df_company.head(3))


heading_properties = [('font-size', '10px')]

cell_properties = [('font-size', '9px')]
pd.set_option('display.max_rows', 100)


service_encoding_key = 'BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D'
service_decoding_key = 'BHI55TQtFP6CNuCQwbnJk0KO44OKicqy/t0TTtjF6WvIEGS5OzxwItbF0STlJ+4v8G9egSBots4E6xF/4ATJig=='

# 공개 일자에 대한 부분도 공공데이터 포탈에서 받아야함. 
present_year = '202104'


# 전체 데이터 수집 
remote_url = f"http://apis.data.go.kr/1130000/holdingProgCompSttusList/holdingProgCompSttusListApi?serviceKey={service_encoding_key}&pageNo=1&numOfRows=6000&presentnYm={present_year}"
    
#local_file = row.corp_code+'.zip'
data = requests.get(remote_url)
soup = BeautifulSoup(data.text, "html.parser")
# pprint(soup)
compnayList = []
for item in soup.find_all("holdingprogcompsttus"):
    jurirno = item.find("jurirno").text
    companyname = item.find("cdpnynm").text
    hldcpsenm = item.find("hldcpsenm").text
    cdpnyjurirno = item.find("cdpnyjurirno").text
    cdpnyqotarate = item.find("cdpnyqotarate").text
    parentjurirno = item.find("parentjurirno").text
    fnncsenm = item.find("fnncsenm").text
    compnayList.append([jurirno, parentjurirno, companyname, cdpnyjurirno, hldcpsenm, cdpnyqotarate, fnncsenm])

holdings_columns = ['jurir_no', 'parent_jurir_no', 'sub_company_name', 'cdpny_jurir_no', 'type', 'qota_rate', 'fnncsenm']
df_holdings = pd.DataFrame(compnayList, columns=holdings_columns)
print(len(df_holdings))
df_merge_parent = pd.merge(df_holdings, df_overview, how='left', on='jurir_no', indicator=True)
print(len(df_merge_parent))


df_merge = pd.merge(df_merge_parent[['stock_name', 'stock_code'] + holdings_columns ], df_overview, how='left', left_on='cdpny_jurir_no', right_on='jurir_no', indicator=True)

df_merge.rename(columns = {'stock_name_x': 'stock_name', 'stock_code_x': 'stock_code', 'jurir_no_x': 'jurir_no', 'stock_name_y': 'sub_stock_name', 'stock_code_y': 'sub_stock_code'}, inplace = True)
result_columns = ['stock_name', 'stock_code', 'jurir_no', 'sub_stock_name', 'sub_stock_code', 'corp_cls', 'parent_jurir_no', 'cdpny_jurir_no',  'sub_company_name', 'type', 'qota_rate', 'fnncsenm']
df_result = df_merge[result_columns]
df_result.fillna('', inplace=True)

display(df_result.style.set_table_attributes('style="font-size: 10px"'))

db_connection_str = 'mysql+pymysql://admin:finance2016!@fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/news'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()

df_result.to_sql(name='gn_company_sub', con=db_connection, if_exists='append',index=False)
```


# 계열사 정보
```py
# 계열사 정보 
service_encoding_key = 'BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D'
jurirno = '1301110006246'
remote_url = f"http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService/getAffiliate?serviceKey={service_encoding_key}&pageNo=1&numOfRows=10000&resultType=xml&basDt=20210117"

data = requests.get(remote_url)
soup = BeautifulSoup(data.text, "html.parser")

# pprint(soup)

compnayList = []
for item in soup.find_all("item"):
    afilcmpycrno = item.find("afilcmpycrno").text
    afilcmpynm = item.find("afilcmpynm").text
    crno = item.find("crno").text
    compnayList.append([afilcmpycrno, afilcmpynm, crno])
    

df_company = pd.DataFrame(compnayList, columns=['afilcmpycrno', 'afilcmpynm', 'crno'])
df_merge = pd.merge(df_company, df_overview, how='left', left_on='crno', right_on='jurir_no', indicator=True)

display(df_merge.loc[df_merge['_merge'] != 'right_only'].style.set_table_attributes('style="font-size: 9px"'))
    
```