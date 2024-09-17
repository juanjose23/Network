from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500)  
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}..."

    @property
    def likes_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-timestamp'] 

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    class Meta:
        unique_together = ('follower', 'following')  

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

    class Meta:
        unique_together = ('user', 'post') 


