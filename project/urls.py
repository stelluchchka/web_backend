from django.contrib import admin
from app import views
from django.urls import include, path
from rest_framework import routers

# routerDish = routers.DefaultRouter()
# routerOrder = routers.DefaultRouter()
# router3 = routers.DefaultRouter()


# routerDish.register(r'dishes', views.DishViewSet)
# routerOrder.register(r'orders', views.OrderViewSet)
# router3.register(r'dishes_orders', views.DishesOrdersViewSet)

urlpatterns = [
    # path('', include(routerDish.urls)),
    # path('', include(routerOrder.urls)),
    # path('', include(router3.urls)),


    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

    #Dish
    path('dishes/', views.GetDishes, name = 'dishes'),
    path('dishes/post', views.PostDishes, name = 'dishes_post'),
    path('dishes/<int:pk>/', views.GetDish, name = 'dish'),
    path('dishes/<int:pk>/delete', views.DeleteDish, name = 'dish_delete'),
    path('dishes/<int:pk>/put', views.PutDish, name = 'dish_put'),
    path('dishes/<int:pk>/post', views.PostDishToOrder, name = 'dish_add'),

    #Order
    path('orders/', views.GetOrders, name = 'orders'),
    # path('orders/post', views.PostOrders, name = 'orders_post'),
    path('orders/<int:pk>/', views.GetOrder, name = 'order'),
    path('orders/<int:pk>/delete', views.DeleteOrder, name = 'order_delete'),
    # path('orders/<int:pk>/put', views.PutOrder, name = 'order_put'),

    path('orders/<int:pk>/confirm', views.ConfirmOrder, name = 'order_confirm'),
    path('orders/<int:pk>/accept', views.ToOrder, name = 'order_accept'),

    #Dishes-Orders
    path('dishes_orders/<int:pk>/put', views.PutDishesOrders, name = 'dishes_orders_put'),
    path('dishes_orders/<int:pk>/delete', views.DeleteDishesOrders, name = 'dishes_orders_delete'),


]
