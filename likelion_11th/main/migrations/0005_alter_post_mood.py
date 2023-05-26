# Generated by Django 4.2 on 2023-05-27 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_post_mood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mood',
            field=models.CharField(choices=[('so-so', '아무 생각이 없어요'), ('bad', '별로에요'), ('good', '좋아요')], default='so-so', max_length=5),
        ),
    ]