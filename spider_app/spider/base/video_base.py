import hashlib
import json
import random
import time
import uuid
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import minio_connect
from SpiderManager import settings
from spider_app.spider.base import get_pictures

ua = UserAgent()
cookies = {
    "buvid3": "{}{:05d}infoc".format(uuid.uuid4(), random.randint(1, 99999))
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Origin': 'https://www.bilibili.com',
    'Referer': 'https://www.bilibili.com/',
    'User-Agent': ua.random,
    'Connection': 'close'
}  # 爬虫模拟访问信息
proxies = settings.PROXIES


def get_play_list(cid, quality=80):
    """
    视频链接爬取函数，用于获取视频的真实流地址。
    Args:
        cid：视频分页的cid
        quality：分辨率，默认为80（1080p）
    Return：
        dict:{
            format:mime类型
            urls:[
                视频url列表
            ]
        }
    """
    headers['User-Agent'] = ua.random
    cookies['buvid3'] = "{}{:05d}infoc".format(uuid.uuid4(), random.randint(1, 99999))
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    # print(url_api)
    html = requests.get(url_api, headers=headers, cookies=cookies, proxies=proxies).json()
    # print(html)
    # print(json.dumps(html))
    formatinfo = html['format']
    video_list = []
    for i in html['durl']:
        video_list.append(i['url'])
    # print(video_list)
    return {
        'format': formatinfo,
        'urls': video_list
    }


# def get_video_url(bvid: str, page: int):
#
#     response = requests.get(url=f"https://www.bilibili.com/video/{bvid}/?p={page}", headers=headers,cookies=cookies,
#                             proxies=proxies)
#     if response.status_code == 200:
#         bs = BeautifulSoup(response.text, 'html.parser')
#         # 取视频标题
#         # print(bs.find('span', class_='tit'))
#         # video_title = bs.find('span', class_='tit').get_text()
#
#         # 取视频链接
#         pattern = re.compile(r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL)
#         script = bs.find("script", text=pattern)
#         result = pattern.search(script.next).group(1)
#
#         temp = json.loads(result)
#
#         # 取第一个视频链接
#         urldict = {}
#         for item in temp['data']['dash']['video']:
#             if 'baseUrl' in item.keys():
#                 urldict['video_url'] = item['baseUrl']
#                 break
#         if 'audio' in temp['data']['dash']:
#             for item in temp['data']['dash']['audio']:
#                 if 'baseUrl' in item.keys():
#                     urldict['audio_url'] = item['baseUrl']
#                     break
#         return {
#             'code': 200,
#             'message': 'ok',
#             'url': urldict
#         }


