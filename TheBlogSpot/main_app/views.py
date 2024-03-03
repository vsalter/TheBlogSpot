from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
import os
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def blog_posts(request):
    # posts = Post.objects.all()
    posts = Post.objects.filter(user=request.user)
    return render(request, 'blog/index.html', {'posts': posts})

@login_required
def blog_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/detail.html', {'post': post})

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']
    # success_url = '/blog/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        return reverse('detail', args=(self.object.id,))


class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = '__all__'
  success_url = '/blog/'

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/blog/'

@login_required
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


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return redirect('blog-posts')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'registration/signup.html', context)