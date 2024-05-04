from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import get_language
from django.contrib import messages
from .models import Game

from operator import itemgetter

from redis import Redis
import dotenv


# Create your views here.
dotenv.load_dotenv(dotenv.find_dotenv())
env = dotenv.dotenv_values()

redis = Redis(
    host=env['REDIS_HOST'],
    port=13121,
    username=env['REDIS_USER'],
    password=env['REDIS_PASSWORD'],
)


class BaseView(View):

    def get_game(self, input):
        games = self.redis_search(input)

        if games:
            return games
        else:
            games = self.search_game(input)
            if games:
                self.store_cache_redis(games)
            return games

    def search_game(self, input):
        games = Game.objects.filter(
            name__istartswith=input).values('id', 'name')
        return games

    def redis_search(self, input):
        games = [game for game in redis.hgetall('games').items(
        ) if game[1].decode("utf-8").lower().startswith(input)]
        return [{'id': game[0].decode("utf-8"), 'name': game[1].decode("utf-8")} for game in games]

    def store_cache_redis(self, games):
        with redis.pipeline() as pipe:
            for game in games:
                pipe.hset('games', game['id'], game['name'])
            pipe.expire('games', 60 * 60 * 24)
            pipe.execute()


class SearchEngineView(BaseView):
    login_url = '/login/'

    def get(self, request):
        searched_games = request.session.get("searched_games", None)
        return render(request, "searchEngine/index.html", {"searched_games": searched_games})


class ResultsListView(BaseView, ListView):
    paginate_by = 12

    template_name = "searchEngine/results.html"

    def post(self, request, *args, **kwargs):
        input = request.POST.get('searchEngineInput')
        games = self.get_game(input)
        if not games:
            messages.error(
                request, "No se encontraron juegos con la búsqueda realizada. Pruebe con otro nombre")
            return redirect('searchEngine')

        list_games = list(games)
        games = sorted(list_games, key=itemgetter('name'))
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
        input_game_id = int(game_id)

        game = Game.objects.filter(id=input_game_id).values().first()

        searched_games = request.session.get("searched_games", [])

        if not any(game.get("id") == searched_game.get("id") for searched_game in searched_games):
            searched_games.append({"id": game["id"], "name": game["name"]})

        request.session["searched_games"] = searched_games

        if get_language() == "es-es":
            description = game.get("translated_description_es")
        else:
            description = game.get("description")

        game_ratings = game.get("ratings")

        ratings = sorted(game_ratings, key=itemgetter('id'), reverse=True)

        return render(request, "searchEngine/details.html", {"game": game, "description": description, "ratings": ratings})
