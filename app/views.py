# import psycopg2
# from psycopg2 import sql
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from app.serializers import *
from app.models import *

# class DishViewSet(viewsets.ModelViewSet):
#     queryset = Dishes.objects.all()
#     serializer_class = DishSerializer


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

#Orders

@api_view(['GET'])
def GetOrders(request):
    order = Orders.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def PostOrders(request):
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(f"Данные недействительны")
    serializer.save()
    order = Orders.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

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

@api_view(['DELETE']) #не работает 
def DeleteDishesOrders(request, pk):
    if not DishesOrders.objects.filter(id=pk).exists():
        return Response(f"Связи м-м с таким id нет?")

    dishes_orders = DishesOrders.objects.get(id=pk)
    dishes_orders.delete()
    dishes_orders.save()

    dishes_orders = DishesOrders.objects.all()
    serializer = DishOrderSerializer(dishes_orders, many=True)
    return Response(serializer.data)
