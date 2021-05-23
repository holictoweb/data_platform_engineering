## google drive 연동 


0. google console 
https://console.cloud.google.com/

1. google drive api 활성

- 링크에 접속 하여 project 생성 
https://console.cloud.google.com/flows/enableapi?apiid=drive&pli=1

- API 및 서비스로 이동 ( 좌측 상단 햄버거 ) 
  - API 및 서비스 사용설정 click -> google drive 검색 -> 사용 

- credential 생성
  - 해당 API 및 서비스 -> 사용자 인증정보 만들기 -> 서비스 계정 생성 (권한 소유자 ) 
  - 서비스계정 선택 -> 키 -> 새키 생성 -> json 으로 로컬 저장 


   


2. client 설치 

```shell 
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```




3. google drive mount - colab
```python
from google.colab import drive
drive.mount('/gdrive', force_remount=True)

```
