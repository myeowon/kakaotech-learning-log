# 아래를 Early Return 패턴으로 바꿔보세요
def send_message(user, message):
    if not user:
        return {"status": "error", "reason": "사용자 없음"}
    if not message:
        return {"status": "error", "reason": "메시지 없음"}
    if len(message) > 200:
        return {"status": "error", "reason": "메시지 너무 김"}
    return {"status": "ok", "msg": message}

# def send_message(user, message):
#     if not user:
#         return {"status": "error", "reason": "사용자 없음"}

#     if not message:
#         return {"status": "error", "reason": "메시지 없음"}

#     if len(message) > 200:
#         return {"status": "error", "reason": "메시지 너무 김"}

#     return {"status": "ok", "msg": message}

print(send_message(None, "안녕하세요"))
print(send_message("문땡땡", ""))
print(send_message("문땡땡", "안녕하세요" * 50))
print(send_message("문땡땡", "안녕하세요"))