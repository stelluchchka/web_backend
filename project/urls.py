from django.contrib import admin
from app import views
from django.urls import include, path
from rest_framework import routers

router1 = routers.DefaultRouter()
router2 = routers.DefaultRouter()
router1.register(r'dishes', views.DishViewSet)
router2.register(r'orders', views.OrderViewSet)


urlpatterns = [
    path('', include(router2.urls)),
    path('', include(router1.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
