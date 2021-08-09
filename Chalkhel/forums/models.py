from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ImageField
from django.db.models import PositiveIntegerField
from django.db.models import PositiveSmallIntegerField
from django.db.models import SmallIntegerField
from django.db.models import TextField
from django_extensions.db.fields import AutoSlugField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import random
from django.contrib.contenttypes.fields import GenericRelation

class Vote(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    vote_type = models.PositiveSmallIntegerField(null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # Relationship Fields
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="votes",
    )



    class Meta:
        ordering = ('-created',)
        unique_together = ('object_id', 'owner', 'content_type')

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('forums_vote_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('forums_vote_update', args=(self.pk,))


class Profile(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    slug = extension_fields.AutoSlugField(populate_from='user', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    bio = models.TextField(max_length=300)
    prestige_points = models.PositiveIntegerField(default=0)
    avatar_hexcode = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to="post/image/", null=True, blank=True)

    # Relationship Fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="profiles",
    )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('forums_profile_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('forums_profile_update', args=(self.slug,))

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            random_number = random.randint(0, 16777215)
            hex_number = str(hex(random_number))
            hex_number = '#' + hex_number[2:]
            profile = Profile.objects.create(user=instance, avatar_hexcode=hex_number.upper())
            profile.save()

    # @receiver(post_save, sender=Comment)
    # def increase_comment_count(sender, instance, created, **kwargs):
    #     if created:
    #         instance.post.owner.profiles.prestige_points += 1
    #         instance.post.owner.profiles.save()


class Comment(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    slug = extension_fields.AutoSlugField(populate_from='body', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    body = models.TextField(max_length=2000)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    votes = GenericRelation(Vote, related_query_name='votes')
    # Relationship Fields
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="comments",
    )
    post = models.ForeignKey(
        'forums.Post',
        on_delete=models.CASCADE, related_name="comments",
    )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('forums_comment_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('forums_comment_update', args=(self.slug,))

    # @receiver(post_save, sender=Vote)
    # def increase_vote_count(sender, instance, created, **kwargs):
    #     if created:
    #         if instance.vote_type == 0:
    #             instance.dislikes += 1
    #         else:
    #             instance.likes += 1
    #         instance.post.save()
    #
    # @receiver(post_delete, sender=Vote)
    # def reduce_vote_count(sender, instance, **kwargs):
    #     if instance.vote_type == 0:
    #         instance.dislikes -= 1
    #     else:
    #         instance.likes -= 1
    #     instance.post.save()


class Post(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    hidden = models.BooleanField(default=0)
    last_updated = models.DateTimeField(auto_now=True, editable=True)
    media_content_type = models.SmallIntegerField(null=True, blank=True)
    # media_content = models.ImageField(upload_to="post/image/", null=True, blank=True)
    media_content = models.FileField(upload_to='post/media_content/', null=True,blank=True, verbose_name='')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    body = models.TextField(max_length=5000)
    votes = GenericRelation(Vote, related_query_name='votes')

    # Relationship Fields
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="posts",
    )
    forum = models.ForeignKey(
        'forums.Forum',
        on_delete=models.CASCADE, related_name="posts",
    )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('forums_post_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('forums_post_update', args=(self.slug,))

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    @receiver(post_save, sender=Comment)
    def increase_comment_count(sender, instance, created, **kwargs):
        if created:
            instance.post.comment_count += 1
            instance.post.save()

    @receiver(post_delete, sender=Comment)
    def reduce_comment_count(sender, instance, **kwargs):
        instance.post.comment_count -= 1
        instance.post.save()

    # @receiver(post_save, sender=Vote)
    # def increase_vote_count(sender, instance, created, **kwargs):
    #     if created:
    #         if instance.content_type.model == "post":
    #             if instance.vote_type == 0:
    #                 instance.content_object.likes -= 1
    #                 instance.content_object.dislikes += 1
    #             else:
    #                 instance.content_object.dislikes -= 1
    #                 instance.content_object.likes += 1
    #             instance.content_object.save()
    #
    # @receiver(post_delete, sender=Vote)
    # def reduce_vote_count(sender, instance, **kwargs):
    #     if instance.content_type.model == "post":
    #         if instance.vote_type == 0:
    #             instance.content_object.dislikes -= 1
    #         else:
    #             instance.content_object.likes -= 1
    #         instance.content_object.save()


class ForumMember(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="forummembers",
    )
    forum = models.ForeignKey(
        'forums.Forum',
        on_delete=models.CASCADE, related_name="forummembers",
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('forum', 'member')

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('forums_forummember_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('forums_forummember_update', args=(self.pk,))


class Forum(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None, null=False, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    bio = models.TextField(max_length=300, blank=True)
    cover_pic = models.ImageField(upload_to="post/image/", null=True, blank=True)
    profile_pic = models.ImageField(upload_to="post/image/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    member_count = models.PositiveIntegerField(default=0)

    # Relationship Fields
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="forums",
    )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('forums_forum_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('forums_forum_update', args=(self.slug,))

    def members(self):
        users = []
        for user in self.forummembers.all():
            users.append(user.member)
        return users

    @receiver(post_save, sender=ForumMember)
    def increase_member_count(sender, instance, created, **kwargs):
        if created:
            instance.forum.member_count += 1
            instance.forum.save()

    @receiver(post_delete, sender=ForumMember)
    def reduce_member_count(sender, instance, **kwargs):
        instance.forum.member_count -= 1
        instance.forum.save()


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    is_read = models.PositiveSmallIntegerField(null=False, default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    tag = models.CharField(max_length=255, default="", null=False, blank=True)

    affected_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="affected_agent",
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=True)

    def __unicode__(self):
        return u'%s' % self.slug

    @receiver(post_save, sender=Comment)
    def create_comment_notification(sender, instance,created, **kwargs):
        if created:
            tag = "commented on"
            notification = Notification.objects.create(tag=tag, affected_agent=instance.post.owner, content_object=instance)
            notification.save()

    @receiver(post_save, sender=Vote)
    def create_vote_notification(sender, instance,created, **kwargs):
        if created:
            tag = "voted"
            notification = Notification.objects.create(tag=tag, affected_agent=instance.content_object.owner, content_object=instance)
            notification.save()
