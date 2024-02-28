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
    



