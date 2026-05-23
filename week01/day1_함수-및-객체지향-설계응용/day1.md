# 함수 및 객체 지향 설계 응용

## 1. 함수 설계 — 읽기 좋은 함수 만들기
### **함수 분리 (Single Responsibility)**
- 한 함수가 한 가지 역할을 가지는 원칙, 테스트하기 쉽고 코드를 이해하기 쉬움.
- 기능마다 함수를 만들고, 메인은 함수를 순서대로 실행

### **Early Return**
- 실패 조건을 먼저 처리(return)함
- [실습] 01_prac.py : Early Return으로 리팩토링해보기

### ***가변 인자 (args, *kwargs)***
- 함수를 만들 때 인자 개수를 사전에 알 수 없을 때 사용
    - def func(name, *args, **kwargs)
    - 주의 : 함수 인자는 일반 인자 → *args → **kwargs 순서로 작성해야 함
- ***args (가변 위치 인자)** : 인자들의 값만 쉼표로 나열하여 전달, 튜플로 묶임, 개수가 정해지지 않은 여러 개의 단순 데이터를 한 번에 받을 때 사용
    - func("사과", "바나나")
- ****kwargs (가변 키위드 인자)** : "이름=값"의 형태로 지정하여 전달, 딕셔너리로 묶임, 개수가 정해지지 않은 추가 옵션/설정값을 유연하게 받을 때 사용
    - func(model="gpt", temp=0.7)
```python
# **kwargs — 이름 있는 추가 옵션 (딕셔너리로 받음)
def call_ai(prompt, **kwargs):
    options = {"model": "gpt-4", "temperature": 0.7}  # 기본값
    options.update(kwargs)                            # 추가 옵션으로 덮어씀
    print(f"프롬프트: {prompt}")
    print(f"옵션: {options}")

call_ai("안녕!")
call_ai("사진 분석", model="gpt-4o", temperature=0.2)
```
### **모듈형 코드 설계 실습**
- 기능별로 파일(모듈)을 나눔
- [실습] 02_prac.py : validators.py 완성하기

## 2. 객체지향 설계
### **상태와 책임 분리**
- 상태: 객체가 기억하고 있는 것
- 책임: 객체가 스스로 수행하는 기능
- 객체지향 설계를 하는 이유
    - 수정하기 쉽다. 다른 객체를 건드릴 필요가 없음.
    - 재사용성. 
    - 확장이 쉬움.
``` python
    class ChatSession:
    def __init__(self, user_name):
        self.user_name = user_name     # 상태: 이 객체만의 데이터
        self.messages = []

    def add_message(self, role, content):   # 책임: 이 객체가 할 수 있는 일
        self.messages.append({"role": role, "content": content})

    def get_summary(self):
        return f"{self.user_name}의 대화 ({len(self.messages)}개)"

    # 각 유저는 완전히 독립된 세션을 가진다
    session_a = ChatSession("철수")
    session_b = ChatSession("영희")

    session_a.add_message("user", "안녕!")
    print(session_a.get_summary())   # 철수의 대화 (1개)
    print(session_b.get_summary())   # 영희의 대화 (0개) — 서로 영향 없음
``` 
###  🤔 ```self```  
- 이 메서드를 호출한 객체 자신
- ```session_a.add_message("user", "안녕!")``` 로 쓰면 자동으로 ```session_a```이 첫 번째 인자인 self로 넘어감.
- 그래서 클래스의 인스턴스 메서드 정의에서 첫 번째 매개변수로 self를 적지 않으면, 자동으로 전달되는 인스턴스를 받을 자리가 없어서 ```TypeError: func() takes 0 positional arguments but 1 was given``` 라는 오류 발생
- 필요한 이유 : 객체마다 자기만의 데이터를 가지기 위함.

### Data Class
- 데이터를 저장하는 용도의 클래스를 간결하고 가독성 있게 정의하게 해주는 표준 라이브러리
- 초기화·출력·비교 메서드가 자동으로 생성
- 정보를 보관하는 게 주 목적인 클래스를 만들 때 사용
- **매직 메서드** : 파이썬의 클래스 안에 정의할 수 있는 특별한 메서드, 개발자가 직접 함수 호출하지 않아도 특정 상황에서 자동으로 호출
    - `init` : 객체 생성 시 필요한 속성 설정
    - `repr` : 개발자가 객체 상태를 파악하기 쉽게 출력
    - `eq` : 내부의 값을 기준으로 같은지 판단
    - `str` : 사용자가 보기 쉬운 문자열


