from django.urls import path
from .views import GameView, SaveScoreView, GetTopScoreView


urlpatterns = [
    path('', GameView.as_view(), name="game"),
    path('save-score/', SaveScoreView.as_view(), name='save_score'),
    path("get-scores/", GetTopScoreView.as_view(), name="get-score"),
]
