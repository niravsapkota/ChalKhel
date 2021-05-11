from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    # slug = models.SlugField(null=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null="True", max_length=500, default=None)
    prestige_points = models.IntegerField(default = 0)
    avatar_hex = models.CharField(max_length=6, default="FFFF")
    profile_pic = models.CharField(max_length=300, null=True)

    def __str__(self):
        return "%s 's profile" % self.user

    # def get_absoulte_url(self):
    #     return reverse('user_profile', kwargs={'user':self.user})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
