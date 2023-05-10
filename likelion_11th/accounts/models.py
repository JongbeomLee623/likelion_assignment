from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="post/", blank=True, null=True) #profile picture
    nickname = models.TextField(max_length=10)
    department = models.TextField(null=True,max_length=30)