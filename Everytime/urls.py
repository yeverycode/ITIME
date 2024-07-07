"""
URL configuration for Everytime project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Everytimeapp.views import SignUpView, index, category_list  # import 시 SignUpView 추가
from django.contrib import admin
from django.urls import path, include
from Everytimeapp.views import SignUpView, index, category_list

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('index/', index, name='index'),
    path('category/', category_list, name='category_list'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('users/', include('users.urls')),
    path('api/', include('Everytimeapp.urls')),
    path('', index, name='home'),
    path('categories/', category_list, name='category_list'),
    path('users/signup_api/', SignUpView.as_view(), name='signup_api'),

]