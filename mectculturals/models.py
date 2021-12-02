
from django.db import models

# Create your models here.
class UserId(models.Model):
    userid=models.AutoField(primary_key=True)
    email=models.CharField(max_length=51,unique=True)
    password=models.CharField(max_length=256)
    webtoken=models.CharField(max_length=70,null=True)
    androidtoken=models.CharField(max_length=70,null=True)
    usertype=models.IntegerField(default=4)
class UserDetails(models.Model):
    userid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=45)
    mobile=models.CharField(max_length=11,unique=True)
    reg_no=models.CharField(max_length=11)
    profilepic=models.CharField(max_length=45,null=True)
    lflag=models.IntegerField(default=0)
    altemail=models.CharField(max_length=51,unique=True,null=True)
    password_reset=models.CharField(max_length=45,null=True)
    resetpwdtoken=models.CharField(max_length=45,null=True)
class Events(models.Model):
    eventid=models.AutoField(primary_key=True)
    eventname=models.CharField(max_length=100)
    eventpic=models.CharField(max_length=50,null=True)
    description=models.CharField(max_length=500,null=True)
    participants_per_team=models.IntegerField(default=1)
    posterpic=models.CharField(max_length=50,null=True)
    eventdate=models.CharField(max_length=50,null=True)
class EventUpdate(models.Model):
    eventid=models.IntegerField(default=0)
    postedon=models.CharField(max_length=25,null=True)
    imgdata=models.CharField(max_length=100,null=True)
    eventmessage=models.CharField(max_length=1000,null=True)
    userid=models.IntegerField(default=0)
class Registration(models.Model):
    eventid=models.IntegerField(default=0)
    userid=models.IntegerField(default=0)
class EventQueries(models.Model):
    eventid=models.IntegerField(default=0)
    query=models.CharField(max_length=600)
    postedby=models.IntegerField(default=0)
    respondedby=models.IntegerField(default=0,null=True)
    response=models.CharField(max_length=1000,null=True)
