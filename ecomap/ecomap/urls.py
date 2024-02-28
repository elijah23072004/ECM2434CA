from django.urls import path

from . import views

app_name = "ecomap"
urlpatterns = [
    path("", views.homepage, name="homepage"),  # Homepage URL
    path("leaderboard/", views.leaderboard, name="leaderboard"),  # Leaderboard URL
    path("login/", views.login, name="login"),  # Login URL
    path("hangman/", views.hangman, name="hangman"),  # Hangman URL
    path("wordle/", views.wordle, name="wordle"),  # Wordle URL
    path("qrcode/", views.qrcode, name="qrcode"),  # QR Code URL
    path("register/", views.register, name="register"),  # Register URL
    path("registerUser/", views.registerUser, name="createUser"),  # Create User URL
    path("loginUser/", views.loginUser, name="loginUser"),  # Login User URL
    path("logout/", views.userlogout, name="logout"),  # Logout URL
    path("wheel/", views.gameWheel, name="wheel"),  # Game Wheel URL
    path("sendScore/", views.submitScore, name="submitScore"), #Submit Score URL
    path("getScores/", views.getUserScores,name="getScores"), #Get Score URL
]
