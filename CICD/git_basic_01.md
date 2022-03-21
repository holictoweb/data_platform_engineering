# git 설치 

```bash
# 설치
sudo apt-get install git

# 정보 입력  
git config --global user.name joonik
git config --global user.mail holictoweb@gmail.com

# git init 
git config --global user.name "joonik.lee"
git config --global user.email joonik.lee@aicelthech.com

1. mkdir A
2. cd A 
3. git init
git remote add origin https://github.com/fngo-bigfinance/aicel-dashboard.git
    - 원격 저장소 확인 


```

# 현재 git 연결 상태 확인
```bash
git remote -v

```

## git 






### private repo 접근 방법

- user명을 명시해서 진행 필요 
git clone https://holictoweb@github.com/holictoweb/bitlab.git

- token 발급
우측상단 profile -> settings -> Developer Setting -> personal access tokens
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

- 하지만 아래 처럼 비밀번호는 더 이상 사용 할 수 없으며 token을 발급 받아 사용
```
holictoweb@DESKTOP-A2T3JAV:~$ git clone https://holictoweb@github.com/holictoweb/bitlab.git
Cloning into 'bitlab'...
remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
fatal: Authentication failed for 'https://github.com/holictoweb/bitlab.git/'
```


- pull origin master issue

```
joonik77.lee@jupyterhub:~/mfas_CICD$ git pull origin master
Username for 'https://github.sec.samsung.net': joonik77.lee
Password for 'https://joonik77.lee@github.com': 
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), 405 bytes | 405.00 KiB/s, done.
From https://github.sec.samsung.net/mfas/mfas_CICD
 * branch            master     -> FETCH_HEAD
   ***423da7a..88cadb4  master     -> origin/master***
Updating 423da7a..88cadb4
error: Your local changes to the following files would be overwritten by merge:
        test_01.txt
Please commit your changes or stash them before you merge.
Aborting
```

```bash
git stash
# git pull 은 git fetch + git merge
gir pull origin master

git apply stash

-- local master로 pull 
git fetch --all
-- 현재 브런치를 master로 reset
git reset --hard origin/master

```




- pull request conflict 이슈 처리 

```bash
# local 
git reset <commit_id>~1

# local
git push -f origin jooni77.lee

# fetch origin master


```


senaio

1. origin master 변경 commit
2. local branch 변경 commit / push
3. origin branch pull request -> confilct 발생
4. local branch reset commit_id~1
5. git push -f origin branch
6. git pull origin master -> confilc 발생
7. git stash -> git pull origin master -> git stash apply -> confilct 파일 확인
8. 파일 수정 후 commit->push->pull request

