from django.urls import path
from .views import *
from . import views

app_name = 'music'
urlpatterns = [
    path('', views.album_list_create),
    path('<int:album_id>/', views.album_detail_update_delete),
    path('<int:album_id>/track/', views.track_read_create),
    path('<int:album_id>/track/<int:track_id>/', views.track_detail_update_delete),
]