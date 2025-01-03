from rest_framework import generics, status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from django.contrib.auth import login
from django.db.models import Count
from .models import Post, Comment, User,CommentsLike,PostLike,Follower
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LoginSerializer,FollowerSerializer
from django.conf import settings
import requests
from rest_framework.decorators import api_view, permission_classes

class UserUpdateView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        openid = request.headers.get('X-WX-OPENID')
        if not openid:
            return Response({'error':'X-WX-OPENID header is required'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data['openid'] = openid
        try:
            user = User.objects.get(openid=openid)
            serializer = UserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCheckView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        openid = request.headers.get('X-WX-OPENID')
        if not openid:
            return Response({'error': 'X-WX-OPENID header is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(openid=openid)
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error':'User not found', 'openid':openid}, status=status.HTTP_404_NOT_FOUND)

class PostPagination(PageNumberPagination):
    page_size = 5
    page_size_query_description = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-create_time')
        openid = self.request.data.get('openid', None)
        if openid is not None:
            queryset = queryset.filter(poster__openid=openid)
        return queryset
    
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

class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_description = 'page_size'
    max_page_size = 100

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.all().annotate(likes_count=Count('likes')).order_by('-likes_count', '-create_time')
        post_id = self.request.data.get('post_id', None)
        if post_id is not None:
            queryset = queryset.filter(post__post_id=post_id)
        return queryset

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

class FanCountView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'name'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        fan_count = instance.followers.count()
        return Response({'name': instance.name, 'fan_count': fan_count})

class FanListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    
    def get_queryset(self):
        name = self.kwargs['name']
        user = User.objects.get(name=name)
        return Follower.objects.filter(user=user)
#取关动作    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        follower = request.user
        user = User.objects.get(openid=user_id)
        follower_instance = Follower.objects.get(user=user, follower=follower)
        follower_instance.delete()
        return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
    except Follower.DoesNotExist:
        return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
#关注动作
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        follower = request.user
        user = User.objects.get(openid=user_id)
        # Check if the user is already followed to avoid duplicate entries
        if not Follower.objects.filter(user=user, follower=follower).exists():
            Follower.objects.create(user=user, follower=follower)
            return Response({'message': 'Followed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    