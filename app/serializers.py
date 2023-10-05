from app.models import *
from rest_framework import serializers


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"

class DishOrderSerializer(serializers.ModelSerializer):
    dish = serializers.StringRelatedField(read_only=True)
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DishesOrders
        fields = "__all__"