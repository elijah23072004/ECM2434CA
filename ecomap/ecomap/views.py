from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from .registerForm import RegisterForm
from django.shortcuts import redirect

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
    if request.method == "GET": 
        return render(request, "ecomap/register.html")
    
@csrf_exempt
def registerUser(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/register/?success=true")
        else:
            form = RegisterForm()

        return redirect("/register/?success=false")
    


