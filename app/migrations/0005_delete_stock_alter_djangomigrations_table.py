# Generated by Django 4.2.4 on 2023-12-26 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_stock_delete_users_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='djangomigrations',
            table='django_migrations',
        ),
    ]