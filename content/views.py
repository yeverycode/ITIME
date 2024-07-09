from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Feed

class Main(APIView):
    def get(self, request):
        feeds = Feed.objects.all().order_by('-created_at')
        return render(request, "techtime/main.html", context={'feeds': feeds})

    def post(self, request):
        feeds = list(Feed.objects.all().order_by('-created_at').values())
        return JsonResponse(feeds, safe=False)

