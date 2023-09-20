from django.db import models

class Dishes(models.Model):
    title = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    energy_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    expiry_date = models.DateField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    chef_name = models.CharField(max_length=255, null=False)
    chef_post = models.CharField(max_length=255, null=True, blank=True)
    chef_url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Orders(models.Model):
    STATUS_CHOICES = (
        ('registered', 'введен'),
        ('moderating', 'готовиться'),
        ('approved', 'приготовлен'),
        ('denied', 'отменен'),
        ('deleted', 'eдален')
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='CREATED')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    moderator = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class DishesOrders(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.dish.title}"

class Users(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email
