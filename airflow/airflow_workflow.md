# airflow workflow 생성 가이드



# 1. trigger rule
``` python
ALL_SUCCESS = 'all_success' #default
ALL_FAILED = 'all_failed'
ALL_DONE = 'all_done' # 작업 성공 여부에 관계없이 모두 작동한 경우
ONE_SUCCESS = 'one_success'
ONE_FAILED = 'one_failed'
DUMMY = 'dummy'
NONE_FAILED = 'none_failed'

```

