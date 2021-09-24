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

```