#### 기존 방식
``` python 
class UserOld:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        # !r을 사용하면 문자열에 자동으로 따옴표(')가 붙어 출력됩니다.
        return f"UserOld(name={self.name!r}, age={self.age})"

u1 = UserOld("카카오", 23, "k@k.com")
u2 = UserOld("카카오", 23, "k@k.com")

print(u1)        
# 출력: UserOld(name='카카오', age=23) -> __repr__ 덕분에 이렇게 나옴
print(u1 == u2)  
# 출력: False -> __eq__를 안 만들었기 때문에 메모리 주소로 비교함

print("-" * 50)
```

#### @dataclass 방식 — __init__, __repr__, __eq__ 자동 생성
``` python 
from dataclasses import dataclass, field
from typing import List
@dataclass
class User:
    name: str
    age: int
    email: str
    tags: List[str] = field(default_factory=list)  

user1 = User(name="카카오", age=23, email="kakao@kakao.com")
user2 = User(name="카카오", age=23, email="kakao@kakao.com")

print(user1)           # 출력: User(name='카카오', age=23, email='kakao@kakao.com', tags=[])
print(user1 == user2)  # 출력: True -> 값이 같으면 같은 객체로 판단 (__eq__ 자동 구현)
```
- `tags: List[str] = field(default_factory=list)`
    - 리스트 기본값은 반드시 field() 사용
    - 일반 클래스 : tags = [] 로 쓰면 모든 인스턴스가 리스트를 공유
    - @dataclass : 이를 방지하기 위해 tags = [] 라고 쓰면 ValueError를 발생
    - 따라서 "인스턴스마다 새 리스트를 만들어라"라는 의미로 field(default_factory=list)를 써야 함
    - 그럼 모든 인스턴스가 리스트를 공유하고 싶다면?
        - 클래스 변수로 선언하기 : `tags: ClassVar[List[str]] = []`
        - 클래스 전체가 공유하는 값이 됨

#### 캡슐화
- 데이터(상태)와 그 데이터를 다루는 기능(메서드)을 하나로 묶고, 외부에서 내부의 데이터를 함부로 들여다보거나 수정하지 못하게 막는 것
- 변수 앞에 "_"를 붙여서 직접 접근 금지를 약속한다.
    - `instance._value` : 가능은 하지만, 추천하지 않는 코드
- 인스턴스 메서드 위에 @property를 붙여 읽기만 허용

``` python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0           # _ : "직접 접근 금지" 약속

    # 안전하게 읽기만 허용 (@property)
    @property
    def balance(self):
        return self._balance

account = BankAccount("카카오")

print(f"현재 잔액: {account.balance}원")

# ❌ 위험한 방식 (직접 수정 시도)
# account.balance = 1000000    # 에러 발생! (@property라 수정 불가)
# account._balance = 1000000   # 가능은 하지만, 추천하지 않는 코드
```

### 확장 가능한 클래스 설계 실습 (상속)
- 처음부터 다시 만들지 말고, 있는 기능을 상속받아 필요한 부분만 추가 / 수정한다는 개념
- 상속은 "A는 B다 (is-a)" 관계일 때만 사용

#### 1단계: 기능 추가 (Extension)
- 부모의 기능을 베이스로 새로운 기능이 더 생기는 경우
``` python
class BasicBot:
    def say(self, msg):
        return f"응답: {msg}"

# BasicBot을 상속받아 기능을 '추가'함
class MusicBot(BasicBot):
    def play_music(self):
        return "🎵 음악을 재생합니다."

bot = MusicBot()
print(bot.say("안녕하세요"))      # 부모 기능 그대로 사용
print(bot.play_music())    # 내 기능 추가 사용
```
- [실습] 03_prac.py : 날씨 챗봇 만들기

