#from django.http import HttpResponse
from django.shortcuts import render

dishes = [
    {
        'title': 'Гаспачо', 
        'id': 0, 
        'chef': 'Mauro Colagreco', 
        'price': '9', 
        'tegs': 'VEG',
        'weight': '5',
        'url': "img/0.jpeg", 
        'chef_post': 'main',
        'chef_url': "img/1.0.png"
    },
    {
        'title': 'не бургер', 
        'id': 1, 
        'chef': 'Christophe Bacquie', 
        'price': '15', 
        'tegs': 'VEG', 
        'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'
    },
    {
        'title': 'неxnj', 
        'id': 2, 
        'chef': 'Mauro Colagreco', 
        'price': '4', 
        'tegs': 'SPICY', 
        'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'
    },
    {
        'title': 'неxnj', 
        'id': 3, 
        'chef': 'Laurent Petit', 
        'price': '9', 
        'tegs': 'NEW', 
        'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'
    },
    {
        'title': 'неxnj', 
        'id': 4, 
        'chef': 'Mauro Colagreco', 
        'price': '4', 
        'tegs': 'SWEET, SPICY', 
        'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'
    },
    {
        'title': 'Коврик для мышки',  
        'id': 5, 
        'chef': 'Dan Barber', 
        'price': '19', 
        'tegs': 'VEG', 
        'url': 'https://media.istockphoto.com/id/1136168094/ru/фото/куриные-терияки-еды-подготовительный-обед-коробки-контейнеры-с-брокколи-рисом-и-морковью.jpg?s=612x612&w=0&k=20&c=7oRrk2U0oKLKuviPV2LBYpNWbS0_n0bOwQbMfALgz_I='
    },
]
def GetOrders(request):
    return render(request, 'orders.html', {'data' : {
        'dishes': dishes
    }})

def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'id': id,
        'dish': dishes[id]
    }})

def sendText(request):
    input_text = request.POST['text']
