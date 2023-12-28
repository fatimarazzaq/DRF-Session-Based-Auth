from django.contrib import admin
from django.urls import path
from .views import PostList,PostCreate,PostDetail

urlpatterns = [
    path("posts/",PostList.as_view(),name="post-list"),
    path("post/create/",PostCreate.as_view(),name="post-create"),
    path("post/detail/<int:pk>/",PostDetail.as_view(),name="post-detail"),
]
