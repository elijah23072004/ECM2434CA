import random
from ecomap.models import Achievement, User, UserAchievement
from django.core.exceptions import ObjectDoesNotExist

def createAchievement(name, description, level1, level2, level3):
    removeAchievement(name)
    achievement = Achievement(name=name.title(), description=description, level_1=level1, level_2=level2, level_3=level3)
    achievement.save()

def removeAchievement(name):
    try:
        achievement = Achievement.objects.get(name=name.title())
    except ObjectDoesNotExist:
        return
    achievement.delete()

