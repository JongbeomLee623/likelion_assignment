# Generated by Django 4.2 on 2023-05-27 02:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_post_mood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mood',
            field=models.CharField(choices=[('bad', '별로에요'), ('good', '좋아요'), ('so-so', '아무 생각이 없어요')], default='so-so', max_length=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
