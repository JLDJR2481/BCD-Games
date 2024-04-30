
import dotenv
import string

import httpx

import argostranslate.package
import argostranslate.translate

import json

from bs4 import BeautifulSoup

from pymongo import MongoClient, ASCENDING

dotenv.load_dotenv(dotenv.find_dotenv())
env = dotenv.dotenv_values()

apiKey = env['MONGO_API_KEY']

externalApiKey = env["RAWG_API_KEY"]
externalApiUrl = env["RAWG_API_URL"]

mongoDbUri = env["MONGO_URI"]

db_client = MongoClient('localhost', 27017)

bcdGamesDB = db_client['bcdGames']
gamesCollection = bcdGamesDB['games']


client = httpx.Client()


# Obtiene los paquetes de traducción que se han instalado de forma local para traducir el texto de Inglés a Español
def get_translation(from_code, to_code):
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next(
        (lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next(
        (lang for lang in installed_languages if lang.code == to_code), None)

    if from_lang is None or to_lang is None:
        print("No se pudo encontrar los idiomas de traducción")
        return None

    return from_lang.get_translation(to_lang)

# Accede a la BBDD de MongoDB en remoto (Donde se guardará una copia de la BBDD) y busca 10 juegos que empiecen por cada combinación de 2 letras disponibles


def get_games_with_letters():
    client = MongoClient(mongoDbUri)
    db = client.get_database('Games')
    collection = db.get_collection('games-id')

    collection.create_index([("name", ASCENDING)])

    letters = list(string.ascii_lowercase)
    games_id = set()

    for letter1 in letters:
        for letter2 in letters:
            search_string = f'{letter1}{letter2}'
            games = collection.find(
                {"name": {"$regex": f'^{search_string}', "$options": "i"}}, {"_id": 0, "id": 1}).limit(10)

            for game in games:
                games_id.add(game['id'])

    games_id_list = list(games_id)
    games_id_sorted_list = sorted(games_id_list)
    with open("games_id.json", "w") as file:
        json.dump(games_id_sorted_list, file)


translation = get_translation("en", "es")

# Traduce la descripción que es pasada por otra función


def translate_data(description):
    if translation is None:
        print("No se pudo obtener la traducción")
    else:
        return translation.translate(description)

# Obtiene los datos de los juegos de la API externa y los guarda en la BBDD de MongoDB de Docker


def fetch_and_store():
    with open("games_id.json", "r") as file:
        games_id = json.load(file)

    total_ids = len(games_id)
    counter = 1

    for id in games_id:
        try:
            response = client.get(
                f"{externalApiUrl}/{id}?key={externalApiKey}", timeout=5)
        except (httpx.ReadTimeout or httpx.ConnectTimeout):
            with open("id_failed.txt", "a+") as idFiles:
                idFiles.write(str(id))
                print(f"Error en la petición del id: {id}")
                print(f"{counter}/{total_ids}")
                counter += 1

        if response.status_code == 200:
            game_data = response.json()

            description = parserHtml(game_data["description"])
            translated_description = translate_data(description)

            data = {
                "id": game_data.get("id"),
                "name": game_data.get("name"),
                "description": description,
                "translated_description_es": translated_description,
                "metacritic": game_data.get("metacritic"),
                "released": game_data.get("released"),
                "updated": game_data.get("updated"),
                "background_image": game_data.get("background_image"),
                "website": game_data.get("website"),
                "average_rating": game_data.get("rating"),
                "ratings": [
                    {
                        "id": rating.get("id"),
                        "title": rating.get("title"),
                        "count": rating.get("count"),
                        "percent": rating.get("percent")
                    }
                    for rating in game_data.get("ratings", [])
                ],
                "platforms": [
                    {
                        "id": platform.get("platform", {}).get("id"),
                        "name": platform.get("platform", {}).get("name"),
                        "released_at": platform.get("released_at"),
                        "requirements": platform.get("requirements")
                    }
                    for platform in game_data.get("platforms", [])
                ],
                "stores": [
                    {
                        "id": store.get("store", {}).get("id"),
                        "store": store.get("store", {}).get("name")
                    } for store in game_data.get("stores", [])
                ],
                "genres": [
                    {
                        "id": genre.get("id"),
                        "name": genre.get("name")
                    } for genre in game_data.get("genres", [])
                ],
                "tags": [
                    {
                        "id": tag.get("id"),
                        "name": tag.get("name")
                    } for tag in game_data.get("tags", [])
                ],
                "developers": [
                    {
                        "id": developer.get("id"),
                        "name": developer.get("name")
                    } for developer in game_data.get("developers", [])

                ],
                "publishers": [
                    {
                        "id": publisher.get("id"),
                        "name": publisher.get("name")
                    } for publisher in game_data.get("publishers", [])
                ],
                "esbr_ratings": {
                    "id": game_data.get("esrb_rating").get("id") if game_data.get("esrb_rating") else None,
                    "name": game_data.get("esrb_rating").get("name") if game_data.get("esrb_rating") else None,
                }
            }

            gamesCollection.insert_one(data)
            with open("inserted_id.txt", "a+") as idFile:
                idFile.write(str(id) + "\n")
            print(f"{counter}/{total_ids}")
            counter += 1

# Parsea el HTML y obtiene el texto de la descripción


def parserHtml(description):
    return BeautifulSoup(description, 'html.parser').get_text()

# Comprueba cuantos documentos hay en la BBDD


def check_data():
    count = gamesCollection.count_documents({})
    print(count)

# Elimina los datos duplicados de la BBDD


def delete_duplicated_data():
    pipeline = [
        {"$group": {"_id": "$id", "unique_ids": {
            "$addToSet": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]

    duplicates = gamesCollection.aggregate(pipeline)

    for duplicate in duplicates:
        unique_ids = duplicate['unique_ids']

        del unique_ids[0]

        gamesCollection.delete_many({"_id": {"$in": unique_ids}})

# Comprueba los datos de un documento en concreto


def check_document_data(id):
    game = gamesCollection.find_one({"id": id})
    print(game)

# Elimina los ids que se han insertado en la BBDD


def delete_id():
    with open('inserted_id.txt', 'r') as file:
        first_list = [int(line.strip()) for line in file]

    with open("games_id.json", "r") as file:
        games_id = json.load(file)

    new_list = [
        game_id for game_id in games_id if game_id not in first_list]

    with open("games_id.json", "w") as file:
        json.dump(new_list, file)


if __name__ == "__main__":

    # fetch_and_store()
    check_data()
    check_document_data(76)

    delete_duplicated_data()

    check_data()
