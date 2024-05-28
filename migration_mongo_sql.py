from searchEngine.models import Game
import json

# Script para la terminal de Django que permite, desde un archivo JSON, añadir todos los videojuegos en la BBDD SQLite3


with open('games.json', 'r', encoding="utf-8") as file:
    files = json.load(file)

for file in files:
    data = file["fields"]
    Game.objects.create(
        game_id=data['game_id'],
        name=data['name'],
        translated_description_es=data['translated_description_es'],
        metacritic=data['metacritic'],
        released=data['released'],
        background_image=data['background_image'],
        average_rating=data['average_rating'],
        platforms=data['platforms'],
        stores=data['stores'],
        genres=data['genres'],
        tags=data['tags'],
        developers=data['developers'],
        publishers=data['publishers'],
        esbr_ratings=data['esbr_ratings']
    )
