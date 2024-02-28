from django.contrib.auth.models import User
from .models import User as EcomapUser
#function that is passed score and adds it to the user passed score
def handleScore(user, score):
    currentUser=EcomapUser.objects.get(username=user.username)
    #checks if a user is in the request if they are not it is erronous so return -1 
    if(currentUser is None):
        return -1;
    score=int(score)
    userTopScore=currentUser.score

    newScore= score+userTopScore 
    currentUser.score=newScore
    EcomapUser.objects.filter(username=user.username).update(score=newScore)


    return 1;
