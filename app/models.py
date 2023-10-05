from django.db import models

class Dishes(models.Model):
    STATUS_CHOICES = [
        ('enabled', 'есть'),
        ('deleted', 'нет'),
    ]
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    energy_value = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    chef_name = models.CharField(max_length=255, blank=True, null=True)
    chef_post = models.CharField(max_length=255)
    chef_url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    expiry_date = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    urrl = models.BinaryField(blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        managed = False
        db_table = 'dishes'


class DishesOrders(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    dish = models.ForeignKey('Dishes', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dishes_orders'



class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'




class Users(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255)
    def __str__(self):
        return f'({self.role}: {self.name})'
    class Meta:
        managed = False
        db_table = 'users'


class Orders(models.Model):
    STATUS_CHOICES = [
        ('registered', 'принят'),
        ('cooking', 'готовится'),
        ('done', 'приготовлен'),
        ('denied', 'отказ'),
        ('deleted', 'удален')
    ]
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    moderator = models.ForeignKey('Users', models.DO_NOTHING, related_name='orders_moderator_set', blank=True, null=True)
    def __str__(self):
        return f'{self.status}'
    class Meta:
        managed = False
        db_table = 'orders'

