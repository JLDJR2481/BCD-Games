import dotenv
from pymongo import MongoClient
from searchEngine.models import Game

# Script para lanzar en la terminal de Django (py manage.py shell) que permite interactuar en los juegos guardados en un cliente MongoDB en Docker y pasarlo al ORM de Django (en este caso, en SQLite3)

dotenv.load_dotenv()

db_client = MongoClient('localhost', 27017)
bcdGamesDB = db_client['bcdGames']
gamesCollection = bcdGamesDB['games']

games = gamesCollection.find()

for game in games:
    Game.objects.create(
        game_id=game['id'],
        name=game['name'],
        translated_description_es=game['translated_description_es'],
        metacritic=game['metacritic'],
        released=game['released'],
        background_image=game['background_image'],
        average_rating=game['average_rating'],
        platforms=game['platforms'],
        stores=game['stores'],
        genres=game['genres'],
        tags=game['tags'],
        developers=game['developers'],
        publishers=game['publishers'],
        esbr_ratings=game['esbr_ratings']
    )
