from app.models import *
from rest_framework import serializers

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Orders
        fields = "__all__"

class CurDishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ['id', 'title', 'price', 'tags', 'url']



class DishOrderSerializer(serializers.ModelSerializer):
    dish = CurDishesSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = DishesOrders
        fields = ['dish', 'order']


class DishesSerializer(serializers.ModelSerializer):
    dish = serializers.StringRelatedField(read_only=True)
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DishesOrders
        fields = "__all__"


class FullOrderSerializer(serializers.ModelSerializer):
    dishes = CurDishesSerializer(many=True, read_only=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, related_name='dishes', blank=True, null=True)
    user = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'status', 'created_at', 'processed_at', 'completed_at', 'is_success', 'user', 'moderator', 'dishes']

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    password = serializers.CharField(write_only=True)

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = super(UserSerializer, self).create(validated_data)
    #     user.set_password(password) 
    #     user.save()
    #     return user
    def create(self, validated_data):
        return AuthUser.objects.create_user(**validated_data)
    
    class Meta:
        model = AuthUser
        fields = "__all__"




# class DishesSerializer1(serializers.ModelSerializer):
#     class Meta:
#         model = Dishes
#         fields = ('id', 'title', 'price', 'tags', 'url')

class DishesOrdersSerializer1(serializers.ModelSerializer):
    # dish = DishesSerializer1()
    id=serializers.CharField(source='dish.id')
    title=serializers.CharField(source='dish.title')
    price=serializers.DecimalField(max_digits=10, decimal_places=2, source='dish.price')
    tags=serializers.CharField(source='dish.tags')
    url=serializers.CharField(source='dish.url')
    
    class Meta:
        model = DishesOrders
        fields = ('id', 'title', 'price', 'tags', 'url', 'quantity')

class OrdersSerializer1(serializers.ModelSerializer):
    dishes = DishesOrdersSerializer1(many=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Orders
        fields = ('id', 'status', 'created_at', 'processed_at', 'completed_at', 'user', 'moderator', 'is_success', 'dishes')
