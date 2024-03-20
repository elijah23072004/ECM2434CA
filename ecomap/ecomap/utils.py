from .models import User as EcomapUser, UserAchievement
from django.contrib.auth.models import User
import datetime
from .UserClass import UserClass
import qrcode
#from PIL import Image
#import base64
#from io import BytesIO
import io

def initialiseAdminUser(username,first_name, last_name, password):
    admin = EcomapUser.objects.create(username=username, password=password, userType="admin",first_name=first_name, last_name=last_name)
    user = User.objects.create_user(username, password=password)
    user.save()

def checkAdmin():
    #if no admin users exist create admin user with username admin and password changeMe
    users =EcomapUser.objects.all().filter(userType="admin")
    if(not users.exists()):
        initialiseAdminUser("admin","admin","NotUser","changeMe")

def getUserType(username):
    user = EcomapUser.objects.get(username=username)
    return user.userType

def getStreak(username):
    currentUser=EcomapUser.objects.get(username=username)
    #checks if a user is in the request if they are not it is erronous so return -1
    if(currentUser is None):
        return -1

    last_played = currentUser.last_played
    # if the user hasn't played any games, set the streak to 0 and date to the current date
    if last_played == None:
        EcomapUser.objects.filter(username=username).update(last_played=datetime.datetime.today())
        EcomapUser.objects.filter(username=username).update(streak=0)
        return 0

    streak = currentUser.streak
    # todays date (when they played today)
    new_date = datetime.datetime.today().strftime('%Y-%m-%d')
    # the date the streak would have ran out (last_played + 1 day)
    streak_refresh_date = (last_played + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    if new_date <= streak_refresh_date:
        return streak
    else:
        #if the streak has expired
        EcomapUser.objects.filter(username=username).update(streak=0)
        return 0

def getLastPlayed(username):
    currentUser=EcomapUser.objects.get(username=username)
    print(currentUser.score)
    #checks if a user is in the request if they are not it is erronous so return -1
    if(currentUser is None):
        return
    if currentUser.score == 0:
        return "N/A"

    last_played = currentUser.last_played
    # if the user hasn't played any games, set the streak to 0 and date to the current date
    if last_played == None:
        return

    return last_played.strftime('%d/%m/%Y')

def deleteEcomapUser(username):
    # delete django user object
    User.objects.filter(username=username).delete()

    user = UserClass(username)
    achievements = user.getAchievements()
    for achievement in achievements:
        achievement.delete()

    user.user.delete()


def generateQrCode(code):
    qr_img = qrcode.make(code)
    output = io.BytesIO()
    #qr_img.save(output, format='PNG')
    qr_img.save(output)
    #output.seek(0)
    #output_s = output.read()
    #b64 = base64.b64encode(output_s)
    return output

def validQrCode(code):
    if(len(code)>10 or len(code)<5):
        return False
    if(not code.isalnum()):
        return False
    return True