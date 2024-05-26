from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import GameScore
from bcdGames.mixins import EmailVerifiedRequiredMixin


class GameView(EmailVerifiedRequiredMixin, View):
    model = GameScore

    def get(self, request):
        return render(request, 'game/index.html')


class SaveScoreView(EmailVerifiedRequiredMixin, View):
    model = GameScore

    def post(self, request):
        score = request.POST.get("score")
        GameScore.objects.create(user=request.user, score=score)
        return JsonResponse({"status": "success"})


class GetTopScoreView(EmailVerifiedRequiredMixin, View):
    def get(self, request):
        top_10_scores = GameScore.objects.all().order_by('-score')[:10]
        data = [
            {
                "score": score.score,
                "username": score.user.username,
                "profile_avatar": score.user.userimage.image if score.user.userimage else None
            }
            for score in top_10_scores
        ]
        return JsonResponse({"scores": data}, safe=False)
