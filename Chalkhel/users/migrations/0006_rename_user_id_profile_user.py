# Generated by Django 3.2 on 2021-05-02 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_user_profile_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user_id',
            new_name='user',
        ),
    ]
