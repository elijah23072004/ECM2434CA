import random
from ecomap.models import Achievement, User, UserAchievement
from django.core.exceptions import ObjectDoesNotExist


class UserClass:
    # throws ObjectDoesNotExist if the username is not real
    def __init__(self, username):
        self.user = User.objects.get(username=username)
        self.achievements = self.getAchievements()

    def getAchievements(self):
        # returns a list of all achievements for this specific user
        achievements = []
        for achievement in Achievement.objects.all():
            try:
                a = UserAchievement.objects.get(username=self.user, achievement_id=achievement.achievement_id)
            except ObjectDoesNotExist:
                a = UserAchievement(username=self.user, achievement_id=achievement, value=0)
                a.save()
            achievements.append(a)
        return achievements

    def getAchievement(self, achievement_id):
        # returns an int 0-3 for what level achievement the user is and the name and description of the achievement
        achievement = Achievement.objects.get(achievement_id=achievement_id)
        name = achievement.name
        desc = achievement.description
        try:
            a = UserAchievement.objects.get(username=self.user, achievement_id=achievement.achievement_id)
        except ObjectDoesNotExist:
            a = UserAchievement(username=self.user, achievement_id=achievement, value=0)
            a.save()
        if name == "Score":
            a.value = self.user.score
        elif name == "Streak":
            self.checkHighestStreak()
        if a.value >= achievement.level_3:
            return name, desc, 3, f"{str(a.value)}/{str(achievement.level_3)}"
        elif a.value >= achievement.level_2:
            return name, desc, 2, f"{str(a.value)}/{str(achievement.level_3)}"
        elif a.value >= achievement.level_1:
            return name, desc, 1, f"{str(a.value)}/{str(achievement.level_2)}"
        return name, desc, 0, f"{str(a.value)}/{str(achievement.level_1)}"

    def checkHighestStreak(self):
        # check if the users highest streak has been updated, if so set the value accordingly
        achievement_id = Achievement.objects.get(name="Streak")
        ua = UserAchievement.objects.get(username=self.user, achievement_id=achievement_id)
        if self.user.streak > ua.value:
            ua.value = self.user.streak
            ua.save()



