# Generated by Django 2.2.25 on 2022-01-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_userpost_check_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.CharField(default='2022-1-1', max_length=12),
        ),
    ]
