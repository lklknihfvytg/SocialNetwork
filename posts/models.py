from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=1280, blank=True)
    post_pic = models.CharField(max_length=128, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through="PostLike", related_name='post_likes')
    comments = models.ManyToManyField(User, through="PostComment", related_name='post_comments')
    reposts = models.ManyToManyField(User, through="RePost", related_name='reposts')
    is_tiny = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']


@receiver(pre_save, sender=Post)
def name_uppercase(sender, instance, *args, **kwargs):
    if len(instance.text) < 42 and not instance.post_pic:
        instance.is_tiny = True


class PostLike(models.Model):
    user_like = models.ForeignKey(User, on_delete=models.CASCADE)
    post_like = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1280, blank=True)


class RePost(models.Model):
    user_repost = models.ForeignKey(User, on_delete=models.CASCADE)
    post_repost = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
