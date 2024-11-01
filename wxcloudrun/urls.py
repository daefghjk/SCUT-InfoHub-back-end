from wxcloudrun import views
from django.urls import path

urlpatterns = (
    # 获取主页
    path("", views.index),
)
