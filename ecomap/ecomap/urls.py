from django.urls import path

from . import views

app_name = "ecomap"

# Define the URL patterns for the ecomap app
urlpatterns = [
    path("", views.homepage, name="homepage"),  # Homepage URL
    path("leaderboard/", views.leaderboard, name="leaderboard"),  # Leaderboard URL
    path("login/", views.login, name="login"),  # Login URL
    path("map/", views.map, name="map"),  # Map URL
    path("hangman/", views.hangman, name="hangman"),  # Hangman URL
    path("wordle/", views.wordle, name="wordle"),  # Wordle URL
    path("qrcode/", views.qrcode, name="qrcode"),  # QR Code URL
    path("register/", views.register, name="register"),  # Register URL
    path("registerUser/", views.registerUser, name="createUser"),  # Create User URL
    path("loginUser/", views.loginUser, name="loginUser"),  # Login User URL
    path("logout/", views.userlogout, name="logout"),  # Logout URL
    path("matching/", views.matching, name="matching"), # matching game URL
    path("wheel/", views.gameWheel, name="wheel"),  # Game Wheel URL
    path("sendScore/", views.submitScore, name="submitScore"), #Submit Score URL
    path("getScores/", views.getUserScores,name="getScores"), #Get Score URL
    path("getStreaks/", views.getUserStreaks,name="getStreaks"), #Get Streak URL
    path("userhomePage/", views.userHomePage,name="userHomepage"),#go to regular user homepage (for admin to access regular site)
    path("editUsers/", views.editUsers, name="editUsers"), #edit user url
    path("getUsers/", views.getUserData, name="getUsers"), #get user data
    path("adminMakeUser/", views.adminMakeUser, name="adminMakeUser"), #admin make user
    path("adminEditUser/",views.adminEditUser, name="adminEditUser"), #admin edit existing user 
    path("gameMaker/", views.gameMakerPage, name="gameMaker"), #game maker page to edit games
    path("getWords/", views.getWords, name="gameMaker"), #get words for games 
    path("addWord/", views.addWord, name="addWord"), # add word to ecowords file
    path("removeWord/", views.removeWord, name="addWord"),# remove word from ecowords file
    path("deleteUser/" ,views.deleteUser, name="deleteUser"), #delete User
    path("achievements/", views.achievements,name="achievements"), # Achievements URL
]
