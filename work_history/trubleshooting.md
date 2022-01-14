


 # xml 파싱 시 이슈 
 ```
  File "src/lxml/etree.pyx", line 3252, in lxml.etree.fromstring
  File "src/lxml/parser.pxi", line 1912, in lxml.etree._parseMemoryDocument
  File "src/lxml/parser.pxi", line 1800, in lxml.etree._parseDoc
  File "src/lxml/parser.pxi", line 1141, in lxml.etree._BaseParser._parseDoc
  File "src/lxml/parser.pxi", line 615, in lxml.etree._ParserContext._handleParseResultDoc
  File "src/lxml/parser.pxi", line 725, in lxml.etree._handleParseResult
  File "src/lxml/parser.pxi", line 654, in lxml.etree._raiseParseError
  File "<string>", line 1
lxml.etree.XMLSyntaxError: Start tag expected, '<' not found, line 1, column 1


데이터가 없었음....

 ```