

# 4. FastAPI 기반 기본 API 서버 구성
``` Bash
# 1단계: 가상환경 생성 및 활성화
python -m venv venv

# (Mac 사용자용 활성화)
source venv/bin/activate

# 2단계: 필수 라이브러리 및 테스팅 툴 설치
pip install fastapi uvicorn "uvicorn[standard]"
pip install pytest pytest-asyncio

# 3단계: 테스트 실행
pytest
```
### FastAPI 
- Python으로 만드는 고성능 웹 API 프레임워크  
    - 타입 힌트 기반으로 자동으로 유효성 검증
    - Swagger UI 자동 생성
    - 비동기 지원
- uvicorn : FastAPI를 실행시켜주는 서버
- 서버 실행 명령어 : `uvicorn main:app --reload`
    - `--reload`: 코드 수정 시 서버가 자동으로 재시작(개발 중 사용)
    - 운영 환경에서는 서비스 중단 위험으로 사용 비추천

### 라우팅
- 어떤 URL로 들어오는 요청을 어떤 함수가 처리할지 연결해주는 것
    - `GET /users/123` 요청 -> `get_user(user_id=123)` 함수 실행
- `uvicorn 01_router:app --reload`

#### 쿼리 파라미터 (query parameter)
- URL 끝에 물음표(?)를 붙이고 키=값 형태로 추가 옵션을 주는 방식
- 주로 데이터의 검색, 필터링, 페이지 나누기(페이징)에 사용
- `GET /users?skip=1&limit=2`
``` python
@app.get("/users/filtered")
def get_filtered_users(skip: int = 0, limit: int = 2):
    return users_database[skip : skip + limit]
```

#### 경로 파라미터 (path parameter)
``` python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users_database:
        if user["id"] == user_id:
            return user
```
- `/users/abc` : 422 에러

### POST 라우팅 (데이터 받기)
- Pydantic : 데이터 클래스에 자동 검사 기능과 자동 타입 변환 기능을 붙이고 싶을 때
- BaseModel : Pydantic을 사용하기 위한 기초 설계도
``` python
class UserCreateRequest(BaseModel):
    id: int
    name: str

@app.post("/create_users")
def create_user(request: UserCreateRequest):
    ...
```

### HTTPException으로 에러 처리
- 데이터가 없거나, 권한이 없는 상황 등에서 HTTP 상태코드와 함께 의미 있는 에러 메시지를 반환하는 방법
``` python
from fastapi import FastAPI, HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users_database:
        if user["id"] == user_id:
            return user
            
    raise HTTPException(
        status_code=404, 
        detail=f"유저 {user_id}를 찾을 수 없습니다"
    )
```

### async def — 비동기 엔드포인트
- FastAPI는 `def`와 `async def` 둘 다 지원
    - `def`: 일반 함수, 일반적인 DB 쿼리나 requests 같은 동기 라이브러리를 쓸 때
    - `async def` : 비동기 함수, await를 지원하는 비동기 라이브러리나 API 호출 시 사용
        - await는 async def 함수 안에서만 사용 가능
        - 일반 def 안에서 await를 쓰면 SyntaxError

### APIRouter로 코드 구조화
- 엔드포인트가 많아지면 main.py 하나에 모두 담기 어려움
- APIRouter를 쓰면 기능별로 파일을 나눠서 관리
    - /users 관련 엔드포인트들은 routers/user.py에 작성
    - /chat 관련 엔드포인트들은 routers/chat.py에 작성
- prefix : 라우터 내 모든 경로 앞에 자동으로 prefix가 붙음
    - prefix="/users"
- tags : Swagger UI에서 같은 태그끼리 묶여서 표시
    - tags=["users"]
- [실습] 01_prac.py : 세션 API 만들기

### Swagger UI
- FastAPI가 자동으로 만들어주는 API 문서 + 브라우저 테스트 도구
- 브라우저에서 직접 API를 호출 가능
- `http://127.0.0.1:8000/docs`
- 명세 -> 구현 -> 검증 흐름
    1. 명세 정의 : 어떤 API가 필요한지 먼저 정의
    2. 구현 : FastAPI 코드로 작성
    3. 검증 : swagger UI에서 직접 호출해서 확인

``` python
app = FastAPI()
# FastAPI 웹 애플리케이션 인스턴스
router = APIRouter(prefix="/reviews", tags=["reviews"])
# 엔드포인트를 묶어둘 라우터를 만드는 줄
# 라우터에 등록되는 모든 경로에는 앞에 "/reviews"가 앞에 붙음
...
app.include_router(router)
# router에 등록된 모든 엔드포인트를 app의 라우팅 테이블에 병합
```
- 엔드포인트를 app에 직접 등록하면 `app.include_router(router)`가 필요없음
    - app가 직접 등록하니까 추가 연결 작업 필요 없음
- 엔드포인트를 router에 등록하면 `app.include_router(router)`가 필요
    - router에 엔드포인트를 등록하니까 추가로 app에 등록해야 함

# 5. Pydantic BaseModel 활용
### Pydantic
- Python 타입 힌트를 이용해 데이터를 자동으로 검증해주는 라이브러리
    - 잘못된 타입이 들어오면 자동으로 에러를 발생
- 요청 스키마 정의 : 클라이언트가 보내는 데이터의 규격(틀)을 정의
    - 규격에 맞지 않으면 FastAPI가 자동으로 422 Unprocessable Entity 에러를 반환
#### Field
- 세부 조건 추가
- `min_length` / `max_length`: 문자열 길이
- `ge` (greater or equal): 이상 / `le` (less or equal): 이하
- `gt` / `lt`: 초과 / 미만
- `default`: 기본값
``` python
content: str = Field(min_length=1, max_length=5)   # 1~5자
max_tokens: int = Field(default=500, ge=1, le=2000)  # 1~2000 사이만 허용
```
- [실습] 03_prac.py : AI 설정 및 텍스트 검증기 완성하기

### 응답 스키마 정의
- 서버가 반환하는 응답 데이터의 규격 정의
- response_model로 지정하면 Swagger UI에 응답 형식이 자동 문서화
### 이메일, 문자열 길이 검증
- EmailStr
``` Bash
pip install fastapi uvicorn "pydantic[email]"
```
``` python
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
```
    - 이메일 형식이여야 통과
### Pydantic 모델 상속과 코드 재사용
- Pydantic 모델을 상속해서 공통 필드를 재사용하고, 상황에 맞게 확장 가능
- 중복 코드 없이 기능을 확장 가능
``` python
from pydantic import BaseModel, Field
from datetime import datetime

# 1. 공통 베이스 (부모 클래스)
class BaseMessage(BaseModel):
    content: str = Field(max_length=500)
    language: str = "ko"


# 2. 일반 유저의 요청 데이터 구조
class MessageRequest(BaseMessage):
    user_id: int
    
    """
    content, language + user_id
    """

# 4. VIP 유저 전용 프리미엄 요청 데이터 구조
class PremiumMessageRequest(MessageRequest):
    priority: int = Field(default=1, ge=1, le=3)

    """
    content, language + user_id + priority
    """
```
- [실습] 04_prac.py : 대학생 커뮤니티 서비스 게시글 API 설계