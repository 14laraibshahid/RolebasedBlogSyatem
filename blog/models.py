from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    class Meta:
        permissions = [
            # Add any custom permissions you need here
        ]
        # Set a custom related_name for user_permissions
        default_related_name = 'custom_user_permissions'

    def __str__(self):
        return self.username

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post_users')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
