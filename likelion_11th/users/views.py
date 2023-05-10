from django.shortcuts import render
from main.models import Post
# Create your views here.
def mypage(request):
    user = request.user
    posts = Post.objects.filter(writer=user.profile.nickname)
    return render(request, 'users/mypage.html', {'posts': posts})