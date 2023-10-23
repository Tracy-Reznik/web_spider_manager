import io
from xmlrpc.client import ResponseError

import django
from django.core.files.base import ContentFile
from minio import Minio, S3Error

from SpiderManager.settings import MINIO

minio_client = Minio(MINIO["SERVER"], access_key=MINIO["USER"], secret_key=MINIO["PASS"], secure=False)

bucket_name = MINIO["BUCKET"]


# 以django File对象的形式上传文件，用于前端文件上传至minio的情景
def upload_fileByDjangoFile(file_path: str, filedata: django.core.files.File):
    """
        文件上传函数，将文件以 Django File 对象形式上传到 MinIO 桶。

        Args:
            file_path (str): 文件在 MinIO 中的路径。
            filedata (django.core.files.File): 要上传的文件对象。

        Returns:
            dict: 包含上传结果的字典，包括 'code' 和 'message'。状态码可能有 200、500。

                状态码 200：表示上传成功
                状态码 500：表示上传错误
    """
    try:
        with filedata.open('rb') as file:
            # 读取文件内容并写入BytesIO对象
            bytes_io = io.BytesIO(file.read())
        minio_client.put_object(
            bucket_name,
            file_path,
            bytes_io,
            length=filedata.size,
            content_type=filedata.content_type
        )
        code = 200  # 正确上传
        message = "ok"
        print(f'File {file_path} uploaded successfully.')
    except ResponseError as err:
        code = 500  # 上传发生错误
        message = f'Error uploading file: {err}'
        print(message)
    return {"code": code, "message": message}


# 以BytesIO对象方式上传，适用于将数据处理过程后或者从外部下载后得到的内存文件上传至minio的情景
def upload_fileByBytesIO(file_path: str, filedata: io.BytesIO, contect_type: str):
    """
        文件上传函数，将文件以 BytesIO流对象形式上传到 MinIO 桶。

        Args:
            file_path (str): 文件在 MinIO 中的路径。
            filedata (io.BytesIO): 要上传的文件对象。
            contect_type (str) 文件mime

        Returns:
            dict: 包含上传结果的字典，包括 'code' 和 'message'。状态码可能有 200、500。
                状态码 200：表示上传成功
                状态码 500：表示上传错误
    """
    try:
        minio_client.put_object(
            bucket_name,
            object_name=file_path,
            data=filedata,
            length=len(filedata.getvalue()),
            content_type=contect_type
        )
        code = 200  # 正确上传
        message = "ok"
        print(f'File {file_path} uploaded successfully.')
    except ResponseError as err:
        message = f'Error uploading file: {err}'
        code = 500  # 上传发生错误
        print(message)
    return {"code": code, "message": message}


# 下载MinIO桶中的文件
def download_file(file_path):
    """
        文件下载函数，从 MinIO 桶中下载文件。

        Args:
            file_path (str): 要下载的文件在 MinIO 中的路径。

        Returns:
            dict: 包含下载结果的字典，包括 'code'、'message'、'mime' 和 'data'。状态码可能有 200、404、500。

                状态码 200：表示下载成功，还包含 'mime' 和 'data' 字段。
                状态码 404：表示文件未找到错误。
                状态码 500：表示下载错误。
    """
    reqdict = {}
    try:
        file = minio_client.get_object(bucket_name, file_path)
        print(f'File {file_path} downloaded successfully.')
        reqdict["code"] = 200
        reqdict["message"] = "ok"
        reqdict["mime"] = file.headers.get('content-type')
        reqdict["data"] = file.data
    except ResponseError as err:
        print(f'Error downloading file: {err}')
        reqdict["code"] = 500
        reqdict["message"] = f'Error downloading file: {err}'
    except S3Error as err:
        print(f'Error downloading file: {err}')
        reqdict["code"] = 404
        reqdict["message"] = f'Error downloading file: {err}'
    return reqdict


# 删除MinIO桶中的文件
def delete_file(file_path):
    """
       文件删除函数，删除 MinIO 桶中的文件。

       Args:
           file_path (str): 要删除的文件在 MinIO 中的路径。

       Returns:
           dict: 包含删除结果的字典，包括 'code' 和 'message'。状态码可能有 200、404、500。

               状态码 200：表示删除成功。
               状态码 404：表示文件未找到错误。
               状态码 500：表示删除错误。
    """
    reqdict = {}
    try:
        minio_client.remove_object(bucket_name, file_path)
        print(f'File {file_path} deleted successfully.')
        reqdict["code"] = 200
        reqdict["message"] = "ok"
    except ResponseError as err:
        print(f'Error deleting file: {err}')
        reqdict["code"] = 500
        reqdict["message"] = f'Error deleting file: {err}'
    except S3Error as err:
        print(f'Error deleting file: {err}')
        reqdict["code"] = 404
        reqdict["message"] = f'Error deleting file: {err}'
    return reqdict
