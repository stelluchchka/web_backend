from rest_framework import permissions
from app.models import *
import redis
from django.conf import settings

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class IsManagerOrReadOnly(permissions.BasePermission): 
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        access_token = request.COOKIES["session_id"]
        if access_token is None: 
            return False 
        try: 
            email = session_storage.get(access_token).decode('utf-8') 
        except Exception as e: 
            return False 
        user = AuthUser.objects.filter(email=email).first() 
        return bool(user.is_staff or user.is_superuser)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        access_token = request.COOKIES["session_id"]
        if access_token is None: 
            return False 
        try: 
            email = session_storage.get(access_token).decode('utf-8') 
        except Exception as e: 
            return False 
        user = AuthUser.objects.filter(email=email).first() 
        return user.is_superuser
    
class IsAuth(permissions.BasePermission): 
    def has_permission(self, request, view): 
        access_token = request.COOKIES["session_id"]
        if access_token is None: 
            return False 
        try: 
            user = session_storage.get(access_token).decode('utf-8') 
        except Exception as e: 
            return False 
        return True