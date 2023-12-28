from .models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = ['title','description','author','date_created','date_updated']
