# Generated by Django 5.0.1 on 2024-07-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_alter_profile_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likepost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]
