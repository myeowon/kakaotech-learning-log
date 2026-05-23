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

# BasicBot을 상속받는 WeatherBot 클래스를 만들어봅시다. 
# 이 챗봇은 부모의 say 기능 외에, "오늘 날씨는 맑습니다."를 반환하는 get_weather() 메서드를 추가로 가져야 합니다.

class WeatherBot(BasicBot):
    def get_weather(self):
        return "오늘 날씨는 맑습니다."

weather_bot = WeatherBot()
print(weather_bot.say("안녕하세요"))
print(weather_bot.get_weather())