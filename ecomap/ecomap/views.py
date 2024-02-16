from django.http import Http404
from django.shortcuts import get_object_or_404, render


def homepage(request):
    return render(request, "ecomap/homepage.html")

def leaderboard(request):
    return render(request, "ecomap/leaderboard.html")

def login(request):
    return render(request, "ecomap/login.html")

def hangman(request):
    return render(request, "ecomap/hangman.html")

def qrcode(request):
    return render(request, "ecomap/qrcodereader.html")

def register(request):
    return render(request, "ecomap/register.html")
