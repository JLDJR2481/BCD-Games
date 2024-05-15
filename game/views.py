from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import GameScore
from user.models import CustomUser
from bcdGames.mixins import EmailVerifiedRequiredMixin


class GameView(EmailVerifiedRequiredMixin, View):
    model = GameScore

    def get(self, request):
        return render(request, 'game/index.html')


class SaveScoreView(EmailVerifiedRequiredMixin, View):
    model = GameScore

    def post(self, request):
        data = request.POST
        score = data.get("score")
        user = CustomUser.objects.get(id=request.user.id)
        GameScore.objects.create(score=score, user=user)
        return JsonResponse({"status": "success"})


class GetTopScoreView(EmailVerifiedRequiredMixin, View):
    def get(self, request):
        top_10_scores = GameScore.objects.all().order_by('-score')[:10]
        data = []
        for score in top_10_scores:
            user = CustomUser.objects.get(id=score.user.id)
            data.append({
                "score": score.score,
                "username": user.username,
                "profile_avatar": user.profile_avatar.url if user.profile_avatar else None
            })
        return JsonResponse({"scores": data}, safe=False)
