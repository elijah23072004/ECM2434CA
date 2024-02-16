from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    password = models.CharField(max_length=100)
