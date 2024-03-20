import os

from django.http import Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as djangoLogin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.utils.safestring import SafeString
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

import json

from .games import Games
from .registerForm import RegisterForm
##from .login import loginAuth
from .models import User as EcomapUser
from .models import Word, QrCode
from .score import handleScore
from .utils import checkAdmin, getUserType, getStreak, getLastPlayed, deleteEcomapUser, generateQrCode, validQrCode
from .UserClass import UserClass
from .achievements import createAchievement

############################################################################
# temp to add values to database
g = Games()
"""createAchievement("Streak", "Maintain a long running streak", 10, 25, 50)
g.addWord("Environment", "The surroundings in which living organisms exist, including the air, water, land, and their interrelations, often referred to as the natural world.")
g.addWord("Sustainability", "The ability to meet the needs of the present without compromising the ability of future generations to meet their own needs. It involves responsibly managing resources and ecosystems to ensure their long-term viability.")
g.addWord("Recycle", "The process of converting waste materials into new products or raw materials, typically to prevent the depletion of resources and reduce the environmental impact of waste disposal.")
g.addWord("Sustainable", "Capable of being maintained or continued over the long term without causing significant environmental, economic, or social harm. It implies practices that balance the needs of the present with the needs of future generations.")
g.addWord("Reuse", "The practice of using items or materials again, either for their original purpose or for a different purpose, in order to minimize waste and resource consumption.")
g.addWord("Conservation", "The careful management and protection of natural resources, habitats, and ecosystems to prevent their depletion, degradation, or destruction.")
g.addWord("Reduce", "To decrease the amount of waste generated or resources consumed by minimizing unnecessary consumption and adopting more efficient practices.")
g.addWord("Renewable", "Resources that are naturally replenished over time, such as sunlight, wind, water, and biomass, and can be used indefinitely without depleting finite reserves.")
g.addWord("Energy", "The capacity to do work, typically derived from various sources such as fossil fuels, renewable resources, or nuclear reactions, and used to power machines, provide heat, or generate electricity.")
g.addWord("Carbon", "A chemical element that is essential to life and exists in various forms, including carbon dioxide (CO2) and carbon compounds. It plays a significant role in the Earth's carbon cycle and climate system.")
g.addWord("Carbon Footprint", "The total amount of greenhouse gases, especially carbon dioxide, emitted directly or indirectly by human activities, typically expressed in equivalent tons of CO2.")
g.addWord("Green", "Related to practices, products, or lifestyles that are environmentally friendly, sustainable, or promote conservation and reduce negative impacts on the environment.")
g.addWord("Biodegradable", "Capable of being decomposed by biological processes, typically bacteria or other microorganisms, into harmless substances such as water, carbon dioxide, and organic matter.")
g.addWord("Recycling", "The process of collecting, sorting, processing, and converting waste materials into new products or raw materials to be used again, thus conserving resources and reducing environmental pollution.")
g.addWord("Habitat Conservation", "The protection/preservation of natural habitats to maintain biodiversity and ecosystem health." )
g.addWord("Renewable Energy", "Energy from natural resources such as sunlight, wind, and water." )
g.addWord("Global Warming", "The gradual increase in Earth's temperature, primarily caused by greenhouse gases releasing into the atmosphere." )
g.addWord("Erosion", "The wearing away of land or soil by natural forces such as wind, water, and ice, often exacerbated by activities like deforestation and overgrazing." )
"""

############################################################################

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
    word = games.getSingleWord(7)
    definition = games.getDefinition(word)
    if word:
        context = {
            'word': word,
            'definition': definition
        }
        context = json.dumps(context)
        return render(request, "ecomap/wordle.html", {'data': SafeString(context)})

@login_required(login_url='/login')
def hangman(request):

    games = Games()
    word = games.getRandomWord()
    definition = games.getDefinition(word)
    if word:
        context = {
            'word': word,
            'definition': definition
        }
        context = json.dumps(context)
        return render(request, "ecomap/hangman.html", {'data': SafeString(context)})

