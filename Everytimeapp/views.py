from django.shortcuts import render
from django.http import HttpResponse  # HttpResponse 임포트
from .models import Category

def index(request):
    return HttpResponse("Hello, world. You're at the Everytimeapp index.")

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
