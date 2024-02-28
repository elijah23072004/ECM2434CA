from django.contrib.auth.models import User
from .models import User as EcomapUser
def handleScore(user, score):
    currentUser=EcomapUser.objects.get(username=user.username)

    if(currentUser is None):
        return -1;
    score=int(score)
    userTopScore=currentUser.score
    if(userTopScore>score):
        return 0;
    currentUser.score=userTopScore
    #currentUser.save(update_fields=['score'])
    EcomapUser.objects.filter(username=user.username).update(score=score)


    return 1;
