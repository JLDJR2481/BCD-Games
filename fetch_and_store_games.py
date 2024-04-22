from pymongo import MongoClient
import requests
import math
import dotenv
import os
import concurrent.futures
import httpx
import time


def get_games(page):
    params = {
        "key": dotenv.get_key(dotenv.find_dotenv(), 'RAWG_API_KEY'),
        "page_size": 40,
        "ordering": "-released",
        "page": page
    }

    with httpx.Client() as client:
        for _ in range(3):
            try:
                response = client.get(
                    "https://api.rawg.io/api/games", params=params, timeout=15.0)
                return response.json()['results']
            except httpx.ReadTimeout:
                print('Timeout error. Retrying...')
                time.sleep(5)
        return None


def store_games(games):
    gameData = []
    for game in games:
        if game.get("released") != None:
            if game['id'] not in existing_game_ids:
                gameData.append({
                    "id": game['id'],
                    "name": game['name'],
                })

    if gameData:
        collection.insert_many(gameData)


# Limpiamos la consola
os.system('clear')

# Cargamos de forma previa las variables de entorno
dotenv.load_dotenv(dotenv.find_dotenv())

# Conexión a la base de datos
uri = dotenv.get_key(dotenv.find_dotenv(), 'MONGO_URI')
client = MongoClient(uri)


# Obtención de la base de datos, la colección y los documentos ya existentes
try:
    db = client.get_database('Games')
    collection = db.get_collection('games-id')
    print("Conexión a la base de datos establecida.")

except Exception as e:
    print(e)

# Tamaño del lote
batch_size = 100000

# Número total de juegos en la colección
total_games = collection.count_documents({})

# Número de lotes
num_batches = math.ceil(total_games / batch_size)

existing_game_ids = set()

for i in range(num_batches):
    # Obtén el lote actual de juegos
    batch = collection.find({}).skip(i * batch_size).limit(batch_size)

    # Añade los IDs de los juegos al conjunto
    for game in batch:
        existing_game_ids.add(game['id'])

# Lanzamos una petición inicial para obtener los primeros 40 juegos, la cantidad total de juegos disponibles y la cantidad de peticiones que se han de realizar en el momento de la ejecución
response = requests.get("https://api.rawg.io/api/games", params={
                        "key": dotenv.get_key(dotenv.find_dotenv(), 'RAWG_API_KEY'), "page_size": 1})
# Se calcula el número de peticiones que se han de realizar para obtener todos los juegos (Se aproxima hacia arriba siempre)
totalPages = math.ceil(response.json()['count'] / 40)

print(f"Paginas de juegos totales: {totalPages}")

# Iteramos en los juegos. Esto nos sirve para obtener los primeros 40 juegos y guardarlos en la base de datos en caso de que estén en el mercado y no estén ya en la base de datos. Además, revisamos el primer y último juego de la petición, de forma que si ambos released's son None, pasará de realizar el bucle
counter = 1
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
    pages = range(1, totalPages)
    results = executor.map(get_games, pages)

    for games in results:
        store_games(games)
        counter += 1
        print(f"Petición {counter} de {totalPages} realizada.")
