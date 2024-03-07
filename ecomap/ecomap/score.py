from django.contrib.auth.models import User
from .models import User as EcomapUser
import datetime

#function that is passed score and adds it to the user passed score
def handleScore(user, score):
    currentUser=EcomapUser.objects.get(username=user.username)
    #checks if a user is in the request if they are not it is erronous so return -1 
    if(currentUser is None):
        return -1
    #update the score
    score=int(score)
    userTopScore=currentUser.score

    newScore= score+userTopScore 
    currentUser.score=newScore
    EcomapUser.objects.filter(username=user.username).update(score=newScore)

    #update the streak
    last_played = currentUser.last_played
    # if the user hasn't played any games until now, set the streak to 1 and date to the current date
    if last_played == None:
        EcomapUser.objects.filter(username=user.username).update(last_played=datetime.datetime.today())
        EcomapUser.objects.filter(username=user.username).update(streak=1)
        return 1

    streak = currentUser.streak
    # todays date (when they played today)
    new_date = datetime.datetime.today().strftime('%Y-%m-%d')
    # the date the streak would have ran out (last_played + 1 day)
    streak_refresh_date = (last_played + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    if new_date == streak_refresh_date:
        #if the two dates are the same, add 1 to the streak
        EcomapUser.objects.filter(username=user.username).update(last_played=datetime.datetime.today())
        EcomapUser.objects.filter(username=user.username).update(streak=streak+1)
    else:
        #if the two dates are not the same
        EcomapUser.objects.filter(username=user.username).update(last_played=datetime.datetime.today())
        EcomapUser.objects.filter(username=user.username).update(streak=1)

    return 1
