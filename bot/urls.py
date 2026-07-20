from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('bot/start/', views.bot_start_view, name='bot_start'),
]
