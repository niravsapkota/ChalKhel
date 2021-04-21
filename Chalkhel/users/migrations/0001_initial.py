# Generated by Django 3.2 on 2021-04-21 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChalkhelUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('bio', models.TextField(blank=True, default=None, max_length=500, null='True')),
                ('prestige_points', models.IntegerField(default=0)),
            ],
        ),
    ]
