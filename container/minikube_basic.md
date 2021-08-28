# minikube 설치


- 기본적으로 가상화 기능 활성화 여부 확인

```
grep -E --color 'vmx|svm' /proc/cpuinfo
```


Dokcer 설치 
```
# docker 설치
sudo apt install docker.io -y

# docker user 설정 
﻿sudo usermod -aG docker $USER && newgrp docker


```
