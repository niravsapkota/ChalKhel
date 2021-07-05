# Generated by Django 3.2.4 on 2021-07-05 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0007_rename_sending_users_notification_sending_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='verb',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(max_length=500),
        ),
    ]
