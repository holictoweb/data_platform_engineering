# EBS 용량 수정



- 30G -> 80G 
```bash
(base) ubuntu@ip-10-0-2-115:~/upload_plugin$ lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0         7:0    0 25.1M  1 loop /snap/amazon-ssm-agent/5656
loop1         7:1    0 24.4M  1 loop /snap/amazon-ssm-agent/6312
loop2         7:2    0 63.2M  1 loop /snap/core20/1695
loop3         7:3    0 55.6M  1 loop /snap/core18/2566
loop4         7:4    0 63.2M  1 loop 
loop5         7:5    0 55.6M  1 loop /snap/core18/2620
loop6         7:6    0 67.8M  1 loop /snap/lxd/22753
loop7         7:7    0   48M  1 loop /snap/snapd/17029
loop8         7:8    0 63.2M  1 loop /snap/core20/1634
loop9         7:9    0   48M  1 loop /snap/snapd/17336
nvme0n1     259:0    0   80G  0 disk 
└─nvme0n1p1 259:1    0   30G  0 part /
```

1. 디바이스 파티션에 할당
- https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html
```bash
# 첫번째 파티션 nvme0n1p1 을 확장  - 디바이스 이름(nvme0n1)과 파티션 번호(1) 사이의 공백에 유의하세요.
sudo growpart /dev/nvme0n1 1
```

2. 파일시스템 확장

```bash
# For ext4 filesystem
sudo resize2fs /dev/root

Filesystem     Type      Size  Used Avail Use% Mounted on
/dev/root      ext4       78G   26G   52G  34% /
devtmpfs       devtmpfs  7.8G     0  7.8G   0% /dev


# For xfs filesystem
sudo xfs_growfs /
```
