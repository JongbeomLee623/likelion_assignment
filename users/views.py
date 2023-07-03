from django.shortcuts import render, get_object_or_404, redirect
from main.models import Post
from django.contrib.auth.models import User
# Create your views here.

def mypage(request, id):
    user = get_object_or_404(User, pk=id)
    context = {
        'user':user,
        'posts':Post.objects.filter(writer=user),
        # 'followings' : 팔로잉 전체 불러오기,
        # 'followers' : 팔로워 전체 불러오기,
        'followings': user.profile.followings.all(),
        'followers': user.profile.followers.all(),
    }
    return render(request, 'users/mypage.html', context)

def follow(request,id):
    user = request.user
    followed_user = get_object_or_404(User,pk=id)
    is_followed = user.profile in followed_user.profile.followers.all()
    if is_followed:
        user.profile.followings.remove(followed_user.profile)
    else:
        user.profile.followings.add(followed_user.profile)
    return redirect('users:mypage', followed_user.id)