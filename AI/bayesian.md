

# bayesian optimazation

- ref
- http://restanalytics.com/2021-08-12-BayesianOptimizationOptimization/


```py
from bayes_opt import BayesianOptimization

features, label = df_test.iloc[:,:-1], df_test.iloc[:,-1]
x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=156)


def XGB_cv(max_depth,learning_rate, n_estimators, gamma
           ,min_child_weight, max_delta_step, subsample
           ,colsample_bytree, colsample_bylevel, scale_pos_weight, nthread=-1):
    model = xgb.XGBClassifier(max_depth=int(max_depth),
                              learning_rate=learning_rate,
                              n_estimators=int(n_estimators),
                              nthread=nthread,
                              gamma=gamma,
                              min_child_weight=min_child_weight,
                              max_delta_step=max_delta_step,
                              subsample=subsample,
                              colsample_bytree=colsample_bytree,
                              colsample_bylevel=colsample_bylevel,
                              scale_pos_weight=scale_pos_weight,
                              objective='binary:logistic',
                              eval_metric='logloss',
                              use_label_encoder=False )
    RMSE = cross_val_score(model, x_train, y_train, scoring='f1', cv=5).mean()
    
    #모델 검증 
    # scores = cross_val_score(model, x_train, y_train, scoring='recall')
    #scores = cross_val_score(model, x_train, y_train, scoring=make_scorer(recall_score))
    # scores = cross_val_score(model, x_train, y_train, scoring='precision')
    precision = cross_val_score(model, x_train, y_train, scoring=make_scorer(precision_score))
    #scores = cross_val_score(model, x_train, y_train, scoring='f1')
    #scores = cross_val_score(model, x_train, y_train, scoring=make_scorer(f1_score))

    return -RMSE

# 주어진 범위 사이에서 적절한 값을 찾는다.
pbounds = {'max_depth': (6,9),
          'learning_rate': (0.1, 0.4),
          'n_estimators': (500, 700),
          'gamma': (0.001, 1.0),
          'min_child_weight': (0.5, 1),
          'max_delta_step': (0, 0.9),
          'subsample': (0.7, 0.9),
          'colsample_bytree': (0.7, 0.99),
          'colsample_bylevel': (0.7, 0.99),
          'scale_pos_weight': (0.5, 0.8)
          }

xgboostBO = BayesianOptimization(f = XGB_cv,pbounds = pbounds, verbose = 2, random_state = 1 )

# 메소드를 이용해 최대화!
xgboostBO.maximize(init_points=2, n_iter = 5)

xgboostBO.max # 찾은 파라미터 값 확인

'''
{'target': -0.5967965367965367,
 'params': {'colsample_bytree': 0.7043407823042612,
  'gamma': 0.7206041689487159,
  'learning_rate': 0.200022874963469,
  'max_delta_step': 0.030233257263183978,
  'max_depth': 6.293511781634226,
  'min_child_weight': 0.8231850816907923,
  'n_estimators': 374.50408455106833,
  'subsample': 0.7691121454086095}}
  '''
```



