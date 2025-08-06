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

def get_type_ko(type_url):
    """타입 URL로 한글 타입명 조회"""
    response = requests.get(type_url)
    if response.status_code == 200:
        data = response.json()
        for entry in data['names']:
            if entry['language']['name'] == 'ko':
                return entry['name']
    return None

def get_ability_ko(ability_url):
    """특성 URL로 한글 특성명 조회"""
    response = requests.get(ability_url)
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

        # 타입 - 한글 표기 리스트 만들기
        types_ko = []
        for t in data['types']:
            type_ko = get_type_ko(t['type']['url'])
            types_ko.append(type_ko if type_ko else t['type']['name'])
        types_str = ", ".join(types_ko) if types_ko else "정보 없음"

        # 특성 - 한글 표기 리스트 만들기
        abilities_ko = []
        for a in data['abilities']:
            ab_ko = get_ability_ko(a['ability']['url'])
            abilities_ko.append(ab_ko if ab_ko else a['ability']['name'])
        abilities_str = ", ".join(abilities_ko) if abilities_ko else "정보 없음"

        height = data['height'] / 10  # m
        weight = data['weight'] / 10  # kg
        artwork_url = data['sprites']['other']['official-artwork']['front_default']
        dot_url = data['sprites']['front_default']
        shiny_url = data['sprites']['front_shiny']

        info = (
            f"# {name_ko if name_ko else '정보 없음'} (ID: {id_})\n"
            f"**영어 이름:** {name_en}\n\n"
            f"**타입:** {types_str}\n\n"
            f"**키:** {height} m\n\n"
            f"**몸무게:** {weight} kg\n\n"
            f"**특성:** {abilities_str}\n\n"
            f"## **공식 일러스트** \n"
            f"![]({artwork_url})\n"
            f"| 도트 | 이로치 |\n"
            f"|:----:|:------:|\n"
            f"| <img src=\"{dot_url}\" width=\"200\"> | <img src=\"{shiny_url}\" width=\"200\"> |\n"
            f"\n"
        )
        return info
    else:
        return "포켓몬 정보를 불러오지 못했습니다."

def update_readme():
    """README.md 파일을 업데이트 (랜덤 숫자 아이디로 포켓몬 정보)"""
    pokemon_id = random.randint(1, 1025)
    pokemon_info = get_pokemon_info(pokemon_id)

    now_kst = datetime.now(ZoneInfo("Asia/Seoul"))
    now_str = now_kst.strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
⏳ 업데이트 시간: {now_str} (KST) ⏳

🤖 자동 업데이트 봇에 의해 관리됩니다! 🤖

---

{pokemon_info}
---
"""
    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
