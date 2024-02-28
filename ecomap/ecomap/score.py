from django.contrib.auth.models import User
from .models import User as EcomapUser

#function that returns -1 if invalid user, 0 if user's high score is higher than score passed and 1 if user's score is lower
#and saves score to user if it is higher then current score
def handleScore(user, score):
    currentUser=EcomapUser.objects.get(username=user.username)
    #checks if a user is in the request if they are not it is erronous so return -1 
    if(currentUser is None):
        return -1;
    score=int(score)
    userTopScore=currentUser.score

    #if userhighscore is higher then scored passed then dont save new score 
    if(userTopScore>score):
        return 0;
    
    #if highscore is lower then save new score as high score
    currentUser.score=userTopScore
    EcomapUser.objects.filter(username=user.username).update(score=score)


    return 1;
