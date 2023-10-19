import hashlib
from io import BytesIO

import requests

import minio_connect
from SpiderManager import settings
import random
from fake_useragent import UserAgent




headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Origin': 'https://www.bilibili.com',
    'Referer': 'https://www.bilibili.com/',
    'user-agent': UserAgent().random,
}  # 爬虫模拟访问信息
proxies = settings.PROXIES


def get_pictures(url):
    mime_to_extension = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/bmp': '.bmp',
        'image/webp': '.webp',
        'image/tiff': '.tiff',
        'image/x-icon': '.ico',
    }

    def calculate_hashes(data):
        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()

        md5_hash.update(data)
        sha256_hash.update(data)

        md5_digest = md5_hash.hexdigest()
        sha256_digest = sha256_hash.hexdigest()

        return md5_digest, sha256_digest

    try:
        data = BytesIO()
        response = requests.get(url=url, headers=headers, proxies=proxies)
        md5, sha256 = calculate_hashes(response.content)
        data.write(response.content)
        mime = response.headers.get("Content-Type")
        if mime in mime_to_extension:
            extension = mime_to_extension[mime]
        else:
            extension = ".imgdata"
        filepath = f"pic/spider/bili/{md5}/{sha256}{extension}"
        minio_connect.upload_fileByBytesIO(file_path=filepath, filedata=data,
                                           contect_type=mime)
        return filepath
    except:
        print("图片下载错误")
        return ""
