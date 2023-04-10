from datetime import datetime

from decouple import config
from peewee import (
    BooleanField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    MySQLDatabase,
    TextField,
)

database = MySQLDatabase(
    "shopping_cart",
    user="root",
    password=config("dbpassword"),
    port=3306,
    host="localhost",
)


class User(Model):
    username = TextField()
    email = TextField()
    password = TextField()
    rol = TextField()
    created_at = DateTimeField(default=datetime.now())
    last_login = DateTimeField()

    class Meta:
        database = database
        db_table = "users"


class Shopping_cart(Model):
    user_id = ForeignKeyField(User, backref="shopping_carts")
    total_price = IntegerField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField()
    deleted = BooleanField(default=False)

    class Meta:
        database = database
        db_table = "shopping_carts"


class Product(Model):
    name = TextField()
    price = IntegerField()
    created_at = DateTimeField(default=datetime.now())
    deleted = BooleanField(default=False)

    class Meta:
        database = database
        db_table = "products"

    @property
    def price_user(self):
        return int(self.price / 100)


class Category(Model):
    name = TextField()
    created_at = DateTimeField(default=datetime.now())
    deleted = BooleanField(default=False)

    class Meta:
        database = database
        db_table = "categories"


class Shopping_cart_products(Model):
    Shopping_cart_id = ForeignKeyField(Shopping_cart, backref="shopping_cart_products")
    Product_id = ForeignKeyField(Product, backref="shopping_cart_products")
    quantity_products = IntegerField()
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        database = database
        db_table = "shopping_cart_products"


class Product_category(Model):
    product_id = ForeignKeyField(Product, backref="product_categories")
    category_id = ForeignKeyField(Category, backref="product_categories")
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        database = database
        db_table = "product_categories"


database.create_tables(
    [User, Shopping_cart, Shopping_cart_products, Product, Product_category, Category]
)
