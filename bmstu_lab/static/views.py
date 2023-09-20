#from django.http import HttpResponse
from django.shortcuts import render
from models import *

def GetDishes(request):
    keyword = request.GET.get('keyword')
    a = Dishes.objects.filter(status='enabled')
    if keyword:
         keyword = keyword[0].upper()+keyword[1:]
         a = Dishes.objects.filter(status='enabled').filter(title=keyword)
    return render(request, 'dishes.html', {'data': {
        'dishes': a},
        "search_query": keyword if keyword else ""})

def GetDish(request, id):
    return render(request, 'dish.html', {'data' : {
        'dish': Dishes.objects.get(id = id)
    }})


# def sendText(request):
#     input_text = request.POST['text']
