from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.views.generic import ListView
from django.views.generic.detail import DetailView


from redis import Redis
import dotenv
import httpx

# Create your views here.
dotenv.load_dotenv(dotenv.find_dotenv())
env = dotenv.dotenv_values()


class BaseView(View):
    def __init__(self):
        self.redis = Redis(
            host=env['REDIS_HOST'],
            port=13121,
            username=env['REDIS_USER'],
            password=env['REDIS_PASSWORD'],
        )
        self.client = httpx.Client()
        self.urlEndpoint = env["URL_ENDPOINT"]
        self.dataSource = env['DATASOURCE']
        self.database = env['DATABASE']
        self.collection = env['COLLECTION']
        self.apiKey = env['MONGO_API_KEY']

        self.externalApiKey = env["RAWG_API_KEY"]
        self.externalApiUrl = env["RAWG_API_URL"]

    def get_game(self, input):
        games = self.redis_search(input)

        if games:
            return games
        else:
            games = self.mongo_search(input)
            if games:
                self.store_cache_redis(games)
            return games

    def mongo_search(self, input):
        urlEndpoint = self.urlEndpoint
        url = f"{urlEndpoint}/action/find"
        data = {
            "dataSource": self.dataSource,
            "database": self.database,
            "collection": self.collection,
            "filter": {"name": {"$regex": f"^{input}", "$options": "i"}},
            "projection": {
                "_id": 0
            },
        }

        headers = {
            "Content-Type": "application/json",
            "api-key": self.apiKey

        }

        response = self.client.post(url, json=data, headers=headers)

        mongo_games = response.json()
        return [{'id': game.get('id'), 'name': game.get('name')} for game in mongo_games.get('documents')]

    def redis_search(self, input):
        games = [game for game in self.redis.hgetall('games').items(
        ) if game[1].decode("utf-8").lower().startswith(input)]
        return [{'id': game[0].decode("utf-8"), 'name': game[1].decode("utf-8")} for game in games]

    def store_cache_redis(self, games):
        with self.redis.pipeline() as pipe:
            for game in games:
                pipe.hset('games', game['id'], game['name'])
            pipe.execute()


class SearchEngineView(BaseView):
    # Método GET para renderizar la página de inicio del motor de búsqueda

    def get(self, request):
        return render(request, "searchEngine/index.html")


class ResultsListView(BaseView, ListView):
    paginate_by = 30

    template_name = "searchEngine/results.html"

    def post(self, request, *args, **kwargs):
        input = request.POST.get('searchEngineInput')
        games = self.get_game(input)
        request.session['games'] = games
        return redirect('results')

    def get_queryset(self):
        games = self.request.session.get('games', [])
        return games

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = self.get_queryset()
        context['games'] = games
        if len(games) == 1:
            context['single_game'] = games[0]
        return context

    def render_to_response(self, context, **response_kwargs):
        if "single_game" in context:
            return redirect('details', game_id=context['single_game']['id'])
        return super().render_to_response(context, **response_kwargs)


class ResultDetailView(BaseView, DetailView):
    def get(self, request, game_id):
        game_id = int(game_id)
        url = f"{self.externalApiUrl}/{game_id}?key={self.externalApiKey}"

        game_details = self.client.get(url).json()

        return render(request, "searchEngine/details.html", {"game": game_details})
