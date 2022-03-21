# 설치

### ubuntu 설치

- 우분투 버젼 확인
```bash
lsb_release -a
```



### MongoDB public GPG key 확인 
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
```

```bash
# repo 확인을 위한 list 생성 
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list


sudo apt-get update

# 설치 
sudo apt-get install -y mongodb-org


# init 시스템 확인 
ps --no-headers -o comm 1


# 실행
sudo systemctl start mongod
# 상태 확인
sudo systemctl status mongod

# conf 위치 확인
ubuntu@ip-172-31-15-162:~/DEV/fargate_crawlers$ sudo systemctl status mongod

● mongod.service - MongoDB Database Server
     Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset: enabled)
     Active: active (running) since Fri 2021-09-24 00:48:42 UTC; 19min ago
       Docs: https://docs.mongodb.org/manual
   Main PID: 911822 (mongod)
     Memory: 62.3M
     CGroup: /system.slice/mongod.service
             └─911822 /usr/bin/mongod --config /etc/mongod.conf


```

## 계정 생성 및 외부 연결

```sql
use admin

db.createUser({ user: "root", pwd: "01234567890", roles:["dbAdminAnyDatabase"] } )
```



# 기본 사용 

```sql 
show dbs
use <db명>
show tables

# collection 생성 
db.createCollection("[COLLECTION_NAME]")




```

# mongo shell 연결

```bash
mongo --host tf-dev-docdb-cluster-vst.cluster-c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com:27017 -u root -p eeee
```

# pymongo
## CRUD
```python
# # 저장 - 예시
doc = {'name':'bobby','age':21}
db.users.insert_one(doc)
#
# # 한 개 찾기 - 예시
user = db.users.find_one({'name':'bobby'})
#
# # 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
same_ages = list(db.users.find({'age':21},{'_id':False}))
#
# # 바꾸기 - 예시
db.users.update_one({'name':'bobby'},{'$set':{'age':19}})
#
# # 지우기 - 예시
db.users.delete_one({'name':'bobby'})

# 전체 삭제
x = mycol.delete_many({})
```

## 집계

```python
count = mdb.naver_news.estimated_document_count()
print(count)
```