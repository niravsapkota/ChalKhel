# Generated by Django 3.2.4 on 2021-08-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0008_alter_post_media_content_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='media_content_video',
            field=models.FileField(blank=True, null=True, upload_to='post/video/', verbose_name=''),
        ),
    ]
