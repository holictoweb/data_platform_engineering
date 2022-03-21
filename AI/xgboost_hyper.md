

![링크](https://miro.medium.com/max/1400/1*87eR1mcwoosszpb_m1K1wg.png)



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


- 불균형 데이터 처리 
How to Configure XGBoost for Imbalanced Classification


- - -

# parameter tunning

- learning rate 
```py
부스팅 각 이터레이션 마다 곱해지는 가중치(loss function의 step size)로 모형 성능과 학습시간에 영향을 준다.

보통 작을수록 모형 성능 향상에 도움이 되지만 학습 시간은 길어지는 trade-off가 있다.

하이퍼파라미터 튜닝시에는 0.1~0.3 정도의 값을 사용하고, 최종 모형 학습시에는 0.05이하의 값을 사용하는 것이 좋다.  

learning rate를 옵티마이저에 넣어서 튜닝할 필요는 없다. 주어진 컴퓨팅 환경을 고려하여 적당한 값을 정한 후 그 값에서 다른 파라미터들을 튜닝하는 것이 좋다. 옵티마이저에 learning rate를 포함시켜서 0.0202048 같은 값에 오버피팅 시키는 것은 불필요한 시도이다.

단, learning rate를 크게 잡았을때 모형 적합이 잘 되지 않는다면, 이 값을 기준으로 튜닝한 다른 하이퍼파라미터의 조합이 learning rate를 낮추었을때는 최적 조합이 아니게 될 가능성이 높다. 경험상 하이퍼파라미터 튜닝시에도 learning rate를 너무 큰 값으로는 설정하지 않는 것이 좋다.  


```


- maxi