#### 2단계: 기능 수정 (Overriding)
- 부모의 기능을 덮어쓰기함
``` python
# 부모 클래스: 기본형 챗봇
class BasicBot:
    def say(self, msg):
        return f"🤖 [기본 응답]: {msg}"


# 자식 클래스: 부모의 특정 기능을 내 방식대로 '덮어쓴' 챗봇
class OverrideBot(BasicBot):
    # 부모와 '완전히 똑같은 이름'의 함수를 만들면 덮어쓰기(오버라이딩)가 됩니다.
    def say(self, msg):
        return f"✨ [덮어쓴 응답]: {msg}"

# 1. 기본형 봇에게 말을 걸었을 때
basic = BasicBot()
print("1. 기본형 봇의 결과:")
print(basic.say("안녕하세요"))

print("-" * 60)

# 2. 덮어쓰기형 봇에게 똑같이 말을 걸었을 때
override = OverrideBot()
print("2. 덮어쓰기형 봇의 결과:")
print(override.say("안녕하세요, 저는 님을 도우러 온 사람입니다."))  # 똑같은 say를 호출했지만 출력 결과가 다름
```
- [실습] 04_prac.py : 영어 챗봇 만들기

#### 3단계: 부모 기능 활용하기
- 부모가 한 일에 내 할 일을 살짝 '덧붙이는' 경우
``` python
class BasicBot:
    def say(self, msg):
        # 부모가 담당하는 '복잡하고 귀찮은' 작업들
        print("[시스템] DB에 메시지 기록 중...")
        print("[시스템] 욕설 필터링 검사 중...")
        return f"응답: {msg}"

class PremiumBot(BasicBot):
    def say(self, msg):
        # 1. 부모가 하던 일을 먼저 시킴(super)
        res = super().say(msg)
        
        # 2. 부모가 일처리를 끝내고 준 결과물(res)에 내 것만 살짝 얹음
        return f"⭐[VIP] {res}"

bot = PremiumBot()
print(bot.say("오늘 하루 고생하셨습니다"))
```
- [실습] 05_prac.py : 로깅 챗봇 만들기

### 다형성(Polymorphism)과 추상화(Abstraction)
- **다형성(Polymorphism)**
    - 같은 메서드 이름인데, 클래스마다 다르게 동작하는 개념
    ``` python
    class KakaoBot:
        def respond(self, msg):
            return f"카카오: {msg}에 답변드립니다"

    class ClovaBot:
        def respond(self, msg):
            return f"클로바: {msg}를 분석했어요"

    # 어떤 봇인지 몰라도 respond()를 호출하면 각자 알아서 동작
    bots = [KakaoBot(), ClovaBot()]
    for bot in bots:
        print(bot.respond("날씨 알려줘"))
    # 카카오: 날씨 알려줘에 답변드립니다
    # 클로바: 날씨 알려줘를 분석했어요
    ```
- **추상화 (Abstraction)**
    - 내부 구현은 몰라도 되고, 어떻게 쓰는지만 알면 된다는 개념
    - `@abstractmethod`가 메서드에 붙어있으면 자식이 이 메서드를 꼭 구현해야 함.
    ``` python
    from abc import ABC, abstractmethod

    class BaseBot(ABC):
        @abstractmethod
        def respond(self, msg: str) -> str:
            """이 메서드는 반드시 구현해야 해요"""
            pass

    class KakaoBot(BaseBot):
        def respond(self, msg):
            return f"카카오 답변: {msg}"

    # BaseBot()  → 직접 생성하면 에러 (추상 클래스는 직접 쓸 수 없음)
    # KakaoBot() → respond()를 구현했으니 OK
    ```

### 조합 (Composition) — 기능이 필요하면 속성으로 가지기
- ChatBot에 번역 기능이 필요하다면? ChatBot이 번역기를 '가지도록' 만들기
- Translator is a ChatBot은 아니기 때문에 상속은 X
``` python
# ChatBot에 번역 기능이 필요하다면? ChatBot이 번역기를 '가지도록' 만들어요
class Translator:
    def translate(self, text):
        return f"[EN] {text}"  # 실제론 번역 API 호출

class ChatBot:
    def __init__(self, name):
        self.name = name
        self.translator = Translator()  # 상속 대신 속성으로 포함

    def respond(self, msg):
        return f"{self.name}: {msg}에 대한 답변"

    def respond_in_english(self, msg):
        response = self.respond(msg)
        return self.translator.translate(response)

bot = ChatBot("카카오봇")
print(bot.respond("안녕"))
# 카카오봇: 안녕에 대한 답변

print(bot.respond_in_english("안녕"))
# [EN] 카카오봇: 안녕에 대한 답변
```
- [실습] 06_prac.py : CafeMenu 클래스 완성하기