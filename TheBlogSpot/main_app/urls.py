from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog_posts, name='blog-posts' ),
    path('blog/<int:post_id>/', views.blog_detail, name='detail'),
    path('blog/create/', views.PostCreate.as_view(), name='post_create'),
    path('blog/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('blog/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('blog/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
]