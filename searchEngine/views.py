from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.translation import get_language
from django.contrib import messages
from .models import Game
from gamesPosts.models import Post
from django.http import JsonResponse
from operator import itemgetter
from django.core.paginator import Paginator
from redis import Redis
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())
env = dotenv.dotenv_values()

redis = Redis(
    host=env['REDIS_HOST'],
    port=13121,
    username=env['REDIS_USER'],
    password=env['REDIS_PASSWORD'],
)


def gameSearch(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        consulta = request.GET.get("term")
        games = Game.objects.filter(
            name__startswith=consulta).order_by("-search_count").values_list('name', "search_count")
        resultados = [{'name': game[0], 'search_count': game[1]}
                      for game in games]

        if resultados and resultados[0]['search_count'] > 0:
            resultados[0]['name'] = f"{resultados[0]['name']} (Más buscado)"

        game_names = [resultado["name"] for resultado in resultados]

        return JsonResponse(game_names, safe=False)
    return JsonResponse({}, safe=False)


class BaseView(View):
    def get_game(self, input):
        games = self.redis_search(input)

        if games:
            if input == "":
                self.store_cache_redis(games)
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
        if input == "":
            games = Game.objects.all().values('id', 'name')
            return [{'id': game['id'], 'name': game['name']} for game in games]
        else:
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
    def get(self, request):
        searched_games = request.session.get("searched_games", None)
        return render(request, "searchEngine/index.html", {"searched_games": searched_games})


class ResultsListView(BaseView, ListView):
    paginate_by = 12
    template_name = "searchEngine/results.html"

    def post(self, request, *args, **kwargs):
        input = request.POST.get('searchEngineInput')
        input = input.replace("(Más buscado)", "").strip()
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
        counter_game = Game.objects.get(id=input_game_id)
        counter_game.search_count += 1
        counter_game.save()
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
        posts = Post.objects.filter(game=game["id"]).values().count()

        return render(request, "searchEngine/details.html", {"game": game, "description": description, "posts": posts})


class GamePostsListView(BaseView, ListView):
    paginate_by = 12
    template_name = "searchEngine/game_posts.html"

    def get(self, request, game_id):
        posts_list = Post.objects.filter(game=game_id)
        paginator = Paginator(posts_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "searchEngine/game_posts.html", {"page_obj": page_obj})
