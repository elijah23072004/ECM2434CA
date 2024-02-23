from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .games import Games
from .registerForm import RegisterForm
from .login import loginAuth

def homepage(request):
    return render(request, "ecomap/homepage.html")

def leaderboard(request):
    return render(request, "ecomap/leaderboard.html")

def login(request):
    return render(request, "ecomap/login.html")

#@login_required(login_url='/login')
def hangman(request):
    games = Games()
    context = {
        'word': games.getRandomWord()
    }
    return render(request, "ecomap/hangman.html", context)

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
            #temp added to test with going to the hangman page which requires an auth
            return render(request, "ecomap/homepage.html", {"form": form})
            return redirect("/register/?success=true")
        else:
            form = RegisterForm()

        return redirect("/register/?success=false")

@csrf_exempt
def loginUser(request):
    print(request.user)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        password_check, message = loginAuth(username, password)
        # Check if a user with the provided username exists
        if not password_check:
            # Display an error message if the login details were wrong
            messages.error(request, message)
            return redirect('/login/')

        # Render the login page template (GET request)
        request.user = username
        return redirect('/homepage', request)



