from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic.edit import CreateView


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def blog_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

def blog_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/detail.html', {'post': post})

class PostCreate(CreateView):
    model = Post
    fields = '__all__'
    success_url = '/blog/'