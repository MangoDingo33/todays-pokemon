import requests

def get_pokemon_info(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data['name'].title()}")
        print(f"ID: {data['id']}")
        print("Types:", ", ".join([t['type']['name'] for t in data['types']]))
        print(f"Height: {data['height'] / 10} m")
        print(f"Weight: {data['weight'] / 10} kg")
        print("Abilities:", ", ".join([a['ability']['name'] for a in data['abilities']]))
        
        # 이미지 URL 출력
        print("Images:")
        # 일러스트
        print("-", "일러스트:", data['sprites']['other']['official-artwork']['front_default'])
        # 도트
        print("-", "도트:", data['sprites']['front_default'])
        # 이로치
        print("-", "이로치:", data['sprites']['front_shiny'])
    else:
        print("포켓몬 정보를 가져오는데 실패했습니다.")

if __name__ == "__main__":
    get_pokemon_info('ditto')
