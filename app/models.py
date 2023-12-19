from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

class NewUserManager(UserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user

class AuthUser(AbstractBaseUser):                       # user
    password = models.CharField(max_length=256, null=False)
    last_login = models.DateTimeField(null=True, auto_now=True)   #?s
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(("email адрес"), max_length=128, unique=True, null=False)
    username = models.CharField(max_length=150, null=True)
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь модератором?")
    is_active = models.BooleanField(null=True, default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        managed = False
        db_table = 'auth_user'
    
    USERNAME_FIELD = 'email'

    objects =  NewUserManager()

class Dishes(models.Model):
    STATUS_CHOICES = [
        ('есть', 'enabled'),
        ('удалено', 'deleted'),
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
    status = models.CharField(max_length=50, blank=True, null=True, choices=STATUS_CHOICES)
    expiry_date = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        managed = False
        db_table = 'dishes'


class DishesOrders(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING, related_name='dishes', blank=True, null=True)
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


class Orders(models.Model):
    STATUS_CHOICES = [
        ('зарегистрирован', 'registered'),
        ('отменен', 'canceled'),
        ('сформирован', 'confirmed'),
        ('отказ', 'denied'),
        ('готов', 'complited')
    ]
    status = models.CharField(max_length=50, blank=True, null=True, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('AuthUser', on_delete=models.DO_NOTHING, null=False, blank=False)
    moderator = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='orders_moderator_set', blank=True, null=True)
    def __str__(self):
        return f'{self.status} {self.user}'
    class Meta:
        managed = False
        db_table = 'orders'




class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)




class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False  
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)


    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)