# Generated by Django 3.0.6 on 2020-05-17 12:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0006_auto_20200517_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]