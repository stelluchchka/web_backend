from django.contrib import admin
from app.models import *

admin.site.register(Dishes)
admin.site.register(Orders)
admin.site.register(DishesOrders)
admin.site.register(AuthUser)