from rest_framework import generics, status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.contrib.auth import login
from .models import Post, Comment, User,CommentsLike,PostLike
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LoginSerializer, LikeSerializer
from django.conf import settings
import requests

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class PostDetailView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        try:
            post_instance = self.get_object()
            like, created = PostLike.objects.get_or_create(post=post_instance, author=request.user)
            if not created:
                return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        except self.queryset.model.DoesNotExist:
            raise NotFound("Post not found.")

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class CommentDetailView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        try:
            comment = self.get_object()
            like, created = CommentsLike.objects.get_or_create(comment=comment, author=request.user)
            if not created:
                return Response({"detail": "You have already liked this comment."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Comment liked successfully."}, status=status.HTTP_201_CREATED)
        except Http404:
            raise NotFound("Comment not found.")

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        code = serializer.validated_data['code']
        appid = settings.WECHAT_APPID
        appsecret = settings.WECHAT_APPSECRET
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            "appid": appid,
            "secret": appsecret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        response = requests.get(url, params=params, verify=False)
        result = response.json()
        if "openid" in result and "session_key" in result:
            openid = result["openid"]
            session_key = result["session_key"]
            user, created = User.objects.get_or_create(openid=openid)
            user.session_key = session_key
            user.save()
            login(request, user)
            return Response({
                "detail": "Login successfully",
                "openid": openid
            }, status=status.HTTP_200_OK)
        return Response({"error": "Fail to fetch openid", "details":result}, status=status.HTTP_400_BAD_REQUEST)
