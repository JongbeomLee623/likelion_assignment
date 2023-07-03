from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Tag
from django.utils import timezone
from django.db import models
from django.db.models import Q
import re
# from django.contrib.auth.decorators import login_required

# Create your views here.

def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        return render(request, "main/detail.html",{
            'post':post,
            'comments':comments,
        })
    elif request.method == 'POST':
        if request.user.is_authenticated:
            new_comment = Comment()
            # 댓글에 post 객체 넣기
            new_comment.post = post
            # 댓글 작성자 객체 넣기
            new_comment.writer = request.user
            new_comment.content = request.POST['content']
            new_comment.pub_date = timezone.now()
            new_comment.save()
            regex = re.compile('#([^\s`~!@#$%^&*()-+=\\\[\]\{\},.<>?]+)')
            tag_list = re.findall(regex, new_comment.content)
            for tags in tag_list:
                # 기존 get, 없으면 create
                tag, boolean = Tag.objects.get_or_create(name=tags)
                # 이후 필드에 추가
                new_comment.tags.add(tag.id)
            return redirect("main:detail", id)
        else:
            return redirect('accounts:login')



def mainpage(request):
    posts = Post.objects.all()
    return render(request, "main/mainpage.html", {"posts": posts})


def secondpage(request):
    return render(request, "main/secondpage.html")


def new(request):
    return render(request, "main/new.html")


def create(request):
    if request.user.is_authenticated:
        new_post = Post()
        new_post.title = request.POST["title"]
        new_post.writer = request.user
        new_post.pub_date = timezone.now()
        new_post.image = request.FILES.get("image")
        new_post.body = request.POST["body"]
        new_post.mood = request.POST["mood"]
        new_post.tmi = request.POST["tmi"]
        new_post.save()
        # 정규식 사용 #가 붙은 단어그룹 찾아서 리스트로 반환한 것을 tag_list에 넣음.
        regex = re.compile('#([^\s`~!@#$%^&*()-+=\\\[\]\{\},.<>?]+)')
        tag_list = re.findall(regex, new_post.body)
        for tags in tag_list:
            # 기존 get, 없으면 create
            tag, boolean = Tag.objects.get_or_create(name=tags)
            # 이후 필드에 추가
            new_post.tags.add(tag.id)
        return redirect("main:detail", new_post.id)
    else:
        return redirect('accounts:login')


def edit(request, id):
    edit_post = Post.objects.get(id=id)
    return render(request, "main/edit.html", {"post": edit_post})


def update(request, id):
    if request.user.is_authenticated:
        update_post = Post.objects.get(id=id)
        if request.user == update_post.writer:
            update_post.title = request.POST["title"]
            update_post.pub_date = timezone.now()
            update_post.image = request.FILES.get("image",update_post.image)
            update_post.body = request.POST["body"]
            update_post.mood = request.POST["mood"]
            update_post.tmi = request.POST["tmi"]
            update_post.tags.clear()
            update_post.save()
            regex = re.compile('#([^\s`~!@#$%^&*()-+=\\\[\]\{\},.<>?]+)')
            tag_list = re.findall(regex, update_post.body)
            for tags in tag_list:
            # 기존 get, 없으면 create
                tag, boolean = Tag.objects.get_or_create(name=tags)
                # 이후 필드에 추가
                update_post.tags.add(tag.id)
            # posts와 comment에 tag가 0개 존재 시 삭제
            Tag.objects.annotate(count=models.Count('posts') + models.Count('comments')).filter(count=0).delete()

            return redirect("main:detail", update_post.id)
    return redirect("accounts:login")


def delete(request, id):
    if request.user.is_authenticated:
        delete_post = Post.objects.get(id=id)
        delete_post.tags.clear()
        delete_post.delete()
        Tag.objects.annotate(count=models.Count('posts') + models.Count('comments')).filter(count=0).delete()
        return redirect("main:mainpage")
    return redirect("accounts:login")

def tag_list(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        return render(request, 'main/tag_list.html', {
            'tags': tags,
        })
    elif request.method == "POST":
        tag_name = request.POST.get('tagname')
        try:
            tag = Tag.objects.get(name=tag_name)
            return redirect("main:tag_posts", tag.id)
        except Tag.DoesNotExist:
            return render(request, 'main/tag_list.html', {
                'tags': Tag.objects.all(),
                'error_message': "검색 결과 없음",
            })

def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id = tag_id)
    # posts에 Post 객체들 중 tags의 이름이 tag이거나,
    # comment의 tag의 이름이 tag인 것을 합치고, distinct()를 통해 중복 제거.
    posts = Post.objects.filter(Q(tags=tag) | Q(comment__tags=tag)).distinct()
    
    return render(request, 'main/tag_posts.html',{
        'tag':tag,
        'posts':posts,
    })

def deleteComment(request, comment_id):
    if request.user.is_authenticated:
        delete_comment = get_object_or_404(Comment, id=comment_id)
        if request.user == delete_comment.writer:
            delete_comment.tags.clear()
            delete_comment.delete()
            Tag.objects.annotate(count=models.Count('posts') + models.Count('comments')).filter(count=0).delete()
            return redirect("main:detail", delete_comment.post.id)
    return redirect("accounts:login")

def likes (request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count +=1
        post.save()
    return redirect('main:detail',post_id)