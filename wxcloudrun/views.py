from rest_framework import generics, status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Comment, User,Like
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LoginSerializer, LikeSerializer
from django.conf import settings

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save()

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

    def perform_create(self, serializer):
        serializer.save()

class CommentDetailView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            return Response({"detail": "You have already liked this comment."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Comment liked successfully."}, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        code = serializer.validated_data['code']
        appid = settings.WeChat_Appid
        appsecret = settings.WeChat_Appsecret
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            "appid": appid,
            "secret": appsecret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        response = request.get(url, params=params)
        result = response.json()
        if "openid" in result and "session_key" in result:
            openid = result["openid"]
            session_key = result["session_key"]
            user, created = User.objects.get_or_create(openid=openid)
            user.session_key = session_key
            user.save()
            return Response({"openid": openid}, status=status.HTTP_200_OK)
        return Response({"error": "Fail to fetch openid", "details":result}, status=status.HTTP_400_BAD_REQUEST)
