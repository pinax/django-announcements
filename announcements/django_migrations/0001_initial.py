# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation_date')),
                ('site_wide', models.BooleanField(default=False, verbose_name='site wide')),
                ('members_only', models.BooleanField(default=False, verbose_name='members only')),
                ('dismissal_type', models.IntegerField(default=2, choices=[(1, 'No Dismissals Allowed'), (2, 'Session Only Dismissal'), (3, 'Permanent Dismissal Allowed')])),
                ('publish_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publish_start')),
                ('publish_end', models.DateTimeField(null=True, verbose_name='publish_end', blank=True)),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'announcement',
                'verbose_name_plural': 'announcements',
            },
        ),
        migrations.CreateModel(
            name='Dismissal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dismissed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('announcement', models.ForeignKey(related_name='dismissals', to='announcements.Announcement')),
                ('user', models.ForeignKey(related_name='announcement_dismissals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
