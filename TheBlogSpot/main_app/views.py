from django.shortcuts import render, redirect
from .models import Post, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
import os


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


class PostUpdate(UpdateView):
  model = Post
  fields = '__all__'
  success_url = '/blog/'

class PostDelete(DeleteView):
  model = Post
  success_url = '/blog/'


def add_photo(request, post_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, post_id=post_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', post_id=post_id)