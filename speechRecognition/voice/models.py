from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass

class Chats(models.Model):
    text=models.TextField()
    date=models.DateField(auto_now_add=True)
    spokeBy=models.CharField(max_length=100,blank=True)
    currentUser=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
