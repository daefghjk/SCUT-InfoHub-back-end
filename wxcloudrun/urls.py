from django.contrib import admin
from django.urls import path,include
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, UserListCreateView, UserDetailView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework import routers, viewsets
# 创建路由器并注册视图集
router = routers.DefaultRouter()
router.register(r'comments', CommentDetailView)
router.register(r'posts', PostDetailView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostDetailView.as_view({'post': 'like'}), name='post-like'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
