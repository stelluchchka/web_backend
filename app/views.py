from app.serializers import *
from app.models import *
from app.permissions import IsManagerOrReadOnly, IsAuth
from app.minio import add_pic

from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from django.http import HttpResponse
from django.conf import settings

import redis
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import *
from rest_framework.status import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView

import uuid

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

# user = AuthUser(id=1, first_name="User", email="aa@mail.ru", password=1234)
# moderator = AuthUser(id=2, first_name="mod", email="ba@mail.ru", password=12345)

# user = AuthUser(id=1, first_name="User", email="aaaaaa@mail.ru", password=1234)
# moderator = AuthUser(id=4, email="moderator@e.ru", password=000, is_staff = True)

@csrf_exempt
@swagger_auto_schema(method='post')
@api_view(['Post'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=email, password=password)
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, email)
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password,
            "is_superuser": user.is_superuser,
        }
        # login(request, user)
        response = Response(user_data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, samesite="Lax")
        return response
    else:
        return HttpResponse("error", status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@authentication_classes([])
def logout_view(request):
    ssid = request.COOKIES["session_id"]
    if session_storage.exists(ssid):
        session_storage.delete(ssid)
        response_data = {'Success'}
        return HttpResponse(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {'Error: Session does not exist'}
    return HttpResponse(response_data, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuth])
def user_info(request):
    try:
        ssid = request.COOKIES["session_id"]
        if session_storage.exists(ssid):
            email = session_storage.get(ssid).decode('utf-8')
            user = AuthUser.objects.get(email=email)
            user_data = {
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_superuser": user.is_superuser
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'})
    except:
        return Response({'status': 'Error', 'message': 'Cookies are not transmitted'})


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer
    model_class = AuthUser

class DishesViewSet(APIView):
    model_class = Dishes
    serializer_class = DishSerializer
    permission_classes=[IsManagerOrReadOnly]

    def get(self, request, format=None):                                    # все блюда
        min_price = request.query_params.get("min_price", '0')
        max_price = request.query_params.get("max_price", '10000000')
        tag = request.query_params.get("tag", '')
        title = request.query_params.get("title", '')

        filters = Q(status="есть") & Q(price__range=(min_price, max_price))
        if tag != '':
            filters &= Q(tags=tag)
        if title != '':
            filters &= Q(title=title)

        dish = Dishes.objects.filter(filters).order_by('title')
        dish_serializer = self.serializer_class(dish, many=True)

        try:
            ssid = request.COOKIES["session_id"]
            email = session_storage.get(ssid).decode('utf-8')
            cur_user = AuthUser.objects.get(email=email)
            # заказ определенного пользователя
            try: 
                order=Orders.objects.filter(user=cur_user, status="зарегистрирован").latest('created_at')
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
        except:
            return Response({'order': [], 'dishes': dish_serializer.data})
        
    @swagger_auto_schema(request_body=DishSerializer)
    def post(self, request, format=None):                                   # добавить блюдо
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
    permission_classes=[IsManagerOrReadOnly]

    def get(self, request, pk, format=None):                                 # 1 блюдо
        if not Dishes.objects.filter(id=pk, status="есть").exists():
            return Response(f"Такого блюда нет")

        dish = Dishes.objects.get(id=pk)
        serializer = self.serializer_class(dish)
        return Response(serializer.data)

    @swagger_auto_schema()
    def delete(self, request, pk, format=None):                              # удалить блюдо
        if not Dishes.objects.filter(id=pk, status="есть").exists():
            return Response(f"Такого блюда нет")
        dish = Dishes.objects.get(id=pk)
        dish.status = "удаленo"
        dish.save()
        # dish = Dishes.objects.filter(status="есть")
        # serializer = self.serializer_class(dish, many=True)
        return Response({"message": "success"})

    @swagger_auto_schema(request_body=DishSerializer)
    def put(self, request, pk, format=None):                                 # изменить блюдо
        print('1')
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
    serializer_class = FullOrderSerializer
    permission_classes=[IsManagerOrReadOnly]

    def get(self, request, format=None):                                  # все заказы
        try:
            ssid = request.COOKIES["session_id"]
            email = session_storage.get(ssid).decode('utf-8')
            cur_user = AuthUser.objects.get(email=email)
        except:
            return HttpResponse("Сессия не найдена", status=status.HTTP_403_FORBIDDEN)
        date_format = "%Y-%m-%d"
        start_date_str = request.query_params.get("start", '2000-01-01')
        if start_date_str == '':
            start_date_str = '2000-01-01'
        start = datetime.strptime(start_date_str, date_format).date()

        end_date_str = request.query_params.get("end", '3023-12-31')
        if end_date_str == '':
            end_date_str = '3023-12-31'
        end = datetime.strptime(end_date_str, date_format).date()

        statusVal = request.query_params.get("status", '')
        emailVal = request.query_params.get("email", '')

        filters = ~Q(status="отменен") & ~Q(status="зарегистрирован")
        if bool(cur_user.is_staff or cur_user.is_superuser):
            if statusVal != '':
                filters &= Q(status=statusVal)
            if emailVal != '':
                try:
                    found_user = AuthUser.objects.get(email=emailVal)
                    filters &= Q(user=found_user)
                except:
                    filters &= Q(user=-1)
            filters &= Q(created_at__range=(start, end))
            orders = Orders.objects.filter(filters).order_by('-created_at')
            serializer = self.serializer_class(orders, many=True)
        else:
            try:
                filters &= Q(user=cur_user)
                order = Orders.objects.filter(filters).order_by('-created_at')
                serializer = self.serializer_class(order, many=True)
            except:
                return Response('Заказов нет')
        
        return Response(serializer.data)


class OrderViewSet(APIView):
    model_class = Orders
    serializer_class = FullOrderSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get(self, request, pk, format=None):                                # 1 заказ
        try: 
            ssid = request.COOKIES["session_id"]
            email = session_storage.get(ssid).decode('utf-8')
            cur_user = AuthUser.objects.get(email=email)
        except:
            return Response("Сессия не найдена", status=status.HTTP_403_FORBIDDEN)
        if (cur_user.is_superuser or cur_user.is_staff):
            try:
                order = Orders.objects.get(id=pk)
            except Orders.DoesNotExist:
                return Response(f"Заказа с таким id нет", status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                order = Orders.objects.filter(user=cur_user).get(id=pk)
            except Orders.DoesNotExist:
                return Response(f"Заказа с таким id нет", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(order)
        return Response(serializer.data)
    
    @swagger_auto_schema()
    def delete(self, request, pk, format=None):                             # удалить заказ
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
    permission_classes = [IsAuth]

    @swagger_auto_schema()
    def put(self, request, pk, format=None):                               # изменение м-м(кол-во), передаем id блюда
        try:
            ssid = request.COOKIES["session_id"]
            email = session_storage.get(ssid).decode('utf-8')
            cur_user = AuthUser.objects.get(email=email)
            order=Orders.objects.get(user=cur_user, status="зарегистрирован") # заказ определенного пользователя
        except:
            return Response("Сессия не найдена", status=status.HTTP_403_FORBIDDEN)
        dishes_orders = DishesOrders.objects.get(dish_id=pk, order_id=order.id)

        try:                                                                # если передем в теле кол-во
            dishes_orders.quantity = request.data["quantity"]
            dishes_orders.save()
        except:                                                            # если не передем в теле ничего
            dishes_orders.quantity = dishes_orders.quantity + 1
            dishes_orders.save()

        dishes_orders = DishesOrders.objects.get(order_id=order.id, dish_id=pk)
        serializer = self.serializer_class(dishes_orders)
        return Response(serializer.data)

    @swagger_auto_schema()
    def delete(self, request, pk, format=None):                              # удаление м-м, передаем id блюда
        try: 
            ssid = request.COOKIES["session_id"]
            email = session_storage.get(ssid).decode('utf-8')
            cur_user = AuthUser.objects.get(email=email)
            order=Orders.objects.get(user=cur_user, status="зарегистрирован") # заказ определенного пользователя
        except:
            return Response("Сессия не найдена", status=status.HTTP_403_FORBIDDEN)
        dishes_orders = get_object_or_404(DishesOrders, dish_id=pk, order_id=order.id)
        dishes_orders.delete()

        dishes_orders = DishesOrders.objects.filter(order_id=order.id)
        serializer = self.serializer_class(dishes_orders, many=True)
        return Response(serializer.data)




# Dishes
@swagger_auto_schema(method='post')
@permission_classes([IsAuthenticated])
@api_view(['POST'])                                  # добавить блюдо в заказ
def PostDishToOrder(request, pk):
    try:
        print(request)
        ssid = request.COOKIES["session_id"]
        print(ssid)
        email = session_storage.get(ssid).decode('utf-8')
        cur_user = AuthUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена", status=status.HTTP_403_FORBIDDEN)
    try: 
        order=Orders.objects.filter(user=cur_user, status="зарегистрирован").latest('created_at') # заказ определенного пользователя
    except:
        order = Orders(                              # если нет, создаем новый заказ
            status='зарегистрирован',
            created_at=datetime.now(),
            user=cur_user,
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

    # dishes_orders = DishesOrders.objects.get(order_id=order_id, dish_id=dish_id)  # выводим 1 м-м
    # serializer = DishOrderSerializer(dishes_orders)
    orders = Orders.objects.get(id=order_id)  # выводим 1 заказ
    serializer = OrderSerializer(orders)
    return Response(serializer.data)

#Orders
@swagger_auto_schema(method='put')
@api_view(['PUT'])                                  # статусы модератора
@permission_classes([IsManagerOrReadOnly])
def ConfirmOrder(request, pk):
    if not Orders.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")

    order = Orders.objects.get(id=pk)
    try:
        ssid = request.COOKIES["session_id"]
        email = session_storage.get(ssid).decode('utf-8')
        cur_user = AuthUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена", status=status.HTTP_403_FORBIDDEN)
    if bool(cur_user.is_staff == False and cur_user.is_superuser == False):
        return Response("Нет прав", status=status.HTTP_403_FORBIDDEN)
    else:
        order.moderator=cur_user                  # назначаем модератора

        if order.status != "сформирован":
            return Response("Такой заказ не сформирован", status=status.HTTP_400_BAD_REQUEST)
        if request.data["status"] not in ["отказ", "готов"]:
            return Response("Ошибка", status=status.HTTP_400_BAD_REQUEST)
        order.status = request.data["status"]
        order.completed_at=datetime.now()
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)

@swagger_auto_schema(method='put')
@api_view(['PUT'])                                  # статусы пользователя
@permission_classes([IsAuth])
def ToOrder(request):
    try:
        ssid = request.COOKIES["session_id"]
        email = session_storage.get(ssid).decode('utf-8')
        cur_user = AuthUser.objects.get(email=email)
    except:
        return Response({'Сессия не найдена'}, status=status.HTTP_403_FORBIDDEN)
    # заказ определенного пользователя
    try: 
        order=Orders.objects.filter(user=cur_user, status="зарегистрирован").latest('created_at')
    # заказа-черновика нет
    except:
        return Response({'error: no order'})

    if order.status != "зарегистрирован":
        return Response("Такой заказ не зарегистрован", status=status.HTTP_404_NOT_FOUND)
    if request.data["status"] not in ["отменен", "сформирован"]:
        return Response("Ошибка", status=status.HTTP_400_BAD_REQUEST)

    order.status = request.data["status"]
    order.processed_at=datetime.now()           #.strftime("%d.%m.%Y %H:%M:%S")
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['POST'])
def Calculate(request):                         # Обработка ответа от второго сервиса
    order_id = int(request.data.get('order_id'))
    token = 4321
    second_service_url = "http://localhost:8080/calc"
    data = {
        'order_id': order_id,
        'token': token
    }

    headers = {
        'Content-Type': 'application/json'
    }
    try:
        order = requests.post(second_service_url, data=data)
        exp = Orders.objects.get(id=order_id)
    except:
        return Response('Нет подключения', status=status.HTTP_404_NOT_FOUND)
    if order.status_code == 200:
        exp.is_success = "ожидание оплаты"
        exp.save()
        serializer = OrderSerializer(exp)
        return Response(serializer.data)
    else:
        return Response(data={'error': 'Запрос завершился с кодом: {}'.format(order.status_code)},
                        status=order.status_code)

@api_view(['PUT'])
@permission_classes([AllowAny])
def Result(request, format=None):                # Обновление данных
    if request.method != 'PUT':
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order_id = request.data.get('order_id')
    try:
        print(request.data.get('token'))
        print(int(request.data.get('is_success')))
        if (int(request.data.get('token')) != 4321):
            return Response({'error'}, status=status.HTTP_403_FORBIDDEN)
        if (int(request.data.get('is_success')) > 20):
            result = "прошла"
        else: 
            result = "не прошла!"
    except:
        return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        order = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

    order.is_success = result
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)