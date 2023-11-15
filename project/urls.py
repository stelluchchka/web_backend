from django.contrib import admin
from app import views
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers

# routerDish = routers.DefaultRouter()
# routerOrder = routers.DefaultRouter()
# router3 = routers.DefaultRouter()

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
# routerDish.register(r'dishes', views.DishViewSet)
# routerOrder.register(r'orders', views.OrderViewSet)
# router3.register(r'dishes_orders', views.DishesOrdersViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('', include(routerDish.urls)),
    # path('', include(routerOrder.urls)),
    # path('', include(router3.urls)),

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

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Login
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',  views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]
