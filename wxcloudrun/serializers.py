from rest_framework import serializers
from .models import Post, Comment, User,Like

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
    likes_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['comment_id', 'post', 'content', 'author', 'create_time','likes_count']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
class LoginSerializer(serializers.ModelSerializer):
    code = serializers.CharField(allow_blank=False)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['comment_id', 'author', 'comment', 'created_time']