def get_video_file(bvid: str, cid, aid):
    """
    视频文件下载函数，用于下载视频文件。
    Args:
        bvid：视频的bv号
        cid：视频分页id
        aid：视频av号
    Return:
        dict：{
                'code': 状态码 可能有200，400，500，501,
                'message': 函数消息,

            }
            状态码200：表示函数顺利运行，函数除基本响应外还包含：
                file_path：文件在minio的存储地址
            状态码400：表示输入参数错误
            状态码500：表示minio错误
            状态码501：表示媒体下载错误
    """
    headers['User-Agent'] = ua.random
    cookies['buvid3'] = "{}{:05d}infoc".format(uuid.uuid4(), random.randint(1, 99999))
    try:
        video_info = get_play_list(cid=cid)
        urls = video_info["urls"]
        formatinfo = video_info["format"]
        if formatinfo[:3] == "flv":
            formatinfo = "flv"
        # print(urls)
        # audio_response = requests.get(url=url["audio_url"], proxies=settings.PROXIES)
        # video_response = requests.get(url=url["video_url"], proxies=settings.PROXIES)
        # video_data = BytesIO(video_response.content)
        # audio_data = BytesIO(audio_response.content)
        minio_path = f"video/{bvid}/{cid}.{formatinfo}"
        # if "audio_url" in url:
        #     ffmpeg_cmd = [
        #         'ffmpeg',
        #         '-i', f'{url["video_url"]}',
        #         '-i', f'{url["audio_url"]}',  # 输入音频流
        #         '-headers', f'accept:{headers["accept"]};referer:{headers["referer"]};',
        #         '-c:v', 'copy', '-c:a', 'copy',  # 使用copy编码视频流，aac编码音频流
        #         '-f', 'mpegts', '-'
        #     ]
        # else:
        #     ffmpeg_cmd = [
        #         'ffmpeg',
        #         '-user_agent',headers["user-agent"],
        #         '-headers',f'accept:{headers["accept"]};referer:{headers["referer"]};user-agent:{headers["user-agent"]}',
        #         '-i', f'{url["video_url"]}',
        #         '-c:v', 'copy', '-c:a', 'copy',  # 使用copy编码视频流，aac编码音频流
        #         '-f', 'mpegts', '-'
        #     ]
        # # command_string = " ".join(shlex.quote(arg) for arg in ffmpeg_cmd)
        # # with open("command","w") as f:
        # #     f.write(command_string)
        # # print(command_string)
        # ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                                   stderr=subprocess.PIPE)
        #
        # output_data, err_info = ffmpeg_process.communicate()
        # print(err_info.decode("utf-8"))
        start_url = f"https://api.bilibili.com/x/web-interface/view?aid={aid}"
        video_headers = headers
        video_headers['Referer'] = start_url
        video_headers['Connection'] = 'keep-alive'
        mimes = {
            "mp4": "video/mp4",
            "flv": "video/x-flv",
        }
        response = requests.get(url=urls[0], headers=headers, cookies=cookies, proxies=proxies)
        output_data = response.content
        if len(output_data) > 0:
            data = BytesIO()
            data.write(output_data)
            info = minio_connect.upload_fileByBytesIO(
                contect_type=mimes[formatinfo],
                filedata=data,
                file_path=minio_path)
            info["file_path"] = minio_path
            return info
        else:
            info = {
                'code': 501,
                'message': 'media error'
            }
            return info
    except requests.RequestException:
        return {
            'code': 400,
            'message': 'bili argument error'
        }


def get_danmaku(cid):
    """
    弹幕爬取函数，用于爬取弹幕数据。
    Args:
        cid：视频分页的cid
    Return:
        list:[
            {
                "time": 弹幕出现时间，浮点数，单位是秒
                "mode": 弹幕模式，有8种类型
                "size": 弹幕字号
                "color": 弹幕颜色
                "timestamp": 弹幕发布时间，格式为yy-mm-dd h:m:s
                "type": 弹幕池类型
                "user-hash": 用户id的哈希值
                "danmaku_id": 弹幕id
                "text": 弹幕内容
            }
            # ...（以下为其他弹幕信息）
        ]
    """
    headers['User-Agent'] = ua.random
    cookies['buvid3'] = "{}{:05d}infoc".format(uuid.uuid4(), random.randint(1, 99999))
    data = []
    api = "https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"

    url = api.format(cid=cid)  # 拼接url
    html = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text)
    # print(soup.prettify())
    for d in soup.find_all(name="d"):
        p = d["p"].split(",")
        data.append({
            "time": p[0],  # 弹幕时间
            "mode": p[1],
            "size": p[2],
            "color": p[3],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(int(p[4]))),
            "type": p[5],
            "user-hash": p[6],
            "danmaku_id": p[7],
            "text": d.string
        })
    return data


