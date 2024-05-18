from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
    username = models.EmailField(max_length=255,blank=True,verbose_name="Email",unique=True)
    uID=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='UID')
    handle = models.CharField(max_length=255,blank=True)
    #pass