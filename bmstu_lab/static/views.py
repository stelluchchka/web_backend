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
        'url': "img/0.png", 
        'chef_post': 'main',
        'chef_url': "img/1.0.png"
    },
    {
        'title': 'Сосиска в тесте', 
        'id': 1, 
        'chef': 'Christophe Bacquie', 
        'price': '15', 
        'tegs': 'VEG', 
        'weight': '5',
        'url': "img/1.png", 
        'chef_post': 'main',
        'chef_url': "img/1.1.png"    
    },
    {
        'title': 'Кукурузные блинчики', 
        'id': 2, 
        'chef': 'Mauro Colagreco', 
        'price': '4', 
        'tegs': 'SPICY', 
        'weight': '5',
        'url': "img/2.png", 
        'chef_post': 'main',
        'chef_url': "img/1.2.png"     
    },
    {
        'title': 'Сладкие блинчики', 
        'id': 3, 
        'chef': 'Laurent Petit', 
        'price': '9', 
        'tegs': 'NEW', 
        'weight': '5',
        'url': "img/3.png", 
        'chef_post': 'main',
        'chef_url': "img/1.3.png"     
    },
    {
        'title': 'Омлет со свежими овощами', 
        'id': 4, 
        'chef': 'Mauro Colagreco', 
        'price': '4', 
        'tegs': 'SWEET, SPICY', 
        'weight': '5',
        'url': "img/4.png", 
        'chef_post': 'main',
        'chef_url': "img/1.4.png"     
    },
    {
        'title': 'Каша рисовая',  
        'id': 5, 
        'chef': 'Dan Barber', 
        'price': '19', 
        'tegs': 'VEG', 
        'weight': '5',
        'url': "img/5.png", 
        'chef_post': 'main',
        'chef_url': "img/1.5.png"     
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
