from dataclasses import dataclass

@dataclass
class CafeMenu:
    name: str
    price: int
    
    # [미션 1] 외부에서 직접 수정할 수 없는 '내부용 재고 변수'를 만드세요.(캡슐화)
    # ✏️ [미션 1] 내부용 재고 변수를 선언하세요 (변수명 앞에 _ 를 붙여 캡슐화)
    # 형식: _변수명: int = 10  (예: _stock: int = 10)
    _stock : int = 10

    # ✏️ [미션 2] @property 데코레이터를 사용해 외부 읽기 전용 속성을 만드세요
    # 이 메서드 위에 @property를 추가하세요
    @property
    def stock(self):
        return  self._stock # 여기에 내부 재고 변수를 반환하세요

    # ✏️ [미션 3] Early Return 패턴을 사용하여 주문 함수를 완성하세요
    def order(self, quantity=1):
        # ✏️ [미션 3-1] 수량이 0 이하일 때 "수량 오류"를 반환하는 조건문을 작성하세요
        if quantity <= 0:  # 여기에 조건식을 작성하세요
            return "수량 오류"
            
        # ✏️ [미션 3-2] 재고가 부족할 때 "재고 부족 (현재 n개)"를 반환하는 조건문을 작성하세요
        if self._stock < quantity :  # 여기에 조건식을 작성하세요
            return f"재고 부족 (현재 {self._stock}개)"
        
        # ✏️ [미션 3-3] 재고를 차감하는 코드를 작성하세요
        # 여기에 재고 차감 코드를 작성하세요
        self._stock = self._stock - quantity
        return f"{self.name} {quantity}잔 주문 완료"


# --- 아래는 코드 검증을 위한 테스트 구문입니다 ---
coffee = CafeMenu("아메리카노", 4500)

print(coffee.order(2))    # 아메리카노 2잔 주문 완료
print(f"남은 재고: {coffee.stock}") # 확인 가능

print(coffee.order(0))    # 수량 오류
print(coffee.order(15))   # 재고 부족 (현재 8개)

# 직접 수정 시도 (에러가 나야 캡슐화 성공!)
try:
    coffee.stock = 100
except AttributeError:
    print("성공: 재고를 직접 수정할 수 없습니다.")