from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def blog_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})