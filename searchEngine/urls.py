from django.urls import path
from .views import SearchEngineView, ResultsListView, ResultDetailView

urlpatterns = [
    path("", SearchEngineView.as_view(), name="searchEngine"),
    path("results/", ResultsListView.as_view(), name="results"),
    path("results/<str:game_id>", ResultDetailView.as_view(), name="details"),
]
