from rest_framework import viewsets

# from rest_framework.response import Response
# from rest_framework.decorators import api_view

from app.serializers import *
from app.models import *
# from django.shortcuts import render


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


# @api_view(['GET'])
# def GetDishes(request):
    # queryset = Dishes.objects.all().order_by('title')
    # serializer = DishSerializer
    # keyword = request.GET.get('name')
    # dishes = Dishes.objects.filter(status='enabled')
    # if keyword:
    #     keyword = keyword[0].upper()+keyword[1:]
    #     dishes = Dishes.objects.filter(status='enabled').filter(title=keyword)
    # return render(request, 'dishes.html', {'data': {
    #     'dishes': dishes},
    #     "search_query": keyword if keyword else ""},
    #     Response(serializer.queryset))
    # dishes=Dishes.objects.all()
    # serializer=DishSerializer(dishes, many=True)
    # return Response(serializer.data)


