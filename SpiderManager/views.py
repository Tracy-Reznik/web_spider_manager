from io import BytesIO

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import minio_connect
from spider_app.spider import dbwrite

from spider_app.spider.run.run import run_video_task


def dowmload_test(request, filepath):
    info = minio_connect.download_file(file_path=filepath)
    if info["code"] == 200:
        response = HttpResponse(info.get("data"), content_type=info.get("mime"))
    else:
        response = JsonResponse(info, status=info["code"])
    return response


def delete_test(request):
    info = minio_connect.delete_file(file_path=request.GET["filepath"])
    response = JsonResponse(info, status=200)
    return response


def index(request):
    return render(request, 'index.html', context={
        'title': 'Web Spider Manager'
    })


def upd_test(request):
    file = request.FILES["file"]
    info = minio_connect.upload_fileByDjangoFile(filedata=file, file_path="/test/" + file.name)
    return JsonResponse(info)


def upd_ByetsIO_test(request):
    url = request.GET["url"]
    respdata = requests.get(url=url, proxies={
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    })

    data = BytesIO()
    data.write(respdata.content)
    info = minio_connect.upload_fileByBytesIO(contect_type=respdata.headers.get("Content-Type"), filedata=data,
                                              file_path="test/{filename}".format(
                                                  filename=url.split("/")[-1].split("?")[0]))
    return JsonResponse(info)


def spider_test(request):
    bvid = request.GET["bvid"]
    return JsonResponse(dict(message=dbwrite.__test__(bvid=bvid)))
