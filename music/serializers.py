from rest_framework import serializers
from .models import *

class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.SerializerMethodField(read_only=True)

    def get_tracks(self, instance):
        # serializer = TrackSerializer(instance.tracks,many=True)
        # return serializer.data
        titles = instance.tracks.values_list('title', flat = True)
        return list(titles)

    class Meta:
        model = Album
        # fields = "__all__"
        fields = ['id', 'artist', 'title', 'realease_year', 'description', 'tracks']

class TrackSerializer(serializers.ModelSerializer):
    album = serializers.SerializerMethodField(read_only=True)

    def get_album(self, instance):
        return instance.album.title
    
    class Meta:
        model = Track
        # fields = "__all__"
        fields = ['track_number', 'title', 'album']
        read_only_fields = ['album']
