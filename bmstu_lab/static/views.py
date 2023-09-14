#from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
orders = [
            {'title': 'бургер', 'id': 0, 'chef': 'Mauro Colagreco', 'price': '9', 'tegs': 'VEG', 'url': 'https://cojo.ru/wp-content/uploads/2022/12/risunki-edy-1.webp'},
            {'title': 'не бургер', 'id': 1, 'chef': 'Christophe Bacquie', 'price': '15', 'tegs': 'VEG', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
            {'title': 'неxnj', 'id': 2, 'chef': 'Mauro Colagreco', 'price': '4', 'tegs': 'SPICY', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
            {'title': 'неxnj', 'id': 3, 'chef': 'Laurent Petit', 'price': '9', 'tegs': 'NEW', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
            {'title': 'неxnj', 'id': 4, 'chef': 'Mauro Colagreco', 'price': '4', 'tegs': 'SWEET, SPICY', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
            {'title': 'Коврик для мышки',  'id': 5, 'chef': 'Dan Barber', 'price': '19', 'tegs': 'VEG', 'url': 'https://media.istockphoto.com/id/1136168094/ru/фото/куриные-терияки-еды-подготовительный-обед-коробки-контейнеры-с-брокколи-рисом-и-морковью.jpg?s=612x612&w=0&k=20&c=7oRrk2U0oKLKuviPV2LBYpNWbS0_n0bOwQbMfALgz_I='},
        ]
def GetOrders(request):
    return render(request, 'orders.html', {'data' : {
        'orders': orders
    }})

def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'id': id,
        'order': orders[id]
    }})

def sendText(request):
    input_text = request.POST['text']