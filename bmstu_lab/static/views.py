#from django.http import HttpResponse
from django.shortcuts import render
from datetime import date

def GetOrders(request):
    return render(request, 'orders.html', {'data' : {
        'current_date': date.today(),
        'orders': [
            {'title': 'бургер', 'id': 1, 'url': 'https://cojo.ru/wp-content/uploads/2022/12/risunki-edy-1.webp'},
            {'title': 'не бургер', 'id': 2, 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
            {'title': 'неxnj', 'id': 3, 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
            {'title': 'Коврик для мышки', 'id': 4, 'url': 'https://media.istockphoto.com/id/1136168094/ru/фото/куриные-терияки-еды-подготовительный-обед-коробки-контейнеры-с-брокколи-рисом-и-морковью.jpg?s=612x612&w=0&k=20&c=7oRrk2U0oKLKuviPV2LBYpNWbS0_n0bOwQbMfALgz_I='},
        ]
    }})

def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})

# def sendText(request):
#     input_text = request.POST['text']
