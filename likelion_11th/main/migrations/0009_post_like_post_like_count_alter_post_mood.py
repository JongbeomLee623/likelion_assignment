# Generated by Django 4.2 on 2023-06-20 03:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_comment_tags_alter_post_mood'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='mood',
            field=models.CharField(choices=[('good', '좋아요'), ('so-so', '아무 생각이 없어요'), ('bad', '별로에요')], default='so-so', max_length=5),
        ),
    ]
