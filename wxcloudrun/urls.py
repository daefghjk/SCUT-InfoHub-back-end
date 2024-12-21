from django.contrib import admin
from django.urls import path,include
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, UserListCreateView, UserDetailView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'comments', CommentDetailView, basename='comment')
router.register(r'posts', PostDetailView, basename='post')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view({'get': 'list','post':'like'}), name='post-detail'),
    
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view({'get': 'list','post':'like'}), name='comment-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
