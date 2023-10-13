from django.shortcuts import *
from rest_framework.decorators import api_view
from rest_framework.response import *
from rest_framework.status import *
# from rest_framework import viewsets
from app.serializers import *
from app.models import *
from minio import Minio
from datetime import datetime

user = Users(id=1, name="User", email="a", password=1234, role="user", login="aa")

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Orders.objects.all()
#     serializer_class = OrderSerializer


#Dishes
@api_view(['GET'])                               # все блюда
def GetDishes(request):
    dish = Dishes.objects.filter(status="есть")
    serializer = DishSerializer(dish, many=True)
    return Response(serializer.data)

@api_view(['POST'])                              # добавить блюдо
def PostDishes(request):
    serializer = DishSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()
    print(serializer.data)
    new_dish = Dishes.objects.create(serializer.data)
    #картинки выгрузить в minio и в поле в бд внести адрес к этому объекту в хранилище
    client = Minio(endpoint="localhost:9000",
                access_key='minioadmin',
                secret_key='minioadmin',
                secure=False)
    i=new_dish.id-1
    client.fput_object(bucket_name='img', 
                    object_name=f"{i}.png",
                    file_path=request.data["url"])
    client.fput_object(bucket_name='img', 
                    object_name=f"chef{i}.png",
                    file_path=request.data["chef_url"])
    new_dish.url=f"/Users/stella/projects/web_backend/sources/img/{i}.png"
    new_dish.chef_url=f"/Users/stella/projects/web_backend/sources/img/chef{i}.png"


    dish = Dishes.objects.filter(status="есть")
    serializer = DishSerializer(dish, many=True)
    return Response(serializer.data)

@api_view(['GET'])                                 # 1 блюдо
def GetDish(request, pk):
    if not Dishes.objects.filter(id=pk).exists():
        return Response(f"Блюда с таким id нет")

    dish = Dishes.objects.get(id=pk)
    serializer = DishSerializer(dish)
    return Response(serializer.data)

@api_view(['DELETE'])                              # удалить блюдо
def DeleteDish(request, pk):
    if not Dishes.objects.filter(id=pk).exists():
        return Response(f"Блюда с таким id нет")
    dish = Dishes.objects.get(id=pk)
    dish.status = "удаленo"
    dish.save()

    dish = Dishes.objects.filter(status="есть")
    serializer = DishSerializer(dish, many=True)
    return Response(serializer.data)

@api_view(['PUT'])                                 # изменить блюдо
def PutDish(request, pk):
    try:
        dish = Dishes.objects.get(id=pk)
    except Dishes.DoesNotExist:
        return Response("Блюда с таким id нет")

    serializer = DishSerializer(dish, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        dish = Dishes.objects.filter(status="есть")
        serializer = DishSerializer(dish, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['POST'])                                 # добавить блюдо в заказ
def PostDishToOrder(request, pk):
    quantity = int(request.data.get('quantity'))
    try: 
        order=Orders.objects.filter(user=user, status="зарегистрирован").latest('created_at') # заказ определенного пользователя
    except:
        order = Orders(                              # если нет, создаем новый заказ
            status='зарегистрирован',
            created_at=datetime.now(),
            user=user,
        )
        order.save()

    order_id=order.id
    dish_id=pk
    try:
        dish_order=DishesOrders.objects.get(order_id=order_id, dish_id=dish_id) #проверка есть ли такая м-м
        dish_order.quantity=dish_order.quantity+quantity      # если да, не создаем новую а меняем существующую
        dish_order.save()
    except:
        dish_order = DishesOrders(                            # если нет, создаем м-м
            order_id=order_id,
            dish_id=dish_id,
            quantity=quantity
        )
        dish_order.save()

    # dishes_orders = DishesOrders.objects.all()  # выводим все м-м
    # serializer = DishOrderSerializer(dishes_orders, many=True)
    orders = Orders.objects.all()  # выводим все заказы
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

#Orders

@api_view(['GET'])                                  # все заказы
def GetOrders(request):
    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get('start', '2023-01-01')
    end_date_str = request.query_params.get('end', '2023-12-31')
    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()
    orders = Orders.objects.filter(created_at__range=(start, end)).order_by('created_at')
    serializer = OrderSerializer(orders, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])                                  # 1 заказ
def GetOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")

    order = Orders.objects.get(id=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['DELETE'])                               # удалить заказ?
def DeleteOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")
    order = Orders.objects.get(id=pk)
    order.status = "отказ"
    order.save()

    order = Orders.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

@api_view(['PUT'])                                  # изменить заказ
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

@api_view(['PUT'])                                  # статусы админа
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
        return Response("Такого заказа не зарегистрировано")
    if request.data["status"] not in ["отменен", "сформирован"]:
        return Response("Ошибка")

    order.status = request.data["status"]
    order.processed_at=datetime.now()
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data)


#Dishes-Orders
@api_view(['PUT'])                                  # изменение м-м(кол-во)
def PutDishesOrders(request, pk):
    if not DishesOrders.objects.filter(id=pk).exists():
        return Response(f"Связи м-м с таким id нет?")

    dishes_orders = DishesOrders.objects.get(id=pk)
    dishes_orders.quantity = request.data["quantity"]
    dishes_orders.save()

    dishes_orders = DishesOrders.objects.all()
    serializer = DishOrderSerializer(dishes_orders, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])                                # удаление м-м
def DeleteDishesOrders(request, pk):
    if not DishesOrders.objects.filter(id=pk).exists():
        return Response(f"Связи м-м с таким id нет?")

    dishes_orders = get_object_or_404(DishesOrders, id=pk)
    dishes_orders.delete()

    dishes_orders = DishesOrders.objects.all()
    serializer = DishOrderSerializer(dishes_orders, many=True)
    return Response(serializer.data)
