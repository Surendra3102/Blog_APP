from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    image=models.ImageField(upload_to='blog_images/', blank=True, null=True)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    blog = models.ForeignKey(Blog, related_name='likes_set', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

