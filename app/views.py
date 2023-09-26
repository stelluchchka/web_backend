from rest_framework import viewsets
from app.serializers import *
from app.models import *
import psycopg2
from psycopg2 import sql

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
