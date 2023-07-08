from rest_framework import serializers
from .models import *

class AlbumSerializer(serializers.ModelSerializer):
    
    tracks = serializers.SerializerMethodField(read_only=True)
    def get_tracks(self, instance):
        # serializer = TrackSerializer(instance.tracks,many=True)
        # return serializer.data
        titles = instance.tracks.values_list('title', flat = True)
        return list(titles)
    
    tag = serializers.SerializerMethodField()
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    images = serializers.SerializerMethodField()
    def get_images(self, instance):
        image = instance.image.all()
        return ImageSerializer(instance=image, many = True, context=self.context).data

    class Meta:
        model = Album
        # fields = "__all__"
        fields = ['id', 'artist', 'title', 'release_year', 'description', 'tracks', 'tag', 'images']


class TrackSerializer(serializers.ModelSerializer):
    album = serializers.SerializerMethodField(read_only=True)

    def get_album(self, instance):
        return instance.album.title
    
    class Meta:
        model = Track
        # fields = "__all__"
        fields = ['track_number', 'title', 'album']
        read_only_fields = ['album']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url= True, required = False)
    
    class Meta:
        model = Image
        fields = ['image']
