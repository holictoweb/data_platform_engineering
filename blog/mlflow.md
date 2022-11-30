Background 

에이셀의 ml/data workflow는 기본적으로 AWS cloud 상에 container 기반으로 수행이 됩니다. 대용량 대이터 처리가 기본적으로 필요 하여 ECS(AWS Elastic Container Service)를 사용하며 머신러닝 수행은 sagemaker에서 제공하는 container 기반의 잡을 사용하며 추론을 위한 서비스도 container 기반의 inference endpoint를 사용합니다. 
기본적으로 개발 초기 단계 부터 container 기반으로 프로세스들이 개발이 되어 workflow의 단계들이 일부 합쳐져 있는 문제는 있었지만 각각의 container 수행들이 queue 형태의 table로 연결 되어 수행 시점에 대한 dependency는 없는 상황이었습니다. CI/CD에 대한 부분은 github actions를 통해 소스 코드 배포와 동시에 container registry 에 컨테이너화 하여 등록 하고 수행 시 변경 된 image를 기반으로 container를 생성하게 됩니다. 

하지만 큐 형태의 테이블을 사용하여 pipeline을 구성 한다는것은 다양하고 복잡한 파이프라인의 구성이 어려우며 파이프라인들이 늘어 나게 됬을때 파이프라인들에 대한 관리/모니터링을 위한 구성과 tool의 적용이 필요하였습니다. 

이미 많은 종류의 ETL 혹은 orchestration 툴들이 나와 있으며 용도에 따라 선택지가 다양합니다. 대표적인 서비스들에 대해 간단히 확인해 보면,

1. kubeflow  
   argo 기반의 kubernetes + ML 형태의 서비스입니다.  ML workflow에 적합한 구성으로 jupyter notebook을 통한 workflow 관리가 가능하며 다양한 머신러닝과 관련된 operator ( MXNet operator, PyTorch operator, XGBoost operator 등 ) 와 prometheus를 통한 로깅 및 모니터링 기능도 함께 제공하고 있습니다. AWS 에서도 eks ( elastic kubernetes Serivce )상에 kubeflow가 정식 배포 되었습니다. 

Kubeflow v1.4.1을 지원하는 AWS에서의 Kubeflow 배포 정식 출시 - 2022-05-16
https://aws.amazon.com/ko/about-aws/whats-new/2022/05/aws-distribution-kubeflow-supporting-kubeflow-v1-4-1-generally-available/

2. apache airflow  
    airbnb 에서 만든 task workflow management tool 입니다. python 코드 기반으로 파이프라인을 구성하며 다양한 executor를 통해 standalone 으로 구성하거나 kubernetes 상에 pod 형태로 클러스터 구성도 가능한 툴입니다. ML에 특화되거나 ETL에 특화되지 않고 python으로 연결 가능한 모든 서비스에 대한 orchestration이 가능한 툴입니다. 

3. dagster  
   Data Driven application을 python code 기반으로 쉽게 개발 및 배포 할 수 있도록 만든다는 모토를 가진 툴입니다. data 를 기반으로 하며 streaming 처리나 모니터링이 가능하며 airflow2.0에 추가된 TaskFlow api와 유사한 개발 형태를 가지고 있습니다. 스트리밍 처리나 입력 데이터를 임의로 넣어서 결과를 받을 수 있는 등 data 처리에 강점을 보이고 있는 서비스 입니다. 

그외에도 public cloud 별로 특화된 ETL management tool ( AWS step function, AZURE data factory), MLOps 관리 서비스 ( AWS Sagemaker, AZURE Machine Learning ) 등도 존재합니다.

저희는 일단 AWS를 사용하고 있으며 ML 이나 DATA 특정 영역이 아닌 전체 workflow를 관리 하면서 aws resource에 대한 모니터링이나 ec2 중지/삭제와 같은 task들도 통합해서 관리할 서비스가 필요 하여 airflow를 선택 하였으며 머신러닝과 관련된 부분은 sagemaker의 기능을 활용 하며 pipeline 구성은 역시 airflow에서 관리 하는 것으로 진행하는 것으로 정했습니다. 