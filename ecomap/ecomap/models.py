from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    userType = models.CharField(max_length=25,default="user")
