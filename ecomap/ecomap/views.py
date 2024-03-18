import os

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
from django.contrib.auth import update_session_auth_hash
from django.conf import settings


from .games import Games
from .registerForm import RegisterForm
from .login import loginAuth
from .models import User as EcomapUser
from .score import handleScore
from .utils import checkAdmin,getUserType

@login_required(login_url='/login')
def homepage(request):
    userType = getUserType(request.user)
    if(userType == "user" ):
        return render(request, "ecomap/homepage.html")
    elif (userType == "admin"):
        return render(request, "ecomap/admin.html")
    elif (userType =="gameMaker"):
        return render(request,"ecomap/gameMaker.html")
    
@login_required(login_url='/login')
def userHomePage(request):
    return render(request, "ecomap/homepage.html")


@login_required(login_url='/login')
def leaderboard(request): 
    return render(request, "ecomap/leaderboard.html")

@csrf_protect
def login(request):
    checkAdmin()#creates an admin user if no admin users exist
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
    
@login_required(login_url='/login')
def map(request):
    return render(request, "ecomap/map.html")
    
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
            print(form.cleaned_data["userType"])
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

# matching redirectory request
def matching(request):
    return render(request,"ecomap/matching.html")

def submitScore(request):
    if(request.method=="POST"):

        alldata=request.POST
        score=alldata.get("score","0")
        result = handleScore(request.user,score)
        #if result is -1 then invalid user is passed (which should be impossible so 400 code returned
        if(result == -1):
            return HttpResponse(400)
        return HttpResponse(200)

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

@login_required(login_url='/login')
def editUsers(request):
    #checks if user has permission (aka being admin or game maker) to view page
    userType = getUserType(request.user)    
    if(userType == "user" ):
        return redirect("/homepage",request)
    return render(request,"ecomap/editUsers.html")

@login_required(login_url='/login')
def getUserData(request):
    
    if(request.method=="GET" and getUserType(request.user) == "admin"):
            
        my_data = EcomapUser.objects.all().values("username", "first_name","last_name","userType")
        return JsonResponse(list(my_data), safe=False)
    return HttpResponse(400)

@login_required(login_url='/login')
def adminMakeUser(request):

    if (request.method == "POST" and getUserType(request.user) == "admin"):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.create_user(form.cleaned_data["username"], password=form.cleaned_data["password"])
            user.save()
            return redirect("/editUsers/")
        else:
            form = RegisterForm()

        return HttpResponse(400)

@login_required(login_url='/login')
def adminEditUser(request):

    if (request.method == "POST" and getUserType(request.user) == "admin"):

        ecomapUser = EcomapUser.objects.get(username=request.POST["username"])
        #if password in request is empty then admin does not want to change password
        if(request.POST["password"]!=""):
            

            ecomapUser.password=request.POST["password"]

            user=User.objects.get(username=request.POST["username"])

            user.set_password(request.POST["password"])

            user.save()
            
            if(request.user.username == request.POST["username"]):
                #stills logs out user if they change own password
                update_session_auth_hash(request, request.user)

            
            
        ecomapUser.first_name=request.POST["first_name"]
        ecomapUser.last_name=request.POST["last_name"]
        ecomapUser.userType=request.POST["userType"]
        ecomapUser.save()

        
        return render(request,"ecomap/editUsers.html")

    return HttpResponse(400)

@login_required(login_url='/login')
def gameMakerPage(request):
    userType = getUserType(request.user)
    if not(userType == "admin" or userType=="gameMaker"):
        redirect("/")
    if(request.method=="GET"):
        return render(request,"ecomap/gameMaker.html")

@login_required(login_url='/login')
def getWords(request):
    userType = getUserType(request.user)
    if request.method=="GET":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")
        #reads ecowords file and splits into an array where each line is its own element
        f = open(os.path.join(settings.BASE_DIR,"./ecomap/eco_words.txt"), "r")
        data =f.read()
        f.close()
        my_data = data.split("\n")
        return JsonResponse(list(my_data), safe=False)
       
    return HttpResponse(400)

@login_required(login_url='/login')
def addWord(request):
    userType = getUserType(request.user)
    if request.method=="POST":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")
        wordToAdd = request.POST["word"]

        f = open(os.path.join(settings.BASE_DIR,"./ecomap/eco_words.txt"), "r")
        #reads file ecowords
        text = f.read()
        my_data = text.split("\n")
        f.close()
        print(my_data)
        for line in my_data:
            #checks if word is already in file (so dont add word 2 times)
            if(line==wordToAdd):
                return HttpResponse(400)
        f = open(os.path.join(settings.BASE_DIR,"./ecomap/eco_words.txt"), "a")
        f.write("\n"+wordToAdd)
        f.close()
        return HttpResponse(200)
@login_required(login_url='/login')
def removeWord(request):
    userType = getUserType(request.user)
    if request.method=="POST":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")

        
        wordToRemove = request.POST["word"]
        f = open(os.path.join(settings.BASE_DIR,"./ecomap/eco_words.txt"), "r")
        data = f.read()
        data = data.split("\n")
        f.close()
        f = open(os.path.join(settings.BASE_DIR,"./ecomap/eco_words.txt"), "w")
        
        
        code = 400
        text = ""
        for line in data:
            #adds each line to text unless that line is the word to be removed 
            if(line==wordToRemove):
                code = 200
                continue
            text += line+"\n"
        text=text[:-1]
        f.write(text)
        f.close()
        return HttpResponse(code)

@login_required(login_url='/login')  
def deleteUser(request):
    userType = getUserType(request.user)
    print(request.POST)
    if request.method=="POST":
        if not(userType == "admin"):
            redirect("/")

        print(request.POST["username"])
        if (request.user.username == request.POST["username"]):
            logout=True
        
        EcomapUser.objects.filter(username=request.POST["username"]).delete()
        User.objects.filter(username=request.POST["username"]).delete()
        return HttpResponse(200)
    return HttpResponse(400)