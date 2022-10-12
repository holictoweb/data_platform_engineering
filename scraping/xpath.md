

- 
-  XPath는 "//"를 이용하여 노드 패스를 생략할 수 있다. "//"는 descendant-or-self의 생략형이다.




### remove node
```py
doc.removeChild(node);
```


    표현식설명

nodename	nodename을 name으로 갖는 모든 요소 선택
/	root 요소에서 선택
//	현재 요소의 자손 요소를 선택
.	현재 요소를 선택
..	현재 요소의 부모 요소를 선택
@	속성(attibutes)를 선택
*	모든 요소에 매치됨
@*	모든 속성 요소에 매치됨
node()	모든 종류의 모든 요소에 매치됨
|	OR 조건의 기능
예시는 다음과 같다.

표현식설명

/div	root 요소의 div 요소
./div	현재 요소의 자식 요소 중 div 요소
/*	name에 상관없이 root 요소를 선택
./* 또는 *	context 요소의 모든 자식 요소를 선택
//div	현재 웹페이지에서 모든 div 요소를 선택
.//div	현재 요소의 모든 자손 div 요소를 선택
//*	현재 웹페이지의 모든 요소를 선택
.//*	현재 요소의 모든 자손 요소를 선택
/div/p[0]	root > div > p 요소 중 첫 번째 p 요소를 선택
/div/p[position()<3]	root > div > p 요소 중 첫 두 p 요소를 선택
/div/p[last()]	root > div > p 요소 중 마지막 p 요소를 선택
/bookstore/book[price>35.00]	root > bookstore > book 요소 중 price 속성이 35.00 초과인 요소들을 선택
//*[@id="tsf"]/div[2]/	id가 tsf인 모든 요소의 자식 div 요소 중 3번째 요소를 선택
//title | //price	title 또는 price 요소를 선택