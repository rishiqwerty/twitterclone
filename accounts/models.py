from re import T
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.CharField(default="2022-1-1", max_length=12, editable=True)
    profile_pic = models.ImageField(default="spotify.png")
    cover_pic = models.ImageField(default="wallpaperflare.com_wallpaper.jpg")
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    follower = models.ManyToManyField(User, related_name="follow")
    follow_check= models.CharField(max_length= 40, blank=True, default="Follow")
    def __str__(self):
        return self.user.username

    def number_of_followers(self):
        return self.follower.count()
    def number_of_following(self, pk):

        # x = UserProfile.objects.filter(follower=self).count()
        # user = UserProfile.objects.get(id=pk-1)
        # print("sfjds",user)
        # obj = user.follower.count()
        # print(obj)
        # map = {'id':pk}
        x=UserProfile.objects.raw('select * from accounts_userprofile_follower')
        count = 0
        for i in x:
            if i.user_id == pk:
                count += 1
        return count

class UserPost(models.Model):
    retweet = models.ForeignKey("self", null=True, on_delete=SET_NULL)
    retweet_user_id = models.CharField(max_length= 50, blank=True, default= 19)
    check_retweet = models.BooleanField(blank=True, default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet_post = models.TextField(max_length=500)
    img = models.ImageField(
        upload_to="images",
        blank=True,
    )
    date_published = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        related_name="user_tweet",
        blank=True,
    )
    check_like = models.BooleanField(blank=True, default=False)

    def number_of_likes(self):
        return self.likes.count()


# class Like(models.Model):
#     tweet = models.ForeignKey(UserPost, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
class RetweetTweet(models.Model):
    retweet = models.ForeignKey(UserPost, null=True, on_delete=SET_NULL)
    user = models.ForeignKey(User, on_delete=CASCADE)


class Comments(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="post_id")
    user = models.ForeignKey(User, related_name="user_id", on_delete=CASCADE ,default=1)
    comments = models.TextField(max_length=500, null=True, blank=True)
    img = models.ImageField(
        upload_to="images",
        blank=True,
    )
    created_on = models.DateTimeField(default=timezone.now)

    
