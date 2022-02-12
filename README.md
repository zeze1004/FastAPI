# FastAPI 실습 저장소입니다.
</br>

## 제제의 트러블 슛 정리❤️‍🔥



PR 오류 이슈 발생 → resolving

`gitpython`에서 `Repo` 모듈에서 인코딩 에러 이슈

```
Encoding problemACKNOWLEDGED
File "/Users/mac/project/...", line 92, in pull_request
    repo = g.get_repo({repo name})
...

UnicodeEncodeError: 'latin-1' codec can't encode character '
```

### 에러 수정을 위한 노력🥲

파이썬3은 디폴트가 utf-8로 인코딩하는거라는데 왜 그러는거야 정말... 

- Repo 인코딩하기… → 실패

```
# decode도 하면 해결 된다는 블로그글도 있길래 따라해봄
create_branch(repo.encode('utf-8').decode('iso-8859-1'))
pull(repo.encode('utf-8'))

>>
AttributeError: 'Repo' object has no attribute 'encode'
```

### `gitpython` 인코딩 부분 코드


#### `compat.py`
```
defenc = sys.getfilesystemencoding().     # -> 요걸 써볼까

def safe_encode(s: Optional[AnyStr]) -> Optional[bytes]:
    """Safely encodes a binary string to unicode"""
    if isinstance(s, str):
        return s.encode(defenc)
    elif isinstance(s, bytes):
        return s
    elif s is None:
        return None
    else:
        raise TypeError('Expected bytes or text, but got %r' % (s,))
```
- gitpython에서 나타나는 인코딩 에러랑 다름

    -  인코딩이 제대로 안 된 상태에서 http단에서 문제가 생긴건가 @_@


</br>

### `requests` 오픈소스 


#### `client.py`
```
   def putheader(self, header, *values):
        """Send a request header line to the server.

        For example: h.putheader('Accept', 'text/html')
        """
        if self.__state != _CS_REQ_STARTED:
            raise CannotSendHeader()

        if hasattr(header, 'encode'):
            header = header.encode('ascii')

        if not _is_legal_header_name(header):
            raise ValueError('Invalid header name %r' % (header,))

        values = list(values)
        for i, one_value in enumerate(values):
            if hasattr(one_value, 'encode'):
                values[i] = one_value.encode('latin-1')     ### 에러 발생 구문
            elif isinstance(one_value, int):
                values[i] = str(one_value).encode('ascii')

            if _is_illegal_header_value(values[i]):
                raise ValueError('Invalid header value %r' % (values[i],))

        value = b'\r\n\t'.join(values)
        header = header + b': ' + value
        self._output(header)
```

### `requests` 인코딩 오류 체크법

```
a = "\u13E0\u19E0\u1320"
a.encode('latin-1')  # Throws UnicodeEncodeError, proves that this can't be expressed in ISO-8859-1.
a.encode('utf-8')  # Totally fine.
r = requests.post('http://httpbin.org/post',
                   data=a)  # Using unicode string, throws UnicodeEncodeError blaming Latin1.
r = requests.post('http://httpbin.org/post', data=a.encode('utf-8'))  # Works fine.
```
- `a.encode('latin-1')` 부터 에러…오열

    - 인코딩 에러가 아닌가???

</br>

### 에러 나는 구문 인코딩 했을 시
```
repo = g.get_repo({repo name}.encode('latin1')) 

>> AssertionError: b'{path}'
```
- {repo name}은 문제 없었음

### 그럼 디코딩을 해보자 ㅎㅎㅎ
```
repo = g.get_repo('b' + {repo name}).decode("utf-8", "replace")
```
- 될리가 없지…

</br>

## 로컬 터미널 문제인걸로 방향이 잡힘 → 슬랙에 질문하길 정말 잘했다~! 제제야

```
❯ file git_api.py
git_api.py: Python script text executable, ASCII text
```
- **ASCII** 가 아니라 **UTF-8**로 설정 되어야 함!!!!!
