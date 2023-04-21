from flask import session
from peewee import fn

from database import Shopping_cart_products


def count_products():
    try:
        count = Shopping_cart_products.select(
            Shopping_cart_products.quantity_products,
            fn.sum(Shopping_cart_products.quantity_products).alias("SUM"),
        ).where(Shopping_cart_products.shopping_cart_id == session["shopping_cart_id"])

        total = 0

        for c in count:
            total += int(c.SUM)
        return total
    except:
        total = 0
        return total
