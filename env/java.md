## java home 설정

```bash
# 설치
sudo apt-get install openjdk-8-jdk

# .bashrc 파일 수정
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

export PATH="$PATH:$JAVA_HOME/bin"

# 적용하기
source ~/.bashrc
```