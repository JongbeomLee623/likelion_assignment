from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    is_author = request.user.is_authenticated and post.writer == request.user.profile.nickname
    return render(request, "main/detail.html", {"post": post, 'is_author':is_author})



def mainpage(request):
    posts = Post.objects.all()
    return render(request, "main/mainpage.html", {"posts": posts})


def secondpage(request):
    return render(request, "main/secondpage.html")


def new(request):
    return render(request, "main/new.html")


def create(request):
    new_post = Post()
    new_post.title = request.POST["title"]
    new_post.writer = request.POST["writer"]
    new_post.pub_date = timezone.now()
    new_post.image = request.FILES.get("image")
    new_post.body = request.POST["body"]
    new_post.mood = request.POST["mood"]
    new_post.tmi = request.POST["tmi"]
    new_post.save()

    return redirect("main:detail", new_post.id)

@login_required
def edit(request, id):
    edit_post = Post.objects.get(id=id)
    return render(request, "main/edit.html", {"post": edit_post})

@login_required
def update(request, id):
    update_post = Post.objects.get(id=id)
    update_post.title = request.POST["title"]
    update_post.writer = request.POST["writer"]
    update_post.pub_date = timezone.now()
    update_post.image = request.FILES.get("image",update_post.image)
    update_post.body = request.POST["body"]
    update_post.mood = request.POST["mood"]
    update_post.tmi = request.POST["tmi"]
    update_post.save()
    return redirect("main:detail", update_post.id)

@login_required
def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect("main:mainpage")
