


### remote 설정하기

```bash
git remote add origin https://github.com/fngo-bigfinance/aicel-dashboard.git

```

### git login 

```bash
git config --global user.email "holictoweb@gmail.com"
# git config --global user.password "!1004cjstk" 비밀번호 방식은 사라짐. token 생성 필요 

git config --global --list

```



# error
- error: RPC failed; curl 55 Failed sending data to the peer
```bash
git config --global http.postBuffer 524288000
저는 이 방법으로 해결되었습니다. 오류의 원인은 git config에서 설정한 http.postBuffer 값보다 크기가 큰 파일이 포함되어 있었기 때문이었습니다. 단일 파일 최대 허용 크기를 500MB로 넉넉하게 설정해주어 해결되었습니다.

2. 크기가 50MB 이상인 파일 삭제
1번과 원인은 동일한데, 파일 크기가 훨씬 크거나 명령어가 작동하지 않는 등 해결이 안 되는 경우 파일을 삭제하는 걸 고려해 볼 수 있습니다. 단일 파일의 크기가 50MB 이상인 파일을 삭제해 보시기 바랍니다.

3. git config --global http.version HTTP/1.1
Stack Overflow에서 많은 추천을 받은 해결 방법입니다. 파일 크기와 관련 없이 오류가 발생하는 경우 이 해결 방법을 고려해볼 수 있습니다.
```


- 더이상 존재 하지 않는 파일 삭제
- Git Erroring for large file that does not exist anymore
```py
git filter-branch --tree-filter 'rm -rf notebook/bybit/data/20220920_t.csv' HEAD
```