# Generated by Django 3.2.4 on 2021-08-09 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0003_alter_post_media_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='media_content',
            field=models.ImageField(blank=True, null=True, upload_to='post/image/'),
        ),
    ]
