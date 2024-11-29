from rest_framework import serializers
from .models import Post, Comment, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['openid', 'session_key', 'name', 'grade', 'major']

class PostSerializer(serializers.ModelSerializer):
    poster = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['post_id', 'title', 'content', 'poster', 'create_time']

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = ['comment_id', 'post', 'content', 'author', 'create_time']

class LoginSerializer(serializers.ModelSerializer):
    code = serializers.CharField(allow_blank=False)
