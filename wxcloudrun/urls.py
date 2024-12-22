from django.contrib import admin
from django.urls import path,include
from .views import PostViewSet, CommentViewSet, UserListCreateView, UserDetailView, LoginView,FanCountView, FanListView,unfollow_user,follow_user
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('<str:name>/fan-count/', FanCountView.as_view(), name='fan-count'),
    path('<str:name>/fans/', FanListView.as_view(), name='fan-list'),
    path('api/fans/follow/<int:user_id>/', follow_user, name='follow-user'),
    path('api/fans/unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    
    path('', include(router.urls)),
]
