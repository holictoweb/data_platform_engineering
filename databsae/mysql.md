[install mysql](#install-mysql)





# Install MySQL

- 설치 
```bash
# 버젼 확인 
lsb_release -a


# mysql server 설치 - client도 함께 설치 
sudo apt-get install mysql-server

# 설치 후 path 에 대한 부분 확인 필요 

# 보안 관련 설정 ( root 비밀번호 설정 등 )
sudo mysql_secure_installation


```

- 실행 방법 
```bash
# mysql 실행 
sudo systemctl start mysql

# 
sudo /usr/bin/mysql -u root -p

```

