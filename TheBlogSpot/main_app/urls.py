from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog_posts, name='blog-post' ),
    path('blog/<int:blog_id>/', views.blog_detail, name='detail'),
    path('blog/create/', views.PostCreate.as_view(), name='post_create')
]