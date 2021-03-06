# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 22:17
from __future__ import unicode_literals

import autoslug.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_project.mixins
import django_project.models
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(auto_now_add=True, verbose_name='date/time submitted')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_comments', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_comment', to='contenttypes.ContentType', verbose_name='content type')),
            ],
            options={
                'permissions': [('can_moderate', 'Can moderate comments')],
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ('-submit_date',),
            },
            bases=(django_project.mixins.CommentMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=64, populate_from='name', unique_with=('project',))),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'component',
                'verbose_name_plural': 'components',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True, verbose_name='joined at')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='member')),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=64, populate_from='name', unique_with=('project',))),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('deadline', models.DateField(default=datetime.date(2016, 5, 1), verbose_name='deadline')),
                ('date_completed', models.DateField(blank=True, null=True, verbose_name='date completed')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'milestone',
                'verbose_name_plural': 'milestones',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='ObjectTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.TextField(verbose_name='object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_objecttask', to='contenttypes.ContentType', verbose_name='content type')),
            ],
            options={
                'verbose_name': 'objecttask',
                'verbose_name_plural': 'objecttasks',
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('order', models.IntegerField(verbose_name='order')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=64, populate_from='name', unique_with=('project',))),
            ],
            options={
                'verbose_name': 'priority level',
                'verbose_name_plural': 'priority levels',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=128, populate_from='name', unique_with=('author',))),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(through='django_project.Membership', to=settings.AUTH_USER_MODEL, verbose_name='members')),
            ],
            options={
                'permissions': (('view_project', 'Can view project'), ('admin_project', 'Can administer project'), ('can_read_repository', 'Can read repository'), ('can_write_to_repository', 'Can write to repository'), ('can_add_task', 'Can add task'), ('can_change_task', 'Can change task'), ('can_delete_task', 'Can delete task'), ('can_view_tasks', 'Can view tasks'), ('can_add_member', 'Can add member'), ('can_change_member', 'Can change member'), ('can_delete_member', 'Can delete member')),
            },
            bases=(django_project.mixins.ProjectMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('order', models.IntegerField(verbose_name='order')),
                ('is_resolved', models.BooleanField(default=False, verbose_name='is resolved')),
                ('is_initial', models.BooleanField(default=False, verbose_name='is initial')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=64, populate_from='name', unique_with=('project',))),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=64, verbose_name='summary')),
                ('description', models.TextField(verbose_name='description')),
                ('deadline', models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='deadline')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('component', smart_selects.db_fields.ChainedForeignKey(chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.Component', verbose_name='component')),
                ('milestone', smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='project', chained_model_field='project', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_project.Milestone', verbose_name='milestone')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('priority', smart_selects.db_fields.ChainedForeignKey(chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.Priority', verbose_name='priority')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project', verbose_name='project')),
                ('status', smart_selects.db_fields.ChainedForeignKey(chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.Status', verbose_name='status')),
            ],
            bases=(django_project.mixins.TaskMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('order', models.IntegerField(verbose_name='order')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project')),
            ],
            options={
                'verbose_name': 'task type',
                'verbose_name_plural': 'task types',
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', django_project.models.ChainedForeignKeyTransition(chained_field='source', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.Status', verbose_name='destination status')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='django_project.Status', verbose_name='source status')),
            ],
            options={
                'verbose_name': 'transition',
                'verbose_name_plural': 'transitions',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.TaskType', verbose_name='task type'),
        ),
        migrations.AddField(
            model_name='status',
            name='destinations',
            field=models.ManyToManyField(blank=True, through='django_project.Transition', to='django_project.Status', verbose_name='destinations'),
        ),
        migrations.AddField(
            model_name='status',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project'),
        ),
        migrations.AddField(
            model_name='priority',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project'),
        ),
        migrations.AddField(
            model_name='objecttask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objecttask_tasks', to='django_project.Task', verbose_name='task'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='membership',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='component',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='transition',
            unique_together=set([('source', 'destination')]),
        ),
        migrations.AlterUniqueTogether(
            name='tasktype',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='status',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='priority',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='milestone',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('project', 'member')]),
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together=set([('project', 'name')]),
        ),
    ]
