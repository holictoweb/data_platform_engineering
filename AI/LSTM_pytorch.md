# pytorch 설치 



- https://pytorch.org/get-started/locally/
``` bash
# linux, cpu
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```


# 기본문서 
https://diane-space.tistory.com/331


# basic

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

#
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# GPU setting
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#print(torch.cuda.get_device_name(0)) #Google colab = TESLA T4


# 1. torch variable 생성
train_x_tensor = Variable(torch.Tensor(train_x))
train_y_tensor = Variable(torch.Tensor(train_y))


```




# RNN

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=http%3A%2F%2Fcfile3.uf.tistory.com%2Fimage%2F9901A1415ACB86A0211095)


