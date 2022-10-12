

# date range 생성
- date range list 생성 
```py

from datetime import datetime, timedelta
from pprint import pprint

base = datetime.today()
date_list = [base - timedelta(days=x) for x in range(10)]

# pprint(date_list)

for ddate in date_list:
    print(ddate.strftime('%Y-%m-%d'))


```

- 특정 시점 부터 range 생성


```py
# date diff from today
from datetime import datetime 
from pytz import timezone
import pytz

now = datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None) #.strftime('%Y-%m-%d')

start = datetime.strptime('20120101', '%Y%m%d')
print(now , start)

delta = now - start
print(delta.days)

```