def get_comment(aid, page):
    """
    评论爬取函数，用于爬取评论数据以及前三楼的回复信息。
    Args:
        aid：视频的av号,
        page: 评论分页页码
    Returns:
        dict:{
            "isEnd":boolean 是否是最后一页,
            "aid":视频的av号,
            "all_count":评论总数,
            "comment":[
                {
                    "rpid": 评论的rpid，唯一标识,
                    "location": ip地址,
                    "like": 点赞数,
                    "ctime": 评论发布时间,
                    "comment": 评论内容,
                    member:{
                        "uid": 用户uid,
                        "name": 用户名,
                        "sex": 用户性别,
                        "sign": 用户个性签名,
                        "face":头像url
                    },
                    "replies": [
                        {
                            "rpid": 回复的rpid，唯一标识,
                            member:{
                                "uid": 用户uid,
                            "name": 用户名,
                                "sex": 用户性别,
                                "sign": 用户个性签名,
                                "face":头像url
                            },
                            "location": ip地址,
                            "like": 点赞数,
                            "ctime": 评论发布时间,
                            "comment": 回复内容,
                        }
                        # ...（以下为其他回复信息）
                    ]
                }
                # ...（以下为其他评论及回复信息）
            ]
        }
    """

    def get_comment_page(aid, i):
        is_end = False
        headers['User-Agent'] = ua.random
        cookies['buvid3'] = "{}{:05d}infoc".format(uuid.uuid4(), random.randint(1, 99999))

        url = f'https://api.bilibili.com/x/v2/reply?&mode=3&pn={i}&oid={aid}&plat=1&type=1'
        print(url)
        response = requests.get(url, proxies=proxies, headers=headers)
        response.encoding = 'utf-8'
        json_data = json.loads(response.text)  # 获取评论的json数据
        if 'data' not in json_data:
            return None, None, None, json_data

        if 'acount' in json_data['data']['page']:
            all_count = json_data['data']['page']['acount']
        else:
            all_count = 0
        data_s = json_data['data']['replies']  # 筛选出评论数据具体信息

        #print(data_s)
        result = []  # 创建一个空列表，用于放评论的各种信息
        if data_s is not None and data_s != []:
            for data in data_s:
                comment = data['content']['message']  # 评论内容
                # print(comment)
                rpid = data['rpid']  # 评论id
                uid = data['mid']  # 评论人员uid
                name = data['member']['uname']  # 评论人员用户名
                sex = data['member']['sex']  # 评论人员性别
                sign = data['member']['sign']  # 评论人员个性签名
                face = data['member']['avatar']  # 评论人员头像
                like = data['like']  # 点赞数
                ctime = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(data['ctime']))  # 发布时间
                try:
                    location = data['reply_control']['location']  # 评论时所在的属地
                except:
                    location = '评论时尚未有ip属地功能'

                replies = []
                if data['replies'] is not None:
                    for reply in data['replies']:
                        reply_comment = reply['content']['message']  # 评论内容
                        # print(comment)
                        reply_rpid = reply['rpid']  # 评论id
                        reply_uid = reply['mid']  # 评论人员uid
                        reply_name = reply['member']['uname']  # 评论人员用户名
                        reply_sex = reply['member']['sex']  # 评论人员性别
                        reply_sign = reply['member']['sign']  # 评论人员个性签名
                        reply_face = data['member']['avatar']  # 评论人员头像
                        reply_like = reply['like']  # 点赞数
                        reply_ctime = time.strftime("%Y-%m-%d %H:%M:%S",
                                                    time.localtime(reply['ctime']))  # 发布时间
                        try:
                            reply_location = data['reply_control']['location']  # 评论时所在的属地
                        except:
                            reply_location = '评论时尚未有ip属地功能'
                        replies.append(dict(rpid=reply_rpid,
                                            location=reply_location, like=reply_like,
                                            ctime=reply_ctime, comment=reply_comment,
                                            member=dict(uid=reply_uid, name=reply_name, sex=reply_sex, sign=reply_sign,
                                                        face=reply_face)))
                person = dict(rpid=rpid, location=location, like=like,
                              ctime=ctime, comment=comment,
                              member=dict(uid=uid, name=name, sex=sex, sign=sign, face=face),
                              replies=replies)
                result.append(person)
        else:
            data_s = []  # 用于终止循环
            result = data_s
            is_end = True
        return all_count, result, is_end, None

    def arrange_comment(aid, page=1):
        while True:
            count_length, comment, is_end, jsondata = get_comment_page(aid, page)
            if jsondata:
                print('爬取异常，正在尝试重新爬取')
                print(jsondata)
                time.sleep(5)
            else:
                break
        return {
            'all_count': count_length,
            'is_end': is_end,
            'aid': aid,
            'comment': comment
        }

    return arrange_comment(aid=aid, page=page)


