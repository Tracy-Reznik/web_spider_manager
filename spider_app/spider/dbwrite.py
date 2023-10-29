import random
import time

from spider_app.models import *
from spider_app.spider.base import get_pictures, video_base


def userwrite(userdata):
    if len(User.objects.filter(uid=userdata["uid"])) <= 0:
        user = User(
            uid=userdata["uid"],
            name=userdata["name"],
            sex=userdata["sex"],
            sign=userdata["sign"],
            face=userdata["face"],
        )
        user.save()
    else:
        user = User.objects.get(uid=userdata["uid"])
        user.name = userdata["name"]
        user.sex = userdata["sex"]
        user.sign = userdata["sign"]
        user.face = userdata["face"]
        user.save()
    return user


def commentwrite(data):
    video = Video.objects.get(aid=data["aid"])
    for commentdict in data["comment"]:
        comment_member = userwrite(commentdict["member"])

        if len(Comment.objects.filter(rpid=commentdict["rpid"])) <= 0:
            comment = Comment(
                rpid=commentdict["rpid"],
                member=comment_member,
                video=video,
                location=commentdict["location"],
                like=commentdict["like"],
                ctime=commentdict["ctime"],
                comment=commentdict["comment"]
            )
            comment.save()
        else:
            comment = Comment.objects.get(rpid=commentdict["rpid"])
        for replydict in commentdict["replies"]:
            reply_member = userwrite(replydict["member"])
            if len(Reply.objects.filter(rpid=replydict["rpid"])) <= 0:
                reply = Reply(
                    rpid=replydict["rpid"],
                    member=reply_member,
                    comment=comment,
                    like=replydict["like"],
                    ctime=replydict["ctime"],
                    reply=replydict["comment"],
                )
                try:
                    reply.save()
                except:
                    pass
            del reply_member


def danmakuwrite(data, cid):
    page = Page.objects.get(cid=cid)
    for danmakudict in data:
        if len(Danmaku.objects.filter(danmaku_id=danmakudict["danmaku_id"])) <= 0:
            danmaku = Danmaku(
                time=danmakudict["time"],
                mode=danmakudict["mode"],
                size=danmakudict["size"],
                color=danmakudict["color"],
                timestamp=danmakudict["timestamp"],
                dtype=danmakudict["type"],
                user_hash=danmakudict["user-hash"],
                danmaku_id=danmakudict["danmaku_id"],
                text=danmakudict["text"],
                video_page=page
            )
            danmaku.save()


def videowrite(info):
    uploader = userwrite(info["uploader"])
    if len(Video.objects.filter(bvid=info["bvid"])) <= 0:
        video = Video(
            bvid=info["bvid"],
            aid=info["aid"],
            title=info["title"],
            pic=info["pic"],
            description=info["description"],
            pubdate=info["pubdate"],
            duration=info["duration"],
            view_count=info["view_count"],
            danmaku_count=info["danmaku_count"],
            reply_count=info["reply_count"],
            favorite_count=info["favorite_count"],
            coin_count=info["coin_count"],
            share_count=info["share_count"],
            like_count=info["like_count"],
            dislike_count=info["dislike_count"],
            uploader=uploader
        )
        video.save()
    else:
        video = Video.objects.get(bvid=info["bvid"])
        video.uploader = uploader
    for pagedict in info["pages"]:
        if len(Page.objects.filter(cid=pagedict["cid"])) <= 0:
            videoinfo=video_base.get_video_file(bvid=info["bvid"], cid=pagedict["cid"], aid=info["aid"])
            path = videoinfo["file_path"]
            page = Page(
                video=video,
                cid=pagedict["cid"],
                page=pagedict["page"],
                part=pagedict["part"],
                path=path
            )
            page.save()


def __test__(bvid):
    info = video_base.get_video_info(bvid)
    videowrite(info)
    aid = info['aid']
    pages = info["pages"]
    for page in pages:
        cid = page["cid"]
        danmaku = video_base.get_danmaku(cid=cid)
        danmakuwrite(data=danmaku, cid=cid)
    i = 1
    flag = 1
    while True:
        commentpage = video_base.get_comment(aid=aid, page=i)
        comment_page_count, remainder = divmod(commentpage["all_count"], 20)
        if remainder > 0:
            comment_page_count += 1
        commentwrite(commentpage)
        time.sleep(2)
        is_end = commentpage['is_end']
        if is_end:
            print(f'爬取完成,实际爬取{i-1}页')
            break
        if flag > random.randint(5, 10):
            sle = random.randint(5, flag)
            flag = 0
            print(f'预计爬取{comment_page_count}页,已爬取{i}页,暂停{sle}秒')
            time.sleep(sle)
        i += 1
        flag += 1

    return "ok"
