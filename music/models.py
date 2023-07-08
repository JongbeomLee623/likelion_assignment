from django.db import models

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.album.id}/{filename}'

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=50)


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    release_year = models.IntegerField() #년도
    description = models.TextField(max_length=200)
    tag = models.ManyToManyField(Tag, blank=True)

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path,blank=True,null=True)


class Track(models.Model):
    id = models.AutoField(primary_key=True)
    track_number = models.SmallIntegerField()
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')