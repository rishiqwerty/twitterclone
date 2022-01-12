from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Like, UserPost, UserProfile, Comments
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserPost)
admin.site.register(Comments)
admin.site.register(Like)