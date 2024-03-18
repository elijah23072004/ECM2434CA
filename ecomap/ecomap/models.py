from django.db import models

class User(models.Model):
    # Define the fields for the User model
    username = models.CharField(max_length=100, unique=True)  # User's username
    first_name = models.CharField(max_length=100)  # User's first name
    last_name = models.CharField(max_length=100)  # User's last name
    password = models.CharField(max_length=100)  # User's password
    userType = models.CharField(max_length=25, default="user")  # User's type (default is "user")
    score = models.IntegerField(default=0)  # User's score (default is 0)
    streak = models.IntegerField(default=0)  # User's streak (default is 0)
    last_played = models.DateField(default=None, null=True)    # Last time the user played any game

class Word(models.Model):
    # Define the words used for the minigames
    word_id = models.AutoField(primary_key=True)            # auto increment id
    term = models.CharField(max_length=40)                  # the actual word to be used
    definition = models.CharField(max_length=100)           # the definition of the word

class Achievement(models.Model):
    # Achievements that can be collected with 3 levels (bronze, silver and gold)
    achievement_id = models.AutoField(primary_key=True)     # auto increment id
    name = models.CharField(max_length=40)                  # the achievement name
    description = models.CharField(max_length=100)          # the description of the achievement
    level_1 = models.IntegerField()                         # the bronze level threshold (e.g. streak of 10)
    level_2 = models.IntegerField()                         # the silver level threshold (e.g. streak of 25)
    level_3 = models.IntegerField()                         # the gold level threshold (e.g. streak of 50)

class UserAchievement(models.Model):
    # Links the user's to their achievements
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")                      # the user's id
    achievement_id = models.ForeignKey(Achievement, on_delete=models.CASCADE, to_field="achievement_id")         # the achievement id
    value = models.IntegerField()                           # the value the user has for this achievement (will determine their level)
