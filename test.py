import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import random

README_PATH = "README.md"

def get_korean_name(pokemon_id):
    """포켓몬 번호로 한국어 이름 추출"""
    url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for entry in data['names']:
            if entry['language']['name'] == 'ko':
                return entry['name']
    return None

def get_pokemon_info(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name_en = data['name'].title()
        id_ = data['id']
        name_ko = get_korean_name(id_)
        types = ", ".join([t['type']['name'] for t in data['types']])
        height = data['height'] / 10  # m
        weight = data['weight'] / 10  # kg
        abilities = ", ".join([a['ability']['name'] for a in data['abilities']])
        artwork_url = data['sprites']['other']['official-artwork']['front_default']
        dot_url = data['sprites']['front_default']
        shiny_url = data['sprites']['front_shiny']

        info = (
            f"# {name_ko if name_ko else '정보 없음'} (ID: {id_})\n"
            f"**영어 이름:** {name_en}\n\n"
            f"**타입:** {types}\n\n"
            f"**키:** {height} m\n\n"
            f"**몸무게:** {weight} kg\n\n"
            f"**특성:** {abilities}\n\n"
            f"## **[공식 일러스트]** \n"
            f"![]({artwork_url})\n"
            f"##\n"
            f"| 도트 | 이로치 |\n"
            f"|:----:|:------:|\n"
            f"| <img src=\"{dot_url}\" width=\"200\"> | <img src=\"{shiny_url}\" width=\"200\"> |\n"
            f"\n"
        )
        return info
    else:
        return "포켓몬 정보를 불러오지 못했습니다."

def update_readme():
    """README.md 파일을 업데이트 (숫자 아이디로 포켓몬 정보)"""
    pokemon_id = random.randint(1, 1025)  # 원하는 도감 번호로 변경
    pokemon_info = get_pokemon_info(pokemon_id)

    now_kst = datetime.now(ZoneInfo("Asia/Seoul"))
    now_str = now_kst.strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
⏳ 업데이트 시간: {now_str} (KST) ⏳

🤖 자동 업데이트 봇에 의해 관리됩니다. 🤖

---


{pokemon_info}
---
"""
    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
