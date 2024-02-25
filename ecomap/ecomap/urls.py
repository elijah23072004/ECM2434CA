from django.urls import path

from . import views

app_name = "ecomap"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("login/", views.login, name="login"),
    path("hangman/", views.hangman, name="hangman"),
    path("wordle/", views.wordle, name="wordle"),
    path("qrcode/", views.qrcode, name="qrcode"),
    path("register/",views.register, name="register"),
    path("registerUser/",views.registerUser, name="createUser"),
    path("loginUser/",views.loginUser, name="loginUser"),
    path("logout/",views.userlogout,name="logout"),
    path("wheel/", views.gameWheel, name="wheel"),
]
