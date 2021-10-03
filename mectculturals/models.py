
from django.db import models

# Create your models here.
class UserId(models.Model):
    userid=models.AutoField(primary_key=True)
    email=models.CharField(max_length=51,unique=True)
    password=models.CharField(max_length=256)
class UserDetails(models.Model):
    userid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=45)
    mobile=models.CharField(max_length=11,unique=True)
    reg_no=models.CharField(max_length=11)
    profilepic=models.CharField(max_length=45,null=True)
    lflag=models.IntegerField(default=0)
    password_reset=models.CharField(max_length=45,null=True)
class Events(models.Model):
    eventid=models.AutoField(primary_key=True)
    eventname=models.CharField(max_length=100)
    eventpic=models.CharField(max_length=50,null=True)
class EventUpdate(models.Model):
    eventid=models.IntegerField(default=0)
class Post(models.Model):
    userid=models.IntegerField(null=True)
    eventid=models.IntegerField(default=0)
    imgdata=models.CharField(max_length=50)
    postdata=models.CharField(max_length=1000,null=True)
    posttime=models.CharField(max_length=35,null=True)
class Registration(models.Model):
    eventid=models.IntegerField(default=0)
    userid=models.IntegerField(default=0)
