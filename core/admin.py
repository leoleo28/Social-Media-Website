from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, Comment, Room, Message, Chat_list

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Chat_list)