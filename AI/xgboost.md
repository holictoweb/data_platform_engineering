# ref
- 공식문서
  - https://xgboost.readthedocs.io/en/stable/prediction.html



- bayesian optimization
  - https://github.com/fmfn/BayesianOptimization
  - pip install bayesian-optimization



# 파라미터 
1. General parameters 
    - booster : 어떤 부스터 구조를 쓸지 결정 . gbtree, gblinear, dart
    - nthread : 몇 개의 쓰레드를 동시에 처리 하도록 할지 결정. default '가능한 많이'
    - num_feature : feature  차원의 숫자를 정해야 하는 경우 옵션을 셋팅. default '가능한 많이'
2. booster paramters
    - eta 
    - gamma : 디폴트 0 작을 수록 보수적 모델
    - max_depth : 숫자가 커질 수록 모델의 복잡도가 높아지고 과적하기 쉽다.  디폴트 6 이대 리프 노드의 개수는 최대 2^6 = 64개 이다. 
    - lambda (L2 reg-form) : tntwkrk zmftnfhr 
    - alpha (L1 reg-form) : 숫자가 클수록 보수적인 모델이 된다. 

    - gamma : 분할 후 손실에서 예상 감소에 기초하여 주어진 노드를 분할할지 여부를 제어한다. 높은 값은 더 적은 분할로 이어진다. 오직 트리기반 학습기만 지원된다.
    - alpha : 리프(leaf) 가중치에 L1 정규화. 큰 값은 더 많은 정규화로 이어진다.
    - lambda : 리프 가중치에 L2 정규화를 하고 L1 정규화보다 더 부드럽다.(smooth)


    출처: https://a292run.tistory.com/entry/Using-XGBoost-in-Python-1 [Dead & Street]
3. Learning Task Parameteres
    - objective : 목적함수 reg:linear(linear-regression), binary:logistic(binary-logistic classification), count:poisson(count data poison regression) 
    - eval_metric : 모델의 평가 함수를 조정하는 함수. rmse (root mean square error), logloss(log-likelihood), map(mean average precision) 등 해당 데이터 특성에 맞게 평가 함수를 조정한다.

4. command line paramters
    - num_rounds : 부스팅 라운드를 결정. 랜덤하게 생성되는 모델이니만큼 이 수가 적당히 큰게 좋다. epoch 옵션과 동일하다. 

# 파라미터 우선 순위
1. booster ( 부스터 모양 )
2. eval_metric(평가함수) / objective(목적함수)
3. eta ( 러닝 레이트)
4. L1 form ( L1 레귤러라이제이션 폼이 Lg2 보다 아웃라이어에 민감하다 )
5. L2 form


#### 참고 https://brunch.co.kr/@snobberys/137
### 공식 xgboost https://xgboost.readthedocs.io/en/latest/parameter.html




# python wrapper
```py
import xgboost as xgb ## XGBoost 불러오기
from xgboost import plot_importance ## Feature Importance를 불러오기 위함
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score
import warnings


features, label = df_train.iloc[:,:-1], df_train.iloc[:,-1]

x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=156)

# DMatrix는 넘파이 입력 파라미터를 받아서 만들어지는 XGBoost의 전용 데이터 세트입니다. 주요 입력 파라미터는 data와 label입니다. 
# 여기서 data는 피처 데이터 세트, label은 분류의 경우 레이블 데이터, 회귀의 경우 종속값 데이터입니다.
dtrain = xgb.DMatrix(data=x_train, label=y_train, enable_categorical=True)
dtest = xgb.DMatrix(data=x_test, label=y_test, enable_categorical=True)


# https://hwi-doc.tistory.com/entry/%EC%9D%B4%ED%95%B4%ED%95%98%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EC%9E%90-XGBoost

# XGBoost를 사용하기 위해서는 DMatrix 형태로 변환해 주어야 합니다
dtrain = xgb.DMatrix(x_train, y_train)
dval = xgb.DMatrix(x_val, y_val)
dtest = xgb.DMatrix(x_test)

# 모델 생성
# num_boost_round 만큼 반복하는데 early_stopping_rounds 만큼 성능 향상이 없으면 중단
# early_stopping_rounds를 사용하려면 eval 데이터 셋을 명기해야함
param = {파라미터 설정}
xgb_model = xgb.train(params = params, dtrain = dtrain, num_boost_round = 400, 
                        early_stopping_rounds = 100, evals=[(dtrain,'train'),(dval,'eval')])

# 예측하기, 확률값으로 반환됨
y_pre_probs = xgb_model.predict(dtest)

# 0또는 1로 변경
y_preds = [1 if x>0.5 else 0 for x in y_pre_probs]

# 특성 중요도 시각화
fig, ax = plt.subplots(figsize=(10,12))
plot_importance(xgb_model, ax=ax)

```



# scikit learn wrapper
```py
# 후보 파라미터 선정
params = {
    'n_estimators':[60,70,100],
    'max_depth':[15,16], 
    'min_child_weight':[0.8,0.9,1], 
    'colsample_bytree':[0.5,0.75],
    'learning_rate':[0.3,0.35,0.4],
    'objective':['binary:logistic','binary:logitraw','binary:hinge']
}

# gridsearchcv 객체 정보 입력(어떤 모델, 파라미터 후보, 교차검증 몇 번)
holic_gridcv = GridSearchCV(holic_model, 
    param_grid=params, 
    cv= KFold(3) ,
    n_jobs= -1,     # 병렬 처리갯수 -1은 전부
    scoring='f1_weighted'
)


holic_gridcv.fit(x_train, y_train, 
    early_stopping_rounds=100, 
    #objective='binary:logistic', # default = reg:linear multi:softmax : softmax를 사용한 다중 클래스 분류, 확률이 아닌 예측된 클래스 반환 
    eval_metric='auc', # aucpr
    eval_set=[(x_test, y_test)]
)
```

# gridsearchCV

```py


```

# pipeline
```py
# pipeline 구성

```

# k-fold

- k-fold Cross Validation using XGBoost
좀더 가력한 모델을 구축하기 위해서는 보통 원본 훈련 데이터셋의 모든 항목이 훈련과 검즘 모두에 사용되는 k-fold 교차 검증을 수행한다. 또한 각 항목(entry)은 단 한번만 검증에 사용된다. XGBoost는 cv() 메서드를 통해 k-fold 교차검증을 지원한다. 단지 만들고자하는 교차 검증 묶음의 수인 nfolds 파라미터를 지정하는 것으로 이를 수행 할 수 있다. 전체 파라미터는 여기를 보자.

- num_boost_round : 구축한 트리의 수를 나타낸다.(n_estimators와 유사)
- metrics : 교차검증동안 관찰할 평가 지표
- as_pandas : 판다스 데이터프레임으로 결과 반환
- early_stopping_rounds : 만약 주어진 횟수 동안 정해진 지표가 개선되지 않으면, 일찍 모델의 훈련을 종료한다.
- seed : 결과의 재현성을 위함   

이제 모든 하이퍼파라미터와 그 값을 키-값 쌍으로 갖는 params 딕셔너리를 만든다. 하지만, num_boost_rounds를 사용하기 때문에 params 딕셔너리에서 n_estimators는 제외한다.




# visualization
```bash
# 기본적인 plot_
sudo apt-get install graphviz

pip install graphviz
pip install 
```



# load and predict
```py

```




- - - 

# GPU 사용
- nvidia xgboost 설치 
```bash
conda remove xgboost
conda install -c nvidia -c rapidsai py-xgboost
```





