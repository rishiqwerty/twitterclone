# Generated by Django 2.2.25 on 2022-01-15 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_userprofile_follow_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follow_check',
            field=models.CharField(blank=True, default='Follow', max_length=40),
        ),
    ]
