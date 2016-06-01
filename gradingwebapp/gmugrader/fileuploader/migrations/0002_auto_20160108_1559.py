# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-08 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import fileuploader.models


class Migration(migrations.Migration):

    dependencies = [
        ('fileuploader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('fileshot', models.FileField(upload_to=fileuploader.models.get_upload_file_name)),
            ],
        ),
        migrations.DeleteModel(
            name='Solutions',
        ),
    ]