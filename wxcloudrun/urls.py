from django.contrib import admin
from django.urls import path,include
from .views import PostViewSet, CommentViewSet, UserListCreateView, UserDetailView, LoginView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
