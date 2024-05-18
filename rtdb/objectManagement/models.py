from django.db import models
from authentication.models import Users
from .storage_backends import *
# Create your models here.


class Status(models.Model):
    class Meta:
        permissions = (("can_mark_approved", "Set Approval Status"),)
    lastUpdated=models.DateTimeField(blank=True,auto_now=True)
    active=models.BooleanField(default=True)
    approved=models.BooleanField(default=False)
    banned=models.BooleanField(default=False)

class Socials(models.Model):
    sID=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='SID')
    twitter=models.URLField(max_length=255,blank=True,verbose_name="Twitter")
    youtube=models.URLField(max_length=255,blank=True,verbose_name="YouTube")
    twitch=models.URLField(max_length=255,blank=True,verbose_name="Twitch")
    website=models.URLField(max_length=255,blank=True,verbose_name="Website")
    email=models.EmailField(max_length=255,blank=True,verbose_name="Email")
    other=models.CharField(max_length=255,blank=True,verbose_name="Other")
    image=models.ImageField(upload_to="images/%Y/%m/%d/",null=True,storage=PublicMediaStorage(),max_length=255)
    
    @property
    def getLinks(self):
        return {"Twitter":self.twitter,
                "YouTube":self.youtube,
                "Twitch":self.twitch,
                "Website":self.website,
                "Other":self.other}

class Projects(models.Model):
    pID=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='PID')
    sID=models.ForeignKey(Socials,on_delete=models.CASCADE)
    projectName=models.CharField(max_length=255)
    projectDescription=models.TextField()
    projectStatus=models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)

class People(models.Model):
    hID=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='HID')
    firstname = models.CharField(max_length=255,blank=True,default='First Name')
    lastname = models.CharField(max_length=255,blank=True,default='Last Name')
    pronouns = models.CharField(max_length=255,blank=True)
    handle = models.CharField(max_length=255,blank=True)
    sID=models.ForeignKey(Socials,on_delete=models.CASCADE,null=True)
    pID=models.ManyToManyField(Projects)
    personStatus=models.ForeignKey(Status, on_delete=models.CASCADE,blank=True, null=True)