def get_video_info(bvid):
    """
    视频信息爬取函数，用于抓取视频的各种数据信息。
    Args:
        bvid(str)：视频的bv号
    Returns:
        dict:{
            "bvid": 视频的Bilibili BV号
            "aid": 视频的aid（另一种唯一标识符）
            "title": 视频标题
            "pic": 视频封面
            "description": 视频描述
            "pubdate": 视频的发布时间戳
            "duration": 视频时长（秒）
            "view_count": 视频观看次数
            "danmaku_count": 视频弹幕数量
            "reply_count": 视频评论数
            "favorite_count": 视频收藏数
            "coin_count": 视频硬币数（投币数）
            "share_count": 视频分享数
            "like_count": 视频点赞数
            "dislike_count": 视频点踩数
            "uploader": {
                "uid": 用户uid,
                "name": 用户名,
                "sex": 用户性别,
                "sign": 用户个性签名,
                "face":头像url
            },
            "pages": [
                {
                    "cid": 分页视频标记id
                    "page": 页码
                    "part": 分页视频标题
                }
                # ...（以下为其他分页信息）
            ]
        }
    """
    headers['User-Agent'] = ua.random
    cookies['buvid3'] = "{}{:05d}infoc".format(uuid.uuid4(), random.randint(1, 99999))
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    response = requests.get(url=url, proxies=proxies, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        data = json.loads(response.text)
        # 解析JSON数据，提取视频信息并构建字典
        pages = []
        for page in data["data"]["pages"]:
            pages.append({
                "cid": page["cid"],  # 分页视频标记id
                "page": page["page"],  # 页码
                "part": page["part"],  # 分页视频标题
            })
        uploaderdata = json.loads(requests.get(
            "https://api.bilibili.com/x/web-interface/card?mid={}".format(data["data"]["owner"]["mid"]),
            headers=headers, cookies=cookies,
            proxies=proxies
        ).text)["data"]["card"]
        print(uploaderdata)
        video_info = {
            "bvid": data["data"]["bvid"],  # 视频的Bilibili BV号
            "aid": data["data"]["aid"],  # 视频的aid（另一种唯一标识符）
            "title": data["data"]["title"],  # 视频标题
            "pic": get_pictures(data["data"]["pic"]),  # 视频封面
            "description": data["data"]["desc"],  # 视频描述
            "pubdate": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data["data"]["pubdate"])),  # 视频的发布时间戳
            "duration": data["data"]["duration"],  # 视频时长（秒）
            "view_count": data["data"]["stat"]["view"],  # 视频观看次数
            "danmaku_count": data["data"]["stat"]["danmaku"],  # 视频弹幕数量
            "reply_count": data["data"]["stat"]["reply"],  # 视频评论数
            "favorite_count": data["data"]["stat"]["favorite"],  # 视频收藏数
            "coin_count": data["data"]["stat"]["coin"],  # 视频硬币数（投币数）
            "share_count": data["data"]["stat"]["share"],  # 视频分享数
            "like_count": data["data"]["stat"]["like"],  # 视频点赞数
            "dislike_count": data["data"]["stat"]["dislike"],  # 视频点踩数
            "uploader": {
                "uid": uploaderdata["mid"],
                "name": uploaderdata["name"],
                "sex": uploaderdata["sex"],
                "sign": uploaderdata["sign"],
                "face": uploaderdata["face"]
            },
            "pages": pages  # 视频分页信息
            # 这里可以继续添加其他信息
        }
        return video_info
    else:
        return None


# 测试
if __name__ == "__main__":
    bvid = "BV1kx411S7L2"
    info = get_video_info(bvid)
    comment = []
    danmaku = {}
    for i in range(len(info["pages"])):
        page = info["pages"][i]
        danmaku[page["page"]] = get_danmaku(page["cid"])
        videodata = get_video_file(bvid=bvid, cid=page["cid"], aid=info["aid"])
        info["pages"][i]["path"] = videodata["file_path"]
        time.sleep(10)
    is_end = False
    i = 1
    while not is_end:
        commentdata = get_comment(info["aid"], page=i)
        comment += commentdata["comment"]
        is_end = commentdata["is_end"]
        i += 1
    data = {
        "info": info,
        "danmaku": danmaku,
        "comment": comment
    }
    with open(f"{bvid}.json", "w") as f:
        f.write(json.dumps(data))
