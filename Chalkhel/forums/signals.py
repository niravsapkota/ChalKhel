# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Profile, Post, Comment, Vote, Forum, ForumMember, Notification
# #
# # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# # def create_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         random_number = random.randint(0, 16777215)
# #         hex_number = str(hex(random_number))
# #         hex_number = '#' + hex_number[2:]
# #         profile = Profile.objects.create(user=instance, avatar_hexcode=hex_number.upper())
# #         profile.save()
# #
# # @receiver(post_save, sender=Vote)
# # def increase_comment_count(sender, instance, created, **kwargs):
# #     if created:
# #         instance.post.owner.profiles.prestige_points += 1
# #         instance.post.owner.profiles.save()
# #
# # @receiver(post_save, sender=Comment)
# # def increase_comment_count(sender, instance, created, **kwargs):
# #     if created:
# #         instance.post.comment_count += 1
# #         instance.post.save()
# #
# # @receiver(post_delete, sender=Comment)
# # def reduce_comment_count(sender, instance, **kwargs):
# #     instance.post.comment_count -= 1
# #     instance.post.save()
# #
# # @receiver(post_save, sender=Vote)
# # def increase_vote_count(sender, instance, created, **kwargs):
# #     if created:
# #         if instance.vote_type == 0:
# #             instance.post.dislikes += 1
# #         else:
# #             instance.post.likes += 1
# #         instance.post.save()
# #
# # @receiver(post_delete, sender=Vote)
# # def reduce_vote_count(sender, instance, **kwargs):
# #     if instance.vote_type == 0:
# #         instance.post.dislikes -= 1
# #     else:
# #         instance.post.likes -= 1
# #     instance.post.save()
# #
# # @receiver(post_save, sender=ForumMember)
# # def increase_member_count(sender, instance, created, **kwargs):
# #     if created:
# #         instance.forum.member_count += 1
# #         instance.forum.save()
# #
# # @receiver(post_delete, sender=ForumMember)
# # def reduce_member_count(sender, instance, **kwargs):
# #     instance.forum.member_count -= 1
# #     instance.forum.save()
