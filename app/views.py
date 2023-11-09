from django.shortcuts import *
from rest_framework.decorators import api_view
from rest_framework.response import *
from rest_framework.status import *
# from rest_framework import viewsets
from app.serializers import *
from app.models import *
from minio import Minio
from datetime import datetime
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile


user = Users(id=1, name="User", email="a", password=1234, role="user", login="aa")
moderator = Users(id=2, name="mod", email="b", password=12345, role="moderator", login="bb")

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Orders.objects.all()
#     serializer_class = OrderSerializer

def process_file_upload(file_object: InMemoryUploadedFile, client, image_name):
    try:
        client.put_object('img', image_name, file_object, file_object.size)
        return f"http://localhost:9000/img/{image_name}"
    except Exception as e:
        return {"error": str(e)}

# def add_pics(new_dish, request):
#     client = Minio(endpoint="localhost:9000",
#                    access_key='minioadmin',
#                    secret_key='minioadmin',
#                    secure=False)
#     i = new_dish.id-1

#     # pic
#     img_obj_name = f"{i}.png"
#     dish_pic = request.FILES.get("pic")
#     if not dish_pic:
#         return Response({"error": "Нет файла для изображения блюда."})
#     result = process_file_upload(dish_pic, client, img_obj_name)
#     if 'error' in result:
#         return Response(result)
#     new_dish.url = result
    
#     # chef_pic
#     chef_img_obj_name = f"chef{i}.png"
#     chef_pic = request.FILES.get("chef_pic")
#     if not chef_pic:
#         return Response({"error": "Нет файла для изображения шеф-повара."})
#     result = process_file_upload(chef_pic, client, chef_img_obj_name)
#     if 'error' in result:
#         return Response(result)
#     new_dish.chef_url = result
    
#     # Сохраняем данные блюда 
#     new_dish.save()
#     return Response({"success"})


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


#Dishes
@api_view(['GET'])                               # все блюда
def GetDishes(request):
    try: 
        order=Orders.objects.filter(user=user, status="зарегистрирован").latest('created_at') # заказ определенного пользователя
        order_serializer = OrderSerializer(order)
        print(order_serializer)
    except:
        order_serializer=[]                     #!!!!!!!!!!error!!

    min_price = request.query_params.get("min_price", '0')
    max_price = request.query_params.get("max_price", '10000000')
    tag = request.query_params.get("tag", '')
    title = request.query_params.get("title", '')

    filters = Q(status="есть") & Q(price__range=(min_price, max_price))
    if tag != '':
        filters &= Q(tags=tag)
    if title != '':
        filters &= Q(title=title)

    dish = Dishes.objects.filter(filters)
    dish_serializer = DishSerializer(dish, many=True)
    return Response({
        'order': order_serializer.data,
        'dishes': dish_serializer.data
    })

@api_view(['POST'])                              # добавить блюдо
def PostDishes(request):
    serializer = DishSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    new_dish = serializer.save()

    # pic
    pic = request.FILES.get("pic")
    pic_result = add_pic(new_dish, pic, 0)
    if 'error' in pic_result.data:    # Если в результате вызова add_pic результат - ошибка, возвращаем его.
        return pic_result
    # chef_pic
    chef_pic = request.FILES.get("chef_pic")
    chef_pic_result = add_pic(new_dish, chef_pic, 1)
    if 'error' in chef_pic_result.data:    # Если в результате вызова add_pic результат - ошибка, возвращаем его.
        return chef_pic_result

    # pic_result = add_pics(new_dish, request)  # добавление сразу 2 картинок
    # if 'error' in pic_result.data:
    #     return pic_result

    # dish = Dishes.objects.filter(status="есть")
    serializer = DishSerializer(new_dish)
    return Response(serializer.data)

@api_view(['GET'])                                 # 1 блюдо
def GetDish(request, pk):
    if not Dishes.objects.filter(id=pk, status="есть").exists():
        return Response(f"Такого блюда нет")

    dish = Dishes.objects.get(id=pk)
    serializer = DishSerializer(dish)
    return Response(serializer.data)

@api_view(['DELETE'])                              # удалить блюдо
def DeleteDish(request, pk):
    if not Dishes.objects.filter(id=pk, status="есть").exists():
        return Response(f"Такого блюда нет")
    dish = Dishes.objects.get(id=pk)
    dish.status = "удаленo"
    dish.save()

    # dish = Dishes.objects.filter(status="есть")
    # serializer = DishSerializer(dish, many=True)
    return Response()

@api_view(['PUT'])                                 # изменить блюдо
def PutDish(request, pk):
    try:
        dish = Dishes.objects.get(id=pk, status="есть")
    except Dishes.DoesNotExist:
        return Response("Блюда с таким id нет")

    serializer = DishSerializer(dish, data=request.data, partial=True)

    if 'pic' in serializer.initial_data:
        pic_result = add_pic(dish, serializer.initial_data['pic'], 0)
        if 'error' in pic_result.data:
            return pic_result

    if 'chef_pic' in serializer.initial_data:
        pic_result = add_pic(dish, serializer.initial_data['chef_pic'], 1)
        if 'error' in pic_result.data:
            return pic_result

    if serializer.is_valid():
        serializer.save()
        # dish = Dishes.objects.filter(status="есть")
        dish = Dishes.objects.get(id=pk)
        serializer = DishSerializer(dish)

        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['POST'])                                  # добавить блюдо в заказ
