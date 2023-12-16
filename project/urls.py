from django.contrib import admin
from app import views
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers

routerUser = routers.DefaultRouter()
# routerDishes = routers.DefaultRouter()


routerUser.register(r'user', views.UserViewSet, basename='user')
# routerDishes.register(r'dishes', views.DishesViewSet, basename='dishes')


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
    #Dish
    path(r'dishes/', views.DishesViewSet.as_view(), name='dishes'),
    path(r'dishes/<int:pk>', views.DishViewSet.as_view(), name='dish'),
    path('dishes/<int:pk>/post', views.PostDishToOrder, name = 'dish_add'),

    #Order
    path(r'orders/', views.OrdersViewSet.as_view(), name='orders'),
    path(r'orders/<int:pk>', views.OrderViewSet.as_view(), name='order'),
    path('orders/<int:pk>/confirm', views.ConfirmOrder, name = 'order_confirm'),
    path('orders/accept', views.ToOrder, name = 'order_accept'),

    #Dishes-Orders
    path(r'dishes_orders/<int:pk>', views.DishesOrdersViewSet.as_view(), name='dishes_orders'),

    # Login
    path('', include(routerUser.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',  views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('user_info', views.user_info, name = 'user_info'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
