from django.shortcuts import render


def home_view(request):
    return render(request, 'bot/home.html')


def bot_start_view(request):
    return render(request, 'bot/bot_info.html')
