from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import GameScores

from searchEngine.models import CustomUser


class GameView(LoginRequiredMixin, View):
    model = GameScores

    def get(self, request):
        scores = GameScores.objects.all().order_by('-score')[:10]
        return render(request, 'game/index.html', {"scores": scores})


class SaveScoreView(LoginRequiredMixin, View):
    model = GameScores

    def post(self, request):

        data = request.POST

        score = data.get("score")
        user = CustomUser.objects.get(id=request.user.id)

        GameScores.objects.create(score=score, user=user)

        return JsonResponse({"status": "success"})
