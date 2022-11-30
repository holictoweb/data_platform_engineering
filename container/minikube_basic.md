# minikube 제공 기능

Minikube 는 Kubernetes 기능중 아래 것들을 제공해 준다.

- DNS
- NodePorts
- ConfigMaps and Secrets
- Dashboards
- Container Runtime: Docker, CRI-O, and containerd
- Enabling CNI (Container Network Interface)
- Ingress


# minikube 설치

- 기본적으로 가상화 기능 활성화 여부 확인

1. docker 설치 확인 

2. minikube 설치 
- 2022-11-16
```bash
# lastest version
sudo curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

# 실행 driver 선택 확인 
minikube start --driver=docker
minikube start

# 상태 확인 
minikube status

# ssh 접속
minikube ssh
```


```bash
sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/

# k8s 1.21.2 부터 필수 설치
#   Exiting due to GUEST_MISSING_CONNTRACK: Sorry, Kubernetes 1.21.2 requires conntrack to be installed in root's path
sudo apt-get install -y conntrack

# 설치 상태 확인
minikube status

# 권한 설정 
sudo usermod -aG docker $USER && newgrp docker

# minikube 실행 
# 실패 ? sudo minikube start --vm-driver=docker
minikube start --driver=docker

```

- 수행 시 아래와 같은 오류 발생  
Suggestion: Check output of 'journalctl -xeu kubelet', try passing --extra-config=kubelet.cgroup-driver=systemd to minikube start

```
minikube start --driver=docker --extra-config=kubelet.cgroup-driver=systemd
```




