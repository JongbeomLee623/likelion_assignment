from django.db import models

# Create your models here.

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    realease_year = models.IntegerField() #년도
    description = models.TextField(max_length=200)

class Track(models.Model):
    id = models.AutoField(primary_key=True)
    track_number = models.SmallIntegerField()
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')