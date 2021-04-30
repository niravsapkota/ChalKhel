from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class UserProfile(models.Model):
    # slug = models.SlugField(null=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null="True", max_length=500, default=None)
    prestige_points = models.IntegerField(default = 0)
    # avatar_hex = models.CharField()
    # profile_pic = models.CharField()

    def __str__(self):
        return self.users

    def get_absoulte_url(self):
        return reverse('user_profile', kwargs={'user':self.slug})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.user)
    #     return super().save(*args,**kwargs)
