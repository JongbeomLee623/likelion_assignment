from django.db import models

# Create your models here.
class Post(models.Model):
    MOOD = {
        ('good','좋아요'),
        ('bad','별로에요'),
        ('so-so','아무 생각이 없어요'),
    }
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()
    mood = models.CharField(max_length=5, choices=MOOD, default='so-so')
    tmi = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]

