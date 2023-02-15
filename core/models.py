from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='get_comment')
    user=models.CharField(max_length=100)
    text=models.CharField(max_length=3000, default='')
    comment_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.user

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name=models.CharField(max_length=500, default='')

class Message(models.Model):
    value=models.CharField(max_length=1000000)
    date=models.DateTimeField(default=datetime.now)
    user=models.CharField(max_length=100)
    room=models.CharField(max_length=100000)
    def __str__(self):
        return self.user

class Chat_list(models.Model):
    user=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    def __str__(self):
        return self.user