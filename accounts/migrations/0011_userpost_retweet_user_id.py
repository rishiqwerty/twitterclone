# Generated by Django 2.2.25 on 2022-01-14 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_userpost_check_retweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='retweet_user_id',
            field=models.IntegerField(blank=True, default=19),
        ),
    ]
