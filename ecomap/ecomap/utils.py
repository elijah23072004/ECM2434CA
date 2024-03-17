from .models import User as EcomapUser
from django.contrib.auth.models import User

def initialiseAdminUser(username,first_name, last_name, password):
    admin = EcomapUser.objects.create(username=username, password=password, userType="admin",first_name=first_name, last_name=last_name)
    user = User.objects.create_user(username, password=password)
    user.save()

def checkAdmin():
    users =EcomapUser.objects.all().filter(userType="admin")
    if(not users.exists()):
        initialiseAdminUser("admin","admin","","changeMe")

def getUserType(username):
    user = EcomapUser.objects.get(username=username)
    return user.userType