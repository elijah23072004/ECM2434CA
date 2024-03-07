from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as djangoLogin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse


from .games import Games
from .registerForm import RegisterForm
from .login import loginAuth
from .models import User as EcomapUser
from .score import handleScore


@login_required(login_url='/login')
def homepage(request):
    return render(request, "ecomap/homepage.html")

@login_required(login_url='/login')
def leaderboard(request): 
    return render(request, "ecomap/leaderboard.html")

@csrf_protect
def login(request):
    return render(request, "ecomap/login.html")

@login_required(login_url='/login')
def wordle(request):
    games = Games()
    context = {
        'word': games.getSingleWord(7)
    }
    return render(request, "ecomap/wordle.html", context)

@login_required(login_url='/login')
def hangman(request):
    games = Games()
    context = {
        'word': games.getRandomWord()
    }
    return render(request, "ecomap/hangman.html", context)
@login_required(login_url='/login')
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
            print("user is:")
            print(form.cleaned_data["username"])
            print("password is")
            print(form.cleaned_data["password"])
            user = User.objects.create_user(form.cleaned_data["username"], password=form.cleaned_data["password"])
            user.save()
            return render(request, "ecomap/login.html")
        else:
            form = RegisterForm()

        return redirect("/register/?success=false")

#@csrf_exempt
@csrf_protect
def loginUser(request):
    if request.method == "POST":
        
        user = authenticate(username=request.POST.get('InputtedUsername'), password=request.POST.get("InputtedPassword"));
        username = request.POST.get('InputtedUsername')
        password = request.POST.get('InputtedPassword')
        if user is None:
            message="Username or password is incorrect"
            messages.error(request, message)
            return redirect('/login/')

        request.user = user
        djangoLogin(request, user)    
        request.session['username']=username

        return redirect('/', request)



def userlogout(request):
    logout(request)
    return redirect("/login",request)

def gameWheel(request):
    return render(request,"ecomap/wheel.html")


def submitScore(request):
    if(request.method=="POST"):

        alldata=request.POST
        score=alldata.get("score","0")
        result = handleScore(request.user,score)
        #if result is -1 then invalid user is passed (which should be impossible so 400 code returned
        if(result == -1):
            return HttpResponse(400)
        return HttpResponse(200);

    #returns code 400 if not POST request
    return HttpResponse(400)

def getUserScores(request):
    if(request.method=="GET"):
        my_data = EcomapUser.objects.order_by("-score").all().values('username','score')
        return JsonResponse(list(my_data), safe=False)
    #returns code 400 if not get request 
    return HttpResponse(400)

def getUserStreaks(request):
    if(request.method=="GET"):
        my_data = EcomapUser.objects.order_by("-streak").all().values('username','streak')
        return JsonResponse(list(my_data), safe=False)
    #returns code 400 if not get request
    return HttpResponse(400)

