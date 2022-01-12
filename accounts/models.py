from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.CharField(default="22-12-2022", max_length=12, editable=True)
    profile_pic = models.ImageField(default="spotify.png")
    cover_pic = models.ImageField(default="wallpaperflare.com_wallpaper.jpg")
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username


class UserPost(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet_post = models.TextField(max_length=500)
    img = models.ImageField(
        upload_to="images",
        blank=True,
    )
    date_published = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        related_name="user_tweet",
        blank=True,
    )


class Like(models.Model):
    tweet = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


class Comments(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="post_id")
    user = models.ForeignKey(User, related_name="user_id", on_delete=CASCADE ,default=1)
    comments = models.TextField(max_length=500, null=True, blank=True)
    img = models.ImageField(
        upload_to="images",
        blank=True,
    )
    created_on = models.DateTimeField(default=timezone.now)

    
