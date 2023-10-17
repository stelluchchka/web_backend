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

# class FullOrderSerializer(serializers.ModelSerializer):
#     dishes = DishSerializer(many=True, read_only=True)

#     class Meta:
#         model = Orders
#         fields = ['id', 'status', 'created_at', 'processed_at', 'completed_at', 'user', 'moderator', 'dishes']


class DishesOrdersSerializer(serializers.ModelSerializer):
    dish_id = serializers.IntegerField(source='dish.id')
    dish_name = serializers.CharField(source='dish.title')

    class Meta:
        model = DishesOrders
        fields = ['dish_id', 'dish_name', 'quantity']

class FullOrderSerializer(serializers.ModelSerializer):
    dishes = DishesOrdersSerializer(many=True, read_only=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, related_name='dishes', blank=True, null=True)

    class Meta:
        model = Orders
        fields = ['id', 'status', 'created_at', 'processed_at', 'completed_at', 'user', 'moderator', 'dishes']
