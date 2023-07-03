from django.contrib import admin
from .models import Post,Comment,Tag
from music.models import Album,Track
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Album)
admin.site.register(Track)