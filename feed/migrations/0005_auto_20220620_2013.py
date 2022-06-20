# Generated by Django 3.2.13 on 2022-06-20 20:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20220620_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
