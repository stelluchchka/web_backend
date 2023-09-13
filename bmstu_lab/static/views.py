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
        'id': id
    }})

def sendText(request):
    input_text = request.POST['text']

# def GetOrders(request):
#     filter_field = request.GET.get('filter_field')
#     if filter_field not in ['name', 'price']:
#         filter_field = 'name'  # Default to filtering by name if an invalid field is provided

#     services = Service.objects.all().order_by(filter_field)

#     return render(request, 'orders.html', {'data': {
#         'current_date': date.today(),
#         'services': services,  # Pass the filtered services to the template
#         'orders': [
#             {'title': 'бургер', 'id': 1, 'chef': 'Mauro Colagreco', 'url': 'https://cojo.ru/wp-content/uploads/2022/12/risunki-edy-1.webp'},
#             {'title': 'не бургер', 'id': 2, 'chef': 'Christophe Bacquie', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
#             {'title': 'неxnj', 'id': 3, 'chef': 'Mauro Colagreco', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
#             {'title': 'неxnj', 'id': 4, 'chef': 'Laurent Petit', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
#             {'title': 'неxnj', 'id': 5, 'chef': 'Mauro Colagreco', 'url': 'https://img.freepik.com/premium-vector/food-and-dessert-seamless-pattern_1639-40641.jpg'},
#             {'title': 'Коврик для мышки',  'id': 6, 'chef': 'Dan Barber','url': 'https://media.istockphoto.com/id/1136168094/ru/фото/куриные-терияки-еды-подготовительный-обед-коробки-контейнеры-с-брокколи-рисом-и-морковью.jpg?s=612x612&w=0&k=20&c=7oRrk2U0oKLKuviPV2LBYpNWbS0_n0bOwQbMfALgz_I='},
#         ]
#     }})