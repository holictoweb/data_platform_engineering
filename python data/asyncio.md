
# python 표준 라이브러리 asyncio 
- https://docs.python.org/ko/3/library/asyncio-task.html#coroutines


- jupyter 에서는 기본적으로 event loop가 이미 돌고 있기 때문에 실행 시 대상 함수를 await 시켜 주기만 하면 실행 됨. 
- 

## - awaitable object
- 코루틴 ( 코루틴 함수/ 코루틴 객체-반환객체 ) 태스크 퓨처

### 1. coroutine 

### 2. task
- coroutine을 동시에 예약 하는데 사용 
### 3. future
- 콜백 기반 코드를 async/await와 함께 사용하려면 asyncio의 Future 객체가 필요합니다.

https://kukuta.tistory.com/345

# event loop
```py
loop = asyncio.get_event_loop() # 이벤트 루프를 가져옴
loop.run_until_complete( say('hello wordl', 1) ) # 코루틴의 객체를 가져 와서 loop에 등록 후 coroutine이 종료 되면 해당 loop를 종료
loop.close()

```

- 멀티태스크
```py
import asyncio
async def say(what, delay):
    await asyncio.sleep(delay)
    print(what)

loop = asyncio.get_event_loop()
task1 = loop.create_task(say('first hello', 2))
task2 = loop.create_task(say('seccond hello', 1))

loop.run_until_complete(task1)
loop.run_until_complete(task2)

loop.close()
```


# 소켓 통신
- 스트리미 통신 - TCP
- 소켓 이벤트 통신 - TCP, UDP


# 기본 용어
- async def 를 사용하여 구현된 함수를 코루틴( corutines ) 이라고 부른다. ( 코루틴 = 비동기 함수 )
```py
# 간단한 함수 생성 
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')
    
asyncio.run(main()) # ipython 에서는 사용 불가 
await main() # ipython 에서 실행 시
```




# async 를 통한 페이지 수집 비동기 처리 
- 실제 크롤링 시점에 proxy 서비스까지 사용할 시 io 대기 시간이 길어 지는 현상 발생 해당 현상 개선에 비동기 처리 적용 필요
```py
import time
import requests
import asyncio                       # asyncio 모듈 임포트

async def download_page(url) :       # async def로 함수 정의
    ​​​​loop = asyncio.get_event_loop()  # 이벤트 루프 객체 얻기
    ​​​​req = await loop.run_in_executor(None, requests.get, url) # 동기함수를 비동기로 호출
    ​​​​
    ​​​​html = req.text
    ​​​​print("complete download:", url, ", size of page(", len(html),")")
​​​​
async def main() :
    ​​​​await asyncio.gather(
    ​​​​​​​​download_page("https://www.python.org/"),
    ​​​​​​​​download_page("https://www.python.org/"),
    ​​​​​​​​download_page("https://www.python.org/"),
    ​​​​​​​​download_page("https://www.python.org/"),
    ​​​​​​​​download_page("https://www.python.org/")
    ​​​​)    

    print(f"stated at {time.strftime('%X')}")
    start_time = time.time()
    asyncio.run(main())
    finish_time = time.time()
    print(f"finish at {time.strftime('%X')}, total:{finish_time-start_time} sec(s)")
출처: https://kukuta.tistory.com/345 [HardCore in Programming:티스토리]
```



# async 를 통한 비동기 수집 (2)
```py
import asyncio
import requests

@asyncio.coroutine
def main():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.google.co.uk')
    response1 = await future1
    response2 = await future2
    print(response1.text)
    print(response2.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```