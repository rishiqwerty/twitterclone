from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name= "profile"),
    path("post_del/<int:pk>/", views.post_delete, name= "post_delete"),
    path("profile_edit/", views.profile_edit, name= "profile_edit"),
    path("new_post/", views.user_posts_form, name= "user_post"),
    path("", views.dashboard, name="dashboard"),
]
