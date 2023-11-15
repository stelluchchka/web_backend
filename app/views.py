from app.serializers import *
from app.models import *
from app.permissions import IsManager, IsAdmin
from app.minio import add_pic

from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from django.http import HttpResponse

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import *
from rest_framework.status import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView

user = Users(id=1, name="User", email="a", password=1234, role="user", login="aa")
moderator = Users(id=2, name="mod", email="b", password=12345, role="moderator", login="bb")

@permission_classes([AllowAny])
@authentication_classes([])
def login_view(request):
    email = request.POST["email"] # передали email и password
    password = request.POST["password"]
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("{'status': 'ok'}")
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")

@permission_classes([AllowAny])
@authentication_classes([])
def logout_view(request):
    logout(request._request)
    return Response({'status': 'Success'})




class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer
    model_class = AuthUser

    def create(self, request):
        # Если пользователя c указанным в request email ещё нет, в БД будет добавлен новый пользователь.
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data) #?
        if serializer.is_valid():
            print(serializer.data)
            self.model_class.objects.create_user(first_name=serializer.data['first_name'],
                                     username=serializer.data['username'],             
                                     last_name=serializer.data['last_name'],            
                                     email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAdmin | IsManager]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class DishesViewSet(APIView):
    model_class = Dishes
    serializer_class = DishSerializer

    def get(self, request, format=None):
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
        dish_serializer = self.serializer_class(dish, many=True)
        # заказ определенного пользователя
        try: 
            order=Orders.objects.filter(user=user, status="зарегистрирован").latest('created_at')
            order_serializer = OrderSerializer(order)
            return Response({
                'order': order_serializer.data,
                'dishes': dish_serializer.data
        })
        # заказа-черновика нет
        except:
            return Response({
                'order': [],
                'dishes': dish_serializer.data
        })

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
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

        # dish = Dishes.objects.filter(status="есть")
        serializer = self.serializer_class(new_dish)
        return Response(serializer.data)


class DishViewSet(APIView):
    model_class = Dishes
    serializer_class = DishSerializer

    def  get(self, request, pk, format=None):                                 # 1 блюдо
        if not Dishes.objects.filter(id=pk, status="есть").exists():
            return Response(f"Такого блюда нет")

        dish = Dishes.objects.get(id=pk)
        serializer = self.serializer_class(dish)
        return Response(serializer.data)

    def  delete(self, request, pk, format=None):                              # удалить блюдо
        if not Dishes.objects.filter(id=pk, status="есть").exists():
            return Response(f"Такого блюда нет")
        dish = Dishes.objects.get(id=pk)
        dish.status = "удаленo"
        dish.save()
        # dish = Dishes.objects.filter(status="есть")
        # serializer = self.serializer_class(dish, many=True)
        return Response({"message": "success"})

    def  put(self, request, pk, format=None):                                 # изменить блюдо
        try:
            dish = Dishes.objects.get(id=pk, status="есть")
        except Dishes.DoesNotExist:
            return Response("Блюда с таким id нет")

        serializer = self.serializer_class(dish, data=request.data, partial=True)

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
            serializer = self.serializer_class(dish)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class OrdersViewSet(APIView):
    model_class = Orders
    serializer_class = OrderSerializer

    @permission_classes([IsManager])
    def get(self, request, format=None):                                  # все заказы
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
        serializer = self.serializer_class(orders, many=True)
        
        return Response(serializer.data)


class OrderViewSet(APIView):
    model_class = Orders
    serializer_class = FullOrderSerializer

    def  get(self, request, pk, format=None):                      # 1 заказ
        try:
            order = Orders.objects.get(id=pk)
        except Orders.DoesNotExist:
            return Response(f"Заказа с таким id нет")

        serializer = self.serializer_class(order)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):                      # удалить заказ
        if not Orders.objects.filter(id=pk).exists():
            return Response(f"Заказа с таким id нет")
        order = Orders.objects.get(id=pk)
        order.status = "отменен"
        order.save()
        # order = Orders.objects.all()
        # serializer = OrderSerializer(order, many=True)
        return Response({"status": "success"})


class DishesOrdersViewSet(APIView):
    model_class = DishesOrders
    serializer_class = DishOrderSerializer

    def put(self, request, pk, format=None):                   # изменение м-м(кол-во), передаем id заказа
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
        serializer = self.serializer_class(dishes_orders, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):                 # удаление м-м, передаем id заказа
        try: 
            order=Orders.objects.get(user=user, status="зарегистрирован", id=pk) # заказ определенного пользователя
        except:
            return Response("нет такого заказа")
        if not DishesOrders.objects.filter(order=order.id).exists():
            return Response(f"в заказе нет блюд")

        dishes_orders = get_object_or_404(DishesOrders, id=pk)
        dishes_orders.delete()

        dishes_orders = DishesOrders.objects.all()
        serializer = self.serializer_class(dishes_orders, many=True)
        return Response(serializer.data)




# Dishes
@swagger_auto_schema(method='post', request_body=OrderSerializer)
@permission_classes([IsAuthenticated])
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
@swagger_auto_schema(method='put', request_body=OrderSerializer)
@permission_classes([IsManager])
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

@swagger_auto_schema(method='put', request_body=OrderSerializer)
@permission_classes([IsAuthenticated])
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

