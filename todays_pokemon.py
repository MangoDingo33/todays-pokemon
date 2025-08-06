import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import random

README_PATH = "README.md"

def check_url_exists(url):
    try:
        resp = requests.head(url, timeout=3)
        return resp.status_code == 200
    except requests.RequestException:
        return False

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

def get_pokemon_gif_url(name_en, dot_url, shiny_url):
    """
    Showdown 이름 기반 GIF 경로 반환.
    없으면 각각 PokéAPI PNG 경로로 fallback
    """
    gif_dot = f"http://play.pokemonshowdown.com/sprites/ani/{name_en.lower()}.gif"
    gif_shiny = f"http://play.pokemonshowdown.com/sprites/ani-shiny/{name_en.lower()}.gif"

    if not check_url_exists(gif_dot):
        gif_dot = dot_url
    if not check_url_exists(gif_shiny):
        gif_shiny = shiny_url

    return gif_dot, gif_shiny

def get_pokemon_info(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code != 200:
        return "포켓몬 정보를 불러오지 못했습니다."

    data = response.json()
    name_en = data['name']  # 보통 소문자
    id_ = data['id']
    name_ko = get_korean_name(id_)

    # 타입 - 한글명 리스트
    types_ko = []
    for t in data['types']:
        type_ko = get_type_ko(t['type']['url'])
        types_ko.append(type_ko if type_ko else t['type']['name'])
    types_str = ", ".join(types_ko) if types_ko else "정보 없음"

    # 특성 - 한글명 리스트
    abilities_ko = []
    for a in data['abilities']:
        ab_ko = get_ability_ko(a['ability']['url'])
        abilities_ko.append(ab_ko if ab_ko else a['ability']['name'])
    abilities_str = ", ".join(abilities_ko) if abilities_ko else "정보 없음"

    height = data['height'] / 10  # m
    weight = data['weight'] / 10  # kg
    artwork_url = data['sprites']['other']['official-artwork']['front_default']
    dot_url = data['sprites']['front_default']  # PNG fallback 도트
    shiny_url = data['sprites']['front_shiny']  # PNG fallback 이로치

    # Showdown GIF 이미지 URL (없으면 PNG로 대체)
    dot_gif, shiny_gif = get_pokemon_gif_url(name_en, dot_url, shiny_url)

    # 최신 울음소리 (있으면 추가)
    cries = data.get('cries', {})
    latest_cry = cries.get('latest')

    info = (
        f"# {name_ko if name_ko else '정보 없음'} (ID: {id_})\n"
        f"**영어 이름:** {name_en.title()}\n\n"
        f"**타입:** {types_str}\n\n"
        f"**키:** {height} m\n\n"
        f"**몸무게:** {weight} kg\n\n"
        f"**특성:** {abilities_str}\n\n"
        f"## 공식 일러스트\n"
        f"![]({artwork_url})\n\n"
        f"| 기본 | 이로치 |\n"
        f"|:----:|:------:|\n"
        f"| <img src=\"{dot_gif}\" width=\"200\"> | <img src=\"{shiny_gif}\" width=\"200\"> |\n\n"
    )

    if latest_cry:
        info += f"**울음소리:**<br><audio controls src=\"{latest_cry}\"></audio>\n\n"

    return info

def update_readme():
    """README.md 파일을 업데이트 (무작위 포켓몬 정보)"""
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
