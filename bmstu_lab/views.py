#from django.http import HttpResponse
from django.shortcuts import render
from bmstu_lab.models import *
from django.shortcuts import redirect
from django.db import connection

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

def delete_dish(request, id):
    service = Dishes.objects.get(id=id)
    service.status = 'disabled'
    service.save()

    return redirect('dishes')  # Перенаправьте на страницу 'dishes' после удаления услуги

# def sendText(request):
#     input_text = request.POST['text']
