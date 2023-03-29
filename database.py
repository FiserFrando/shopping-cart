from datetime import datetime

from decouple import config
from peewee import (DateTimeField, ForeignKeyField, IntegerField, Model,
                    MySQLDatabase, TextField)

database = MySQLDatabase(
    'shopping-cart',
    user = 'root',
    password = config('dbpassword'),
    port = 3306,
    host = 'localhost'
)


class User(Model):
    name = TextField()
    email = TextField()
    password = TextField()
    created_at = DateTimeField(default=datetime.now())
    last_login = DateTimeField

    class Meta:
        database = database
        db_table = 'users'


class Shopping_cart(Model):
    user_id = ForeignKeyField(User, backref='shopping_carts')
    total_price = IntegerField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField()

    class Meta:
        database = database
        db_table = 'shopping_carts'


class Product(Model):
    name = TextField()
    price = IntegerField()
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        database = database
        db_table = 'products'


class Category(Model):
    name = IntegerField()
    created_at = IntegerField()

    class Meta:
        database = database
        db_table = 'categories'


class Shopping_cart_products(Model):
    Shopping_cart_id = ForeignKeyField(Shopping_cart, backref='shopping_cart_products')
    Product_id = ForeignKeyField(Product, backref='shopping_cart_products')
    
