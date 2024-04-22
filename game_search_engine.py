from redis import Redis
# from pymongo import MongoClient
import dotenv
import time
import httpx

# Carga de variables del sistema
dotenv.load_dotenv(dotenv.find_dotenv())
env = dotenv.dotenv_values()

# Conexión a Redis en Remoto
try:
    redis = Redis(
        host=env['REDIS_HOST'],
        port=13121,
        username=env['REDIS_USER'],
        password=env['REDIS_PASSWORD'],
    )
    print("Conexión a Redis establecida.")
except Exception as e:
    print(e)

# Función que devuelve los juegos almacenados previamente. Primero, revisará en Redis la existencia de alguna clave que permita recuperar los juegos. En caso de no encontrarla, se conectará a MongoDB para recuperar los juegos.


def get_game(input):
    games = redis_search(input.capitalize())

    if games:
        return (game.decode("utf-8") for game in games)

    else:
        games = mongo_search(input)
        if games:
            store_cache_redis(games)
        return games


def mongo_search(input):
    urlEndpoint = env["URL_ENDPOINT"]
    url = f"{urlEndpoint}/action/find"
    data = {
        "dataSource": env['DATASOURCE'],
        "database": env['DATABASE'],
        "collection": env['COLLECTION'],
        "filter": {"name": {"$regex": f"^{input}", "$options": "i"}},
        "projection": {
            "_id": 0
        },
        # "limit": 10
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": env['MONGO_API_KEY']

    }

    response = httpx.post(url, json=data, headers=headers)

    mongo_games = response.json()

    return list(map(lambda game: game.get('name'), mongo_games.get('documents')))

# Función que busca los juegos en Redis


def redis_search(input):
    games = redis.zrangebylex('games', f"[{input}", f"[{input}\xff")
    return games

# Procedimiento para almacenar los juegos dentro de la caché de Redis


def store_cache_redis(games):
    redis.zadd('games', {game: 0 for game in games})


if __name__ == "__main__":

    start_time = time.time()
    get_game('Cou')
    end_time = time.time()
    print(f"Tiempo total de ejecución: {end_time - start_time} segundos.")
