#from django.http import HttpResponse
from django.shortcuts import render
from bmstu_lab.models import *
from django.shortcuts import redirect
import psycopg2

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
    # dish = Dishes.objects.get(id=id)
    # dish.status = 'disabled'
    # dish.save()
    conn = psycopg2.connect(database="small_business", user="postgres", password="1234", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("update dishes set status='deleted' WHERE id = %s;", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('dishes')

# def sendText(request):
#     input_text = request.POST['text']
