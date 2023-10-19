# Generated by Django 3.2 on 2023-08-21 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rpid', models.CharField(max_length=20, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('like', models.PositiveIntegerField()),
                ('ctime', models.DateTimeField()),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=10)),
                ('sign', models.TextField()),
                ('face', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bvid', models.CharField(max_length=20, unique=True)),
                ('aid', models.PositiveIntegerField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('pic', models.URLField()),
                ('description', models.TextField()),
                ('pubdate', models.DateTimeField()),
                ('duration', models.PositiveIntegerField()),
                ('view_count', models.PositiveIntegerField()),
                ('danmaku_count', models.PositiveIntegerField()),
                ('reply_count', models.PositiveIntegerField()),
                ('favorite_count', models.PositiveIntegerField()),
                ('coin_count', models.PositiveIntegerField()),
                ('share_count', models.PositiveIntegerField()),
                ('like_count', models.PositiveIntegerField()),
                ('dislike_count', models.PositiveIntegerField()),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rpid', models.CharField(max_length=20, unique=True)),
                ('like', models.PositiveIntegerField()),
                ('ctime', models.DateTimeField()),
                ('reply', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider_app.comment')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.PositiveIntegerField(unique=True)),
                ('page', models.PositiveIntegerField()),
                ('part', models.CharField(max_length=200)),
                ('filepath', models.CharField(max_length=200)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider_app.video')),
            ],
        ),
        migrations.CreateModel(
            name='Danmaku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.FloatField()),
                ('mode', models.CharField(max_length=10)),
                ('size', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField()),
                ('dtype', models.CharField(max_length=20)),
                ('user_hash', models.CharField(max_length=100)),
                ('danmaku_id', models.CharField(max_length=20, unique=True)),
                ('text', models.TextField()),
                ('video_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider_app.page')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider_app.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider_app.video'),
        ),
    ]