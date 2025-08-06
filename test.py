import requests

def get_pokemon_form_info(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon-form/{pokemon_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # 폼 이름
        form_name = data.get("form_name") or data.get("name")
        # 폼 이미지 정보
        sprites = data.get("sprites", {})
        front_default = sprites.get("front_default")
        front_shiny = sprites.get("front_shiny")
        # 결과 예시 출력
        print("폼 이름:", form_name)
        print("기본 이미지:", front_default)
        print("이로치 이미지:", front_shiny)
        return data
    else:
        print("폼 정보를 불러오지 못했습니다.")
        return None

# 사용 예시
get_pokemon_form_info(132)
