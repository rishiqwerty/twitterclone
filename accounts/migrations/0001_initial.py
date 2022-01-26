# Generated by Django 2.2.25 on 2022-01-26 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.CharField(default='2022-1-1', max_length=12)),
                ('profile_pic', models.ImageField(default='spotify.png', upload_to='')),
                ('cover_pic', models.ImageField(default='wallpaperflare.com_wallpaper.jpg', upload_to='')),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('website', models.URLField(blank=True, max_length=50, null=True)),
                ('bio', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('follow_check', models.CharField(blank=True, default='Follow', max_length=40)),
                ('follower', models.ManyToManyField(related_name='follow', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retweet_user_id', models.CharField(blank=True, default=19, max_length=50)),
                ('check_retweet', models.BooleanField(blank=True, default=False)),
                ('tweet_post', models.TextField(max_length=500)),
                ('img', models.ImageField(blank=True, upload_to='images')),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('check_like', models.BooleanField(blank=True, default=False)),
                ('likes', models.ManyToManyField(blank=True, related_name='user_tweet', to=settings.AUTH_USER_MODEL)),
                ('retweet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.UserPost')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RetweetTweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retweet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.UserPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(blank=True, max_length=500, null=True)),
                ('img', models.ImageField(blank=True, upload_to='images')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL)),
                ('user_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_id', to='accounts.UserPost')),
            ],
        ),
    ]
