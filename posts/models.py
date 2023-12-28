from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    author = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name="posts")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title