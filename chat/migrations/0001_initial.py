# Generated by Django 2.1.7 on 2021-03-29 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('type', models.CharField(default='author', max_length=200)),
                ('id', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('host', models.URLField(null=True)),
                ('displayName', models.CharField(max_length=200, null=True, unique=True)),
                ('url', models.URLField(null=True)),
                ('github', models.URLField(null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('type', models.CharField(default='comment', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('comment', models.TextField()),
                ('contentType', models.CharField(max_length=200)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('type', models.CharField(default='followers', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('items', models.ManyToManyField(blank=True, related_name='follower_followers_items', to='chat.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('type', models.CharField(default='follow', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('summary', models.CharField(max_length=200)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendrequest_author', to='chat.Profile')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendrequest_object', to='chat.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('friend_requests', models.ManyToManyField(blank=True, to='chat.FriendRequest')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('type', models.CharField(default='like', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('context', models.CharField(default='Like', max_length=200)),
                ('summary', models.CharField(default='Like', max_length=200)),
                ('object', models.CharField(default='Like', max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_author', to='chat.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('type', models.CharField(default='liked', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('items', models.ManyToManyField(blank=True, to='chat.Like')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('type', models.CharField(default='post', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('title', models.TextField()),
                ('source', models.URLField()),
                ('origin', models.URLField()),
                ('description', models.TextField()),
                ('contentType', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('categories', models.CharField(max_length=200)),
                ('count', models.IntegerField(default=0)),
                ('size', models.IntegerField(default=0)),
                ('comments_url', models.CharField(max_length=200)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('visibility', models.CharField(max_length=50)),
                ('unlisted', models.CharField(default='false', editable=False, max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Profile')),
                ('comments', models.ManyToManyField(blank=True, to='chat.Comment')),
                ('likes', models.ManyToManyField(blank=True, to='chat.Like')),
            ],
        ),
        migrations.CreateModel(
            name='PostInbox',
            fields=[
                ('type', models.CharField(blank=True, default='inbox', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
                ('items', models.ManyToManyField(blank=True, to='chat.Post')),
            ],
        ),
        migrations.AddField(
            model_name='inbox',
            name='like_inbox',
            field=models.ManyToManyField(blank=True, to='chat.Like'),
        ),
        migrations.AddField(
            model_name='inbox',
            name='post_inbox',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.PostInbox'),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, to='chat.Like'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Post'),
        ),
    ]
