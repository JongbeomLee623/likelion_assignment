from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('',mainpage, name="mainpage"),
    path('intro/',secondpage, name="secondpage"),
    path('new/',new, name="new"),
    path('create/',create, name="create"),
    path('<int:id>',detail, name="detail"),
    path('edit<int:id>', edit, name="edit"),
    path('update<int:id>', update, name="update"),
    path('delete<int:id>', delete, name="delete"),
    path('tag/', tag_list, name="tag_list"),
    path('tag/<int:tag_id>', tag_posts, name="tag_posts"),
    path('deleteComment<int:comment_id>',deleteComment,name="deleteComment"),
    path('likes/<int:post_id>',likes,name="likes"),
]