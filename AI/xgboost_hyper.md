

# F1 score 



## xgboost prarmeter 
- learnning rate
  - 높을수록 과적합 하기 쉬움
- subsample ( 0.5 ~ 1)
   - weak learniner가 학습에 사용하는 샘플링 비율
  - 값이 낮을 수록 과적합 방지 

- n-estimator ( default=100 )
  - 생성할 weak leaner 숫자
  - learning rate가 낮을때, n-estimatore가 높아야 과적합 방지   
- max_depth ( default=7 )
  - 클 수록 모델 복잡도가 높아지고 과적합 하는 경향 

- gamma ( default = 0 )
  - leaf node 의 추가 분할을 결정할 최소 손실 감소값
  - 해당값 보다 손실값이 크게 감소 할때 분리
  - 값이 높을 수록 과적합








# 파라미터 확인
https://injo.tistory.com/44






- - -

# history

```py
holic_model = xgb.XGBClassifier(
    tree_method="hist", booster='gbtree', use_label_encoder=False, objective='binary:logistic', 

    
    

    colsample_bylevel=0.84109,
    colsample_bytree=0.8502, 
    gamma=0.76004, 
    learning_rate=0.3972,
    max_delta_step=0.94751,
    max_depth=7,
    min_child_weight=0.99936, 
    n_estimators=700,
    reg_lambda=1.00208,
    reg_alpha=0,
    scale_pos_weight=0.9774, # 음성 데이터 수/ 양성 데이터 수 값
    num_parallel_tree=1,
)
'''
'colsample_bylevel': 0.8410922557785607,
  'colsample_bytree': 0.8502017422414512,
  'gamma': 0.7600464624092124,
  'learning_rate': 0.39720456126623527,
  'max_delta_step': 0.9475119514527265,
  'max_depth': 6.204319788151851,
  'min_child_weight': 0.999361237466811,
  'n_estimators': 525.7258113847278,
  'reg_lambda': 1.0020829366882584,
  'scale_pos_weight': 0.9774478735663362
'''

```