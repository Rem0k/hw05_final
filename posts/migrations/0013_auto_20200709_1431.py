# Generated by Django 2.2.9 on 2020-07-09 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20200609_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='author',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]