# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(unique=True)),
                ('key', models.CharField(max_length=255)),
                ('optimized_key', models.CharField(max_length=255)),
                ('thumbnail_key', models.CharField(max_length=255)),
                ('optimized_url', models.URLField()),
                ('thumbnail_url', models.URLField()),
                ('original_filename', models.CharField(max_length=255)),
                ('date_taken', models.DateTimeField(null=True)),
                ('iso', models.IntegerField(null=True)),
                ('width', models.PositiveSmallIntegerField()),
                ('height', models.PositiveSmallIntegerField()),
                ('size', models.PositiveIntegerField()),
                ('camera_make', models.CharField(max_length=32, null=True)),
                ('camera_model', models.CharField(max_length=128, null=True)),
                ('lens_model', models.CharField(max_length=128, null=True)),
                ('f_stop_denominator', models.IntegerField(null=True)),
                ('f_stop_numerator', models.IntegerField(null=True)),
                ('exposure_denominator', models.IntegerField(null=True)),
                ('exposure_numerator', models.IntegerField(null=True)),
                ('focal_length_denominator', models.IntegerField(null=True)),
                ('focal_length_numerator', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SortedPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveSmallIntegerField()),
                ('album', models.ForeignKey(to='photos.Album')),
                ('photo', models.ForeignKey(to='photos.Photo')),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photo',
            name='private_tags',
            field=models.ManyToManyField(to='photos.Tag', related_name='private_tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='public_tags',
            field=models.ManyToManyField(to='photos.Tag', related_name='public_tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(through='photos.SortedPhoto', to='photos.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
