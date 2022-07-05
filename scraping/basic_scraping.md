



## chrome driver 설치 

- chrome 설치 
```bash
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -


sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

# 업데이트
sudo apt-get update

sudo apt-get install google-chrome-stable

```

- chrome driver 설치 

```bash
# 크롬 버젼 확인 
google-chrome --version
> Google Chrome 103.0.5060.53 

# 위치 / 버젼 지정 후 다운 로드
wget -N http://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_linux64.zip -P ~/download


# unzip
unzip ~/download/chromedriver_linux64.zip

# lib로 위치 이동
sudo mv chromedriver /usr/bin/chromedriver
```

?????????????? 제대로 안되는디???