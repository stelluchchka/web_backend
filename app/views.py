# import psycopg2
# from psycopg2 import sql
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from app.serializers import *
from app.models import *
from minio import Minio


# client = Minio(endpoint="localhost:9000",
#             access_key='minioadmin',
#             secret_key='minioadmin',
#             secure=False)
# for i in range(5):
#     client.fget_object(bucket_name='bucket', 
#                     object_name=f"img/{i}.png",
#                     file_path=f"/Users/stella/projects/web_backend/app/img/{i}.png")
# for i in range(5):
#     client.fget_object(bucket_name='bucket', 
#                     object_name=f"img/chef{i}.png",
#                     file_path=f"/Users/stella/projects/web_backend/app/img/chef{i}.png")



# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Orders.objects.all()
#     serializer_class = OrderSerializer


# class DishesOrdersViewSet(viewsets.ModelViewSet):
#     queryset = DishesOrders.objects.all()
#     serializer_class = DishOrderSerializer


#Dishes
@api_view(['GET'])
def GetDishes(request):
    dish = Dishes.objects.filter(status="enabled")
    serializer = DishSerializer(dish, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def PostDishes(request):
    serializer = DishSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(f"Данные недействительны")
    # картинки выгрузить в minio и в поле в бд внести адрес к этому объекту в хранилище
    # client = Minio(endpoint="localhost:9000",
    #             access_key='minioadmin',
    #             secret_key='minioadmin',
    #             secure=False)
    # client.fput_object(bucket_name='img', 
    #                 object_name=f"{i}.png",
    #                 file_path=request.url)
    # client.fput_object(bucket_name='img', 
    #                 object_name=f"chef{i}.png",
    #                 file_path=request.chef_url)
    # serializer.url=...
    # serializer.chef_url=...
    serializer.save()

    dish = Dishes.objects.filter(status="enabled")
    serializer = DishSerializer(dish, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetDish(request, pk):
    if not Dishes.objects.filter(id=pk).exists():
        return Response(f"Блюда с таким id нет")

    dish = Dishes.objects.get(id=pk)
    serializer = DishSerializer(dish)
    return Response(serializer.data)

@api_view(['DELETE'])
def DeleteDish(request, pk):
    if not Dishes.objects.filter(id=pk).exists():
        return Response(f"Блюда с таким id нет")
    dish = Dishes.objects.get(id=pk)
    dish.status = "deleted"
    dish.save()

    dish = Dishes.objects.filter(status="enabled")
    serializer = DishSerializer(dish, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def PutDish(request, pk):
    try:
        dish = Dishes.objects.get(id=pk)
    except Dishes.DoesNotExist:
        return Response("Блюда с таким id нет")

    serializer = DishSerializer(dish, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        dish = Dishes.objects.filter(status="enabled")
        serializer = DishSerializer(dish, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def AddDishToOrder(request, pk):

    serializer = OrderSerializer(status = "registered", processed_at = None, completed_at = None, user = None, moderator = None)
    if not serializer.is_valid():
        return Response(f"Данные недействительны")
    serializer.save()
    try:
        last_order = Orders.objects.filter(user=request.user).order_by('-created_at').first()

        if not last_order:
            return Response("У вас нет активных заказов.")

        dish_order = DishesOrders(order=last_order, dish_id=pk, quantity=request.quantity)
        dish_order.save()
        
        serializer = DishOrderSerializer(dish_order)
        return Response(serializer.data)
    except Dishes.DoesNotExist:
        return Response("Блюдо с указанным ID не найдено.")

#Orders

@api_view(['GET'])
def GetOrders(request):
    order = Orders.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# def PostOrders(request):
#     serializer = OrderSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response(f"Данные недействительны")
#     serializer.save()
#     order = Orders.objects.all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def GetOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")

    order = Orders.objects.get(id=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['DELETE'])
def DeleteOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")
    order = Orders.objects.get(id=pk)
    order.status = "удален"
    order.save()

    order = Orders.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def PutOrder(request, pk):
    try:
        order = Orders.objects.get(id=pk)
    except Orders.DoesNotExist:
        return Response("Заказа с таким id нет")
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()

    order = Orders.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def ConfirmOrder(request, pk):      #admin
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")

    order = Orders.objects.get(id=pk)
    order.status = request.data["status"]
    order.save()

    order = Orders.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def ToOrder(request, pk):        #user
    if not Orders.objects.filter(pk=id).exists():
        return Response(f"Заказа с таким id нет")

    order = Orders.objects.get(id=pk)
    order.status = request.data["status"]
    order.save()

    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)


#Dishes-Orders
@api_view(['PUT'])
def PutDishesOrders(request, pk):
    if not DishesOrders.objects.filter(id=pk).exists():
        return Response(f"Связи м-м с таким id нет?")

    dishes_orders = DishesOrders.objects.get(id=pk)
    dishes_orders.quantity = request.data["quantity"]
    dishes_orders.save()

    dishes_orders = DishesOrders.objects.all()
    serializer = DishOrderSerializer(dishes_orders, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def DeleteDishesOrders(request, pk):
    # if not DishesOrders.objects.filter(id=pk).exists():
    #     return Response(f"Связи м-м с таким id нет?")

    dishes_orders = get_object_or_404(DishesOrders, id=pk)
    dishes_orders.delete()

    dishes_orders = DishesOrders.objects.all()
    serializer = DishOrderSerializer(dishes_orders, many=True)
    return Response(serializer.data)
