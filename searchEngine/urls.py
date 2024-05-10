from django.urls import path
from .views import SearchEngineView, ResultsListView, ResultDetailView, gameSearch, GamePostsListView


urlpatterns = [
    path("", SearchEngineView.as_view(), name="searchEngine"),
    path("results/", ResultsListView.as_view(), name="results"),
    path("results/<str:game_id>", ResultDetailView.as_view(), name="details"),
    path("game-search/", gameSearch, name="game-search"),
    path("game-posts/<int:game_id>", GamePostsListView.as_view(), name="game-posts")
]
