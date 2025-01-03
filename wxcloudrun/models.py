from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, openid, **extra_fields):
        if not openid:
            raise ValueError('The OpenID must be set')
        user = self.model(openid=openid, **extra_fields)
        user.save(using=self.db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    openid = models.CharField(primary_key=True, max_length=50)
    session_key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    major = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'openid'
    REQUIRED_FIELD = []

    class Meta:
        db_table = 'users'
        managed = True

    def __str__(self):
        return self.openid

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'
        managed = True

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
        managed = True

    def __str__(self):
        return f'Comment by openid:{self.author.openid} on post_id:{self.post.post_id}'

class CommentsLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='Commentslikes'
        managed = True
        unique_together = ('comment', 'author')
        
    def __str__(self):
        return f'Comment by openid:{self.author.openid}'
    
class PostLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='postlikes'
        managed = True
        unique_together = ('post', 'author')
        
    def __str__(self):
        return f'Postlike by openid:{self.author.openid}'
    
class Follower(models.Model):
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'follower')