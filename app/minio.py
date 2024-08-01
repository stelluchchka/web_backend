from minio import Minio
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import *

def process_file_upload(file_object: InMemoryUploadedFile, client, image_name):
    try:
        client.put_object('img', image_name, file_object, file_object.size)
        return f"http://localhost:9000/img/{image_name}"
    except Exception as e:
        return {"error": str(e)}

def add_pic(new_dish, pic, chef):
    client = Minio(endpoint="localhost:9000",
                   access_key='minioadmin',
                   secret_key='minioadmin',
                   secure=False)
    i = new_dish.id-1

    if chef == 1:
        img_obj_name = f"chef{i}.png"
    else:
        img_obj_name = f"{i}.png"

    if not pic:
        if chef == 1:
            return Response({"error": "Нет файла для изображения повара."})
        else:
            return Response({"error": "Нет файла для изображения блюда."})
    result = process_file_upload(pic, client, img_obj_name)
    if 'error' in result:
        return Response(result)

    if chef == 1:
        new_dish.chef_url = result
    else:
        new_dish.url = result

    new_dish.save()
    return Response({"message": "success"})