
# leaf-wise tree 주요 파라미터 
1. num_leaves

이것은 트리모델의 복밥성을 컨트롤하는 주요 파라미터이다.
보통 num_leaves = 2^(max_depth)는 depth-wise tree와 같은 수의 leaves를 가지게 하여, 이보다 작게 설정해야 오버피팅을 줄일 수 있다.
예를 들어, max_depth가 7일 경우 좋은 성능을 보였다면, num_leaves는 127보다 적은 70~80사이에서 더 좋은 성능을 얻을 수 있다.
default = 31

2. min_data_in_leaf

오버피팅을 예방하는 데 중요한 파라미터이다.
값을 크게 하면 너무 깊은 tree를 피할 수 있지만, 언더피팅이 생길 수 도 있다.
아주 큰 데이터 셋(최소 10000건 이상)에서는 100~1000의 값이면 충분하다.
default = 20

3. max_depth

tree의 depth 한계를 지정하는 것
default = -1 (가능한 최대, -1일 때 학습하는 모델의 max_depth을 알아내는 것을 찾아볼 것


- - - 
- 실제 적용 방식

1. 적절한 max_depth 값을 찾아낼 것

max_depth를 찾을 때, 우선 큰 값으로 학습하면 default일 때와 metric이 같은 경우가 있습니다. 그 값을 찾은 이후에 gridsearch 함수나 수동으로... 찾아서 적절한 max_depth를 찾으면 될 것 같습니다.
feature 약 280개, 데이터 약 10000건인 경우에 max_depth는 약 20~30 사이인 것 같습니다. 그 수치보다 작게 설정한 후 적절한 num_leaves를 튜닝하면 될 것 같습니다.
2. max_depth 값에 알맞게 num_leaves를 튜닝할 것

3. min_data_in_leaf를 튜닝할 것