

- pre-trained 
  - https://fasttext.cc/docs/en/crawl-vectors.html

  

### install fasttext

```bash
$ git clone https://github.com/facebookresearch/fastText.git
$ cd fastText
$ sudo pip install .
$ # or :
$ sudo python setup.py install
```



### download pre-trained model

```python
import fasttext.util
fasttext.util.download_model('ko', if_exists='ignore')  
ft = fasttext.load_model('cc.en.300.bin')
```

### text file

```
wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ko.300.vec.gz
```



### 유사 단어 검출 

```python
from fasttext

# 차원 확인 ( default 300 )
ft.get_dimension()

# 차원 변경
fasttext.util.reduce_model(ft, 100)

# 단어 차원 확인 
ft.get_word_vector('hello').shape


# 변경된 차원 저장
ft.save_model('cc.en.100.bin')

# 유사단어 검색 
ft.get_nearest_neighbors('우주항공', k=30)
```





