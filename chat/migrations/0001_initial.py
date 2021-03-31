# Generated by Django 2.1.7 on 2021-03-31 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('type', models.CharField(default='comment', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('comment', models.TextField()),
                ('contentType', models.CharField(max_length=200)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('type', models.CharField(default='followers', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('type', models.CharField(default='follow', max_length=200)),
                ('id', models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('summary', models.CharField(max_length=200)),
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
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('type', models.CharField(default='author', max_length=200)),
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('host', models.URLField(null=True)),
                ('displayName', models.CharField(max_length=200, null=True)),
                ('url', models.URLField(null=True)),
                ('github', models.URLField(null=True)),
                ('followers', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Follower')),
                ('followings', models.ManyToManyField(blank=True, related_name='profile_followings', to='chat.Profile')),
                ('friend_requests', models.ManyToManyField(blank=True, related_name='profile_friend_requests', to='chat.FriendRequest')),
                ('friend_requests_sent', models.ManyToManyField(blank=True, related_name='profile_friend_requests_sent', to='chat.FriendRequest')),
                ('friends', models.ManyToManyField(blank=True, related_name='profile_friends', to='chat.Profile')),
                ('liked', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Liked')),
                ('timeline', models.ManyToManyField(blank=True, to='chat.Post')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Profile'),
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, to='chat.Comment'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, to='chat.Like'),
        ),
        migrations.AddField(
            model_name='like',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_author', to='chat.Profile'),
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
            model_name='friendrequest',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendrequest_author', to='chat.Profile'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendrequest_object', to='chat.Profile'),
        ),
        migrations.AddField(
            model_name='follower',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='follower_followers_items', to='chat.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Profile'),
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
