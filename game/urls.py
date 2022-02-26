from django.contrib import admin
from .views import game
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="index"),  # /app
    path('', views.LoginView.as_view(), name="index"),
    path('play/<room_code>', game),
    path('profile/<profile_user>', login_required(views.ProfileView.as_view()), name="profile"),
    path('register/', views.CaUserSignupView.as_view(), name='confirm'),
    path('lobby/', views.lobby),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
