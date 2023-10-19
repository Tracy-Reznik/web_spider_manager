

from spider_app.spider.base import video_base


def get_video_data(config: dict):
    bvid = config["bvid"]
    info = video_base.get_video_info(bvid)
    danmaku = {}
    for page in info["pages"]:
        danmaku[page["cid"]] = video_base.get_danmaku(page["cid"])
        print(video_base.get_video_file(bvid=bvid, aid=info["aid"],cid=page["cid"]))
    comment = video_base.get_comment(info["aid"])

