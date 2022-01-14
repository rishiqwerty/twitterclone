# Generated by Django 2.2.25 on 2022-01-13 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0008_auto_20220113_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follower',
            field=models.ManyToManyField(related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserFollowing',
        ),
    ]
