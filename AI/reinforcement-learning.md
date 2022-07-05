

# DQN 기본 수식

- State = 현재 상태
- Action = 특정 상태에서 수행가능한 행동들
- 보상함수(reword) = State(S)에서 Action(a) 을 실행 했을때의 보상 
- 학습률(learning rate) α = 0~1 사이의 실수. 학습의 결과로 부터 얻어지는 강화 값의 갱신율을 조절하는 역활을 한다. 
- 감쇄율(discount rate) λ= 0~1 사이의 실수. 가치 함수를 수렴하도록 만드는 역활을 한다. 
- 


- 신경망 (torch.nn)
- 최적화 (torch.optim)
- 자동 미분 (torch.autograd)
- 시각 태스크를 위한 유틸리티들 (torchvision - a separate package).




# DDPG (Deep Deterministic Policy Gradient)
- 딥마인드 논문 확인 필요 
- DDPG는 구글 딥마인드에서 만든 모델로 DQN을 개선한 Model-Free Reinforce Learning 중 하나의 학습 방법으로 replay buffer를 추가한 off-policy algorithm 입니다. 
- DDPG는 오로지 COntinous Action Sapce에서만 활용이 가능하며 DQN 방식을 continuous action space 에 적용한 학습 방법으로 볼 수 있습니다. 
- DDPG 관련하여 확인 ( https://velog.io/@uonmf97/HUFS-RL-%EA%B0%95%ED%99%94%ED%95%99%EC%8A%B5-Reinforcement-Learning-DDPG-Deep-Deterministic-Policy-Gradient )
![](https://velog.velcdn.com/images%2Fuonmf97%2Fpost%2F763ddcba-87fc-4810-bef4-ac6cb4bf483c%2FScreen%20Shot%202022-03-16%20at%208.13.00%20PM.png)

## DDPG 금융 관련 논문 번역 
### DDPG
- https://koreapy.tistory.com/519
- DDPG와 관련된 좋은 