def PostDishToOrder(request, pk):
    try: 
        order=Orders.objects.filter(user=user, status="зарегистрирован").latest('created_at') # заказ определенного пользователя
    except:
        order = Orders(                              # если нет, создаем новый заказ
            status='зарегистрирован',
            created_at=datetime.now(),
            user=user,
        )
        order.save()

    if not Dishes.objects.filter(id=pk, status="есть").exists():
        return Response(f"Такого блюда нет")

    order_id=order.id
    dish_id=pk
    try:
        dish_order=DishesOrders.objects.get(order_id=order_id, dish_id=dish_id) #проверка есть ли такая м-м
        dish_order.quantity=dish_order.quantity+1    # если да, не создаем новую а меняем существующую
        dish_order.save()
    except:
        dish_order = DishesOrders(                   # если нет, создаем м-м
            order_id=order_id,
            dish_id=dish_id,
            quantity=1
        )
        dish_order.save()

    # dishes_orders = DishesOrders.objects.all()  # выводим все м-м
    # serializer = DishOrderSerializer(dishes_orders, many=True)
    orders = Orders.objects.get(id=order_id)  # выводим 1 заказ
    serializer = OrderSerializer(orders)
    return Response(serializer.data)

#Orders

@api_view(['GET'])                                  # все заказы
def GetOrders(request):
    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get("start", '2000-01-01')
    end_date_str = request.query_params.get("end", '3023-12-31')
    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()
    status = request.query_params.get("status", '')
    filters = ~Q(status="отменен") & Q(created_at__range=(start, end))
    if status != '':
        filters &= Q(status=status)
        
    orders = Orders.objects.filter(filters).order_by('created_at')
    print(orders)
    serializer = OrderSerializer(orders, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])                                  # 1 заказ
def GetOrder(request, pk):
    try:
        order = Orders.objects.get(id=pk)
    except Orders.DoesNotExist:
        return Response(f"Заказа с таким id нет")

    serializer = FullOrderSerializer(order)
    return Response(serializer.data)

@api_view(['DELETE'])                               # удалить заказ
def DeleteOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")
    order = Orders.objects.get(id=pk)
    order.status = "отменен"
    order.save()

    # order = Orders.objects.all()
    # serializer = OrderSerializer(order, many=True)
    return Response()

# @api_view(['PUT'])                                  # изменить заказ(назначить модератора)
# def PutOrder(request, pk):
#     try:
#         order = Orders.objects.get(id=pk)
#     except Orders.DoesNotExist:
#         return Response("Заказа с таким id нет")
#     order.moderator=request.data["moderator"]
#     order.save()
#     order = Orders.objects.all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)

@api_view(['PUT'])                                  # статусы модератора
def ConfirmOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")

    order = Orders.objects.get(id=pk)

    if order.status != "сформирован":
        return Response("Такой заказ не сформирован")
    if request.data["status"] not in ["отказ", "готов"]:
        return Response("Ошибка")
    order.status = request.data["status"]
    order.completed_at=datetime.now()
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['PUT'])                                  # статусы пользователя
def ToOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")

    order = Orders.objects.get(id=pk)

    if order.status != "зарегистрирован":
        return Response(serializer.errors)
    if request.data["status"] not in ["отменен", "сформирован"]:
        return Response(serializer.errors)

    order.status = request.data["status"]
    order.processed_at=datetime.now()           #.strftime("%d.%m.%Y %H:%M:%S")
    order.moderator=moderator                   # назначаем модератора
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data)


#Dishes-Orders
@api_view(['PUT'])                                  # изменение м-м(кол-во)
def PutDishesOrders(request, pk):                   # передаем id заказа
    try: 
        order=Orders.objects.get(user=user, status="зарегистрирован", id=pk) # заказ определенного пользователя
    except:
        return Response("нет такого заказа")
    if not DishesOrders.objects.filter(order=order.id).exists():
        return Response(f"в заказе нет блюд")
    dishes_orders = DishesOrders.objects.get(id=pk)
    dishes_orders.quantity = request.data["quantity"]
    dishes_orders.save()

    dishes_orders = DishesOrders.objects.all()
    serializer = DishOrderSerializer(dishes_orders, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])                                # удаление м-м
def DeleteDishesOrders(request, pk):                 # передаем id заказа
    try: 
        order=Orders.objects.get(user=user, status="зарегистрирован", id=pk) # заказ определенного пользователя
    except:
        return Response("нет такого заказа")
    if not DishesOrders.objects.filter(order=order.id).exists():
        return Response(f"в заказе нет блюд")

    dishes_orders = get_object_or_404(DishesOrders, id=pk)
    dishes_orders.delete()

    dishes_orders = DishesOrders.objects.all()
    serializer = DishOrderSerializer(dishes_orders, many=True)
    return Response(serializer.data)
