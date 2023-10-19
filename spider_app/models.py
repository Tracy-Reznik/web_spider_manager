from django.db import models


class User(models.Model):
    uid = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    sign = models.TextField()
    face = models.URLField()

    def __str__(self):
        return f"Comment {self.name}"


class Video(models.Model):
    bvid = models.CharField(max_length=20, unique=True)
    aid = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=200)
    pic = models.URLField()
    description = models.TextField()
    pubdate = models.DateTimeField()
    duration = models.PositiveIntegerField()
    view_count = models.PositiveIntegerField()
    danmaku_count = models.PositiveIntegerField()
    reply_count = models.PositiveIntegerField()
    favorite_count = models.PositiveIntegerField()
    coin_count = models.PositiveIntegerField()
    share_count = models.PositiveIntegerField()
    like_count = models.PositiveIntegerField()
    dislike_count = models.PositiveIntegerField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Page(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    cid = models.PositiveIntegerField(unique=True)
    page = models.PositiveIntegerField()
    part = models.CharField(max_length=200)
    path = models.URLField(default="")

    def __str__(self):
        return f"Page {self.page} - {self.part}"


class Comment(models.Model):
    rpid = models.CharField(max_length=20, unique=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    like = models.PositiveIntegerField()
    ctime = models.DateTimeField()
    comment = models.TextField()

    def __str__(self):
        return f"Comment {self.rpid}-{self.comment}"


class Reply(models.Model):
    rpid = models.CharField(max_length=20, unique=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.PositiveIntegerField()
    ctime = models.DateTimeField()
    reply = models.TextField()

    def __str__(self):
        return f"Reply {self.rpid}-{self.reply}"


class Danmaku(models.Model):
    time = models.FloatField()
    mode = models.CharField(max_length=10)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    dtype = models.CharField(max_length=20)
    user_hash = models.CharField(max_length=100)
    danmaku_id = models.CharField(max_length=20, unique=True)
    text = models.TextField()
    video_page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return f"Danmaku {self.danmaku_id} - {self.text}"
