from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

# 1. 모든 모델의 뼈대가 되는 공통 모델을 정의하세요
class PostBase(BaseModel):
    # 내용을 작성하세요
    title: str = Field(min_length=2, max_length=50)
    content: str = Field(min_length=5)
    is_anonymous: bool = Field(default=True)


# 2. 게시글 작성 요청 모델을 정의하세요 (상속 활용)
class PostCreate(PostBase):
    # 내용을 작성하세요
    author_ip: str = Field(default="127.0.0.1")

# 3. 게시글 응답 모델을 정의하세요 (상속 활용)
class PostResponse(PostBase):
    # 내용을 작성하세요
    id: int
    created_at: datetime

# 4. 엔드포인트를 완성하세요 (경로, response_model, 파라미터 설정)
@app.post("/posts", response_model=PostResponse)
def create_post(post : PostResponse):
    # 실제로는 DB에 저장되는 데이터라고 가정합니다.
    db_data = {
        "id": 101,
        "title": post.title,
        "content": post.content,
        "is_anonymous": post.is_anonymous,
        "author_ip": post.author_ip, # 5. 요청에는 있었지만 응답 모델에는 없으므로 숨겨져야 함
        "created_at": datetime.now()
    }
    return db_data