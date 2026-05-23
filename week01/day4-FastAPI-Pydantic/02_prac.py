from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

# [문제 1] FastAPI 객체 생성하기
# 여기에 코드를 작성하세요
app = FastAPI()
router = APIRouter(prefix="/reviews", tags=["reviews"])

# 실습용 기본 데이터
univ_reviews = {
    "강원대": "캠퍼스가 넓고 공기가 좋아요!",
    "경북대": "전통 있는 명문대, 공부하기 좋은 분위기입니다.",
    "부산대": "주변에 맛집이 많고 활기차요!",
    "전남대": "도서관 시설이 정말 최고입니다.",
    "충남대": "교통이 편리하고 연구 시설이 잘 되어 있어요."
}

# [문제 2] 리뷰 등록을 위한 Pydantic 모델 정의하기
# 여기에 코드를 작성하세요
class ReviewCreate(BaseModel):
    univ_name: str
    review: str


@router.get("/")
def get_all_reviews():
    return univ_reviews

# [문제 3] 특정 대학교 리뷰 조회 API (GET) 구현하기
# 경로: /reviews/{univ_name}
# 여기에 코드를 작성하세요
@router.get("/{univ_name}")
def get_review(univ_name : str):
    if univ_name not in univ_reviews:
        raise HTTPException(
            status_code=404,
            detail=f"{univ_name}를 찾을 수 없습니다"
        )
    return univ_reviews[univ_name]


# [문제 4] 새로운 리뷰 등록 API (POST) 구현하기
# 경로: /reviews
# 아래 코드를 활용해 작성하세요
@router.post("/")
def add_review(request : ReviewCreate):
    # 딕셔너리에 데이터 추가하기: 딕셔너리명['키'] = 값
    univ_reviews[request.univ_name] = request.review
    return {"message": f"{request.univ_name} 리뷰가 등록되었습니다."}

app.include_router(router)
# http://localhost:8000/docs