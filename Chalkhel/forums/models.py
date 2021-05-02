from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None, null=False)
    name = models.CharField(max_length=25, default=None, null=False, unique=True)
    members = models.IntegerField(default = 0)
    hidden = models.BooleanField(default=0)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None, null=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE,default=None, null=False)
    title = models.TextField(null="False", max_length=500, default="")
    body = models.TextField(null="False", max_length=5000, default="")
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)
    comments = models.IntegerField(default = 0)
    hidden = models.BooleanField(default=0)

    def __str__(self):
        return self.title

class ForumMember(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE,default=None, null=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE,default=None, null=False)
