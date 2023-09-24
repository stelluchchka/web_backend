from app.models import *
from rest_framework import serializers


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ["title", "price", "tags", "weight", "energy_value", "content", "chef_name", 
                  "chef_post", "chef_url", "status", "expiry_date", "url"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ["status", "created_at", "processed_at", "completed_at", "moderator_id", "user"]