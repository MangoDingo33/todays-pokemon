import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import random

now = datetime.now()

MIN = now.minute
JSON_PATH = "/tmp/test.json"
URL = f"https://jsonplaceholder.typicode.com/todos/{MIN}"


def get_data():
    """API를 호출"""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "정보를 가져오는 데 실패했습니다."

def update_json():
    """test.json 파일을 업데이트"""
    weather_info = get_data()
    
    # UTC 현재 시간 가져와서 한국 시간으로 변환 (UTC+9)
    now_utc = datetime.utcnow()
    now_kst = now_utc + timedelta(hours=9)
    now_str = now_kst.strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
⏳ 업데이트 시간: {now_str} (KST) ⏳

🤖 자동 업데이트 봇에 의해 관리됩니다! 🤖

---

> {weather_info}
---
"""
    with open(JSON_PATH, "a", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_json()


