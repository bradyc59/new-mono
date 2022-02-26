from django.contrib import admin
from django.urls import path, include
from game.views import index, game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
]
