## git 



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

```
git stash
gir pull origin master
git apply stash

-- local master로 pull 
git fetch --all
-- 현재 브런치를 master로 reset
git reset --hard origin/master  or git reset --hard origin master

```




- conflict 이슈 처리 