@login_required(login_url='/profile')
def profile(request):
    requested_user = request.GET.get('user', '')
    self_view = True
    if requested_user:
        try:
            user = UserClass(requested_user)
            if requested_user != request.user.username:
                self_view = False
        except:
            user = UserClass(request.user)
    else:
        user = UserClass(request.user)
    print(getLastPlayed(request.user))
    data = {
        'username': user.user.username,
        'score': user.user.score,
        'streak': getStreak(user.user.username),
        'last_played': getLastPlayed(user.user.username),
    }
    if self_view:
        data['first_name'] = user.user.first_name
        data['last_name'] = user.user.last_name
        data['user_type'] = getUserType(user.user.username)

    data = json.dumps(data)
    return render(request, "ecomap/profile.html", {'data': SafeString(data)})

@login_required(login_url='/achievements')
def achievements(request):
    achievements = {}
    user = UserClass(request.user)
    for ach in user.achievements:
        name, desc, level, progress = user.getAchievement(ach.achievement_id.achievement_id)
        achievements[name] = [progress, level]
        print(achievements)
    achievements = json.dumps(achievements)
    return render(request, "ecomap/achievements.html", {'data': SafeString(achievements)})

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
        query = QueryDict('', mutable=True)
        data = {
            'username': request.POST['username'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'password': make_password(request.POST['password']),
        }
        query.update(data)
        form = RegisterForm(query)
        if form.is_valid():
            form.save()
            print("user is:")
            print(form.cleaned_data["username"])
            print("password is")
            print(make_password(form.cleaned_data["password"]))
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
        username = request.POST.get('InputtedUsername')
        password = request.POST.get('InputtedPassword')

        # get user object by username else return to login pagae
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return redirect('/login/')
        if not user:
            return redirect('/login/')

        # check password, if incorrect, stay on the same page and display a message
        if not validateUser(username, password):
            message="Username or password is incorrect"
            messages.error(request, message)
            return redirect('/login/')

        request.user = user
        djangoLogin(request, user)
        request.session['username'] = username

        return redirect('/', request)



def userlogout(request):
    logout(request)
    return redirect("/login",request)

def gameWheel(request):
    return render(request,"ecomap/wheel.html")

# matching redirectory request
login_required(login_url='/login')
def matching(request):
    games = Games()
    words = []
    while len(words) < 3:
        word = games.getRandomWord()
        if word:
            definition = games.getDefinition(word)
            if definition:
                dict = {'term': word, 'definition': definition}
                if dict not in words:
                    words.append(dict)

    words = json.dumps(words)
    return render(request, "ecomap/matching.html", {'data': SafeString(words)})

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

def deleteSelfAccount(request):
    # checks password sent from delete account button, returns true if it is correct
    if(request.method=="POST"):
        data = request.POST
        password = data.get("password","")

        if validateUser(request.user, password):
            deleteEcomapUser(request.user)
            return HttpResponse(200)
    return HttpResponse(400)

def validateUser(username, password):
    # validates a user, returns true if correct and false if incorrect
    ecomapuser = EcomapUser.objects.get(username=username)
    if check_password(password, ecomapuser.password):
        return True
    return False

def getUserScores(request):
    if(request.method=="GET"):
        my_data = EcomapUser.objects.order_by("-score").all().values('username','score')
        return JsonResponse(list(my_data), safe=False)
    #returns code 400 if not get request
    return HttpResponse(400)

def getUserStreaks(request):
    if(request.method=="GET"):
        for user in list(EcomapUser.objects.all()):
            getStreak(user.username)
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
        query = QueryDict('', mutable=True)
        data = {
            'username': request.POST['username'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'password': make_password(request.POST['password']),
        }
        #creates a user with the fields passed in the request object
        query.update(data)
        form = RegisterForm(query)
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


            ecomapUser.password=make_password(request.POST["password"])

            user=User.objects.get(username=request.POST["username"])

            user.set_password(make_password(request.POST["password"]))

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
       
        words = Word.objects.all().values("term","definition")
        return JsonResponse(list(words), safe=False)
 
       
    return HttpResponse(400)

@login_required(login_url='/login')
def addWord(request):
    userType = getUserType(request.user)
    if request.method=="POST":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")
        wordToAdd = request.POST["word"]
        definition=request.POST["definition"]

        words = Word.objects.all()
        if Word.objects.filter(term = wordToAdd).exists():
            return HttpResponse(200)

       


        for word in words:
            #checks if word is already in file (so dont add word 2 times)
            if(word.term==wordToAdd):
                return HttpResponse(400)
        Word.objects.create(term=wordToAdd, definition=definition)

        return HttpResponse(200)
@login_required(login_url='/login')
def removeWord(request):
    userType = getUserType(request.user)
    if request.method=="POST":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")


        wordToRemove = request.POST["word"]

        words = Word.objects.filter(term=wordToRemove).first()
        print(words)
        if(words is None):

            return HttpResponse(200)


        print(words.term)
        words.delete()


        return HttpResponse(400)

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

        deleteEcomapUser(request.POST["username"])
        return HttpResponse(200)
    return HttpResponse(400)

@login_required(login_url='/login')  
def getQrCodes(request):
    userType = getUserType(request.user)
    if request.method=="GET":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")
        #reads ecowords file and splits into an array where each line is its own element
        
        codes = QrCode.objects.all().values("code")
        print(codes)
        return JsonResponse(list(codes), safe=False)
       
    return HttpResponse(400)

@login_required(login_url='/login')  
def addQrCode(request):
    userType = getUserType(request.user)
    if request.method=="POST":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")
        qrCode = request.POST["qrCode"]        
        if(not validQrCode(qrCode)):
            return HttpResponse(400)
        if QrCode.objects.filter(code = qrCode).exists():
            return HttpResponse(400)
        QrCode.objects.create(code = qrCode)
        return HttpResponse(200)
    

@login_required(login_url='/login')  
def removeQrCode(request):
    userType = getUserType(request.user)
    if request.method=="POST":
        qrCode = request.POST["qrCode"]    
        code = QrCode.objects.filter(code=qrCode).first()
        print(code)
        if(code is None):
            return HttpResponse(200)
        
        
        print(code.code)
        code.delete()
        
        return HttpResponse(400)
    
@login_required(login_url='/login')  
def checkQrCode(request):
    if request.method=="POST":
        qrCode = request.POST["qrCode"]    
        
        if QrCode.objects.filter(code = qrCode).exists():
            return JsonResponse({"ValidCode":True}, safe=False)
        return JsonResponse({"ValidCode":False}, safe=False)

@login_required(login_url='/login')     
def editQrCode(request):
    userType = getUserType(request.user)
    if not(userType == "admin" or userType=="gameMaker"):
        redirect("/")
    if(request.method=="GET"):
        return render(request,"ecomap/editQrCode.html")

@login_required(login_url='/login')  
def getQrCodeImage(request):
    userType = getUserType(request.user)
    if request.method=="POST":
        if not(userType == "admin" or userType=="gameMaker"):
            redirect("/")


        jsonText = request.POST["json"]

        data= data = json.loads(request.POST["json"])
        qrCode = data["qrCode"]

        #generates qr code with code passed 
   
        qrCodeImage = generateQrCode(qrCode)
        response = HttpResponse(content_type="image/png")
        image_data = qrCodeImage.getvalue()
        return HttpResponse(image_data, content_type="image/png")

def checkValidQrCode(request):
    if request.method=="POST":
        qrCode = request.POST["qrCode"]
        #checks if qr code exists and if it does returns http response code 200 and if it doesn't exist returns http response code 400
        if QrCode.objects.filter(code = qrCode).exists():
            return HttpResponse(200)
        return HttpResponse(400)