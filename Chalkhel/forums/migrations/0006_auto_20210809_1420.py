# Generated by Django 3.2.4 on 2021-08-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0005_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='bio',
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='forum',
            name='cover_pic',
            field=models.ImageField(blank=True, null=True, upload_to='post/image/'),
        ),
        migrations.AddField(
            model_name='forum',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='post/image/'),
        ),
    ]
