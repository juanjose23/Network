
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/",views.post_create, name="create"),
    path('posts/<int:post_id>/like', views.toggle_like, name='toggle_like'),
    path('users/<int:user_id>/follow', views.toggle_follow, name='toggle_follow'),
    path('posts/<int:post_id>/edit', views.edit_post, name='edit'),
    path("following-posts/", views.following_posts, name='following_posts'),
    path('profile/<str:username>/', views.user_profile, name='user_profile')
]
