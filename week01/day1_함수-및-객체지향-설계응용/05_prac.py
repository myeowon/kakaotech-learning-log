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

class LogBot(BasicBot):
    def say(self, msg):
        print("--- 로그 기록 중 ---")
        return super().say(msg)

l_bot = LogBot()
print(l_bot.say("로그 봇 결과"))