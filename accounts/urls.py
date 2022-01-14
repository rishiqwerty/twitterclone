from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name= "profile"),
    path("profile_user/<int:pk>/", views.users_profile, name= "profile_user"),
    path("post_del/<int:pk>/", views.post_delete, name= "post_delete"),
    path("comment_del/<int:pk>/", views.comment_delete, name= "comment_delete"),
    path("profile_edit/", views.profile_edit, name= "profile_edit"),
    path("new_post/", views.user_posts_form, name= "user_post"),
    path("search/", views.search_users, name= "search_users"),
    path("post/<int:pk>", views.post_detail, name= "post_detail"),
    path("follower/<int:pk>", views.follow, name="follow"),
    path("liked/<int:pk>", views.liked_post, name="liked_post"),
    path("", views.dashboard, name="dashboard"),
    path("retweet/<int:pk>", views.retweet, name="retweet")
]
