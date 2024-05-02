from django.urls import path
from .views import SearchEngineView, ResultsListView, ResultDetailView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", SearchEngineView.as_view(), name="searchEngine"),
    path("results/", ResultsListView.as_view(), name="results"),
    path("results/<str:game_id>", ResultDetailView.as_view(), name="details"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
