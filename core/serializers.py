from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.serializers import PostSerializer


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['email','username','posts']
