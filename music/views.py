from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from django.conf import settings
import os

from django.shortcuts import get_object_or_404
# Create your views here.
@api_view(['GET','POST'])
def album_read_create(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = AlbumSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            content = request.data['description']
            words = content.split(' ')
            tag_list = []
            album = get_object_or_404(Album, id = serializer.data['id'])
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name = t)
                except:
                    tag = Tag(name = t)
                    tag.save()
                album.tag.add(tag)
            
            images_data = request.FILES.getlist('images')
            for image_data in images_data:
                Image.objects.create(album=album, image=image_data)

            album.save()
        return Response(data = AlbumSerializer(album).data)
        
@api_view(['GET','PATCH','DELETE'])
def album_detail_update_delete(request,album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'GET':
        serializer = AlbumSerializer(album)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = AlbumSerializer(instance=album, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            album = get_object_or_404(Album, id = serializer.data['id'])
            album.tag.clear()
            content = request.data['description']
            words = content.split(' ')
            tag_list = []
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)   
                    tag.save()
                album.tag.add(tag)
            
            for image in album.image.all():
                file_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
                if os.path.exists(file_path):
                    os.remove(file_path)
            album.image.all().delete()  

            images_data = request.FILES.getlist('images')
            for image_data in images_data:
                Image.objects.create(album=album, image=image_data)    
            album.save()            
        return Response(AlbumSerializer(album).data)
        
    elif request.method == 'DELETE':

        for image in album.image.all():
            file_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
            if os.path.exists(file_path):
                os.remove(file_path)
        album.image.all().delete()
        album.delete()
        data = {
            'deleted_album':album_id,
        }
        return Response(data)
    
@api_view(['GET','POST'])
def track_read_create(request, album_id):
    if request.method == 'GET':
        tracks = Track.objects.filter(album=album_id)
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        album = get_object_or_404(Album,pk=album_id)
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(album=album)
        return Response(serializer.data)

@api_view(['GET','PATCH','DELETE'])
def track_detail_update_delete(request, track_id):
    track = get_object_or_404(Track, id=track_id)

    if request.method == 'GET':
        serializer = TrackSerializer(track)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = TrackSerializer(track,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        track.delete()
        data = {
            'deleted_track':track_id,
        }
        return Response(data)

@api_view(['GET','POST'])
def find_tag(request, tag_name = None):
    if request.method == 'GET':
        f_tag = get_object_or_404(Tag, name = tag_name)
        album = Album.objects.filter(tag__in = [f_tag])
        serializer = AlbumSerializer(album, many = True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        tag_name = request.data['tag']
        f_tag = get_object_or_404(Tag, name = tag_name)
        album = Album.objects.filter(tag__in = [f_tag])
        serializer = AlbumSerializer(album, many = True)
        return Response(data=serializer.data)