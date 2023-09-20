#from django.http import HttpResponse
from django.shortcuts import render
from bmstu_lab.models import *

def GetDishes(request):
    keyword = request.GET.get('name')
    dishes = Dishes.objects.filter(status='enabled')
    if keyword:
        keyword = keyword[0].upper()+keyword[1:]
        dishes = Dishes.objects.filter(status='enabled').filter(title=keyword)
    return render(request, 'dishes.html', {'data': {
        'dishes': dishes},
        "search_query": keyword if keyword else ""})


def GetDish(request, id):
    return render(request, 'dish.html', {'data' : {
        'dish': Dishes.objects.filter(id = id)[0]
    }})


# def sendText(request):
#     input_text = request.POST['text']
