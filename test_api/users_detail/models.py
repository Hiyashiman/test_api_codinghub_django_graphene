from django.db import models
from django.contrib.auth.models import User 

class UsersDetail(models.Model):
    cardId = models.CharField(max_length=13)
    address = models.TextField()
    phoneNumber = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  


