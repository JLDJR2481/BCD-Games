from redis import Redis
from pymongo import MongoClient
import dotenv

# Carga de variables del sistema
dotenv.load_dotenv(dotenv.find_dotenv())

# Conexión a MongoDB en Remoto
uri = dotenv.get_key(dotenv.find_dotenv(), 'MONGO_URI')

try:
    client = MongoClient(uri)
    db = client.get_database('Games')
    collection = db.get_collection('games-id')
    print("Conexión a la base de datos establecida.")

except Exception as e:
    print(e)


# Conexión a Redis en Remoto
try:
    redis = Redis(
        host=dotenv.get_key(dotenv.find_dotenv(), 'REDIS_HOST'),
        port=13121,
        username=dotenv.get_key(dotenv.find_dotenv(), 'REDIS_USER'),
        password=dotenv.get_key(dotenv.find_dotenv(), 'REDIS_PASSWORD')
    )
    print("Conexión a Redis establecida.")
except Exception as e:
    print(e)

# Función que devuelve los juegos almacenados previamente. Primero, revisará en Redis la existencia de alguna clave que permita recuperar los juegos. En caso de no encontrarla, se conectará a MongoDB para recuperar los juegos.


def get_game(input):
    input = input.lower()
    games = redis_search(input)

    if games:
        print('Existe en Redis')
        return (game.decode("utf-8") for game in games)

    else:
        print('No existe en Redis')
        games = mongo_search(input)
        if games:
            store_cache_redis(games)

        return games


# Función que busca los juegos en MongoDB
def mongo_search(input):
    query = {"name": {"$regex": f"^{input}", "$options": "i"}}
    mongo_games = collection.find(query)

    return list(map(lambda game: game.get('name'), mongo_games))

# Función que busca los juegos en Redis


def redis_search(input):
    all_games = {game.decode("utf-8") for game in redis.smembers('games')}
    input_set = {game for game in all_games if game.startswith(input)}
    return all_games & input_set

# Procedimiento para almacenar los juegos dentro de la caché de Redis


def store_cache_redis(games):
    redis.sadd('games', *games)
