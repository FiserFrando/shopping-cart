from datetime import datetime

from flask import Flask, redirect, render_template, request, session
from peewee import *

from count_products import count_products
from database import (
    Category,
    Product,
    Product_category,
    Shopping_cart,
    Shopping_cart_products,
    User,
)

app = Flask(__name__)
app.secret_key = (
    'asflknjkJKIU/&/()h976789BH/(&%)()ghG(/&%//GR$&%T/gjhkjHiohbhjgGGYom!"#!")'
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        login = datetime.now()

        if User.select().where(User.email == email):
            return render_template("email-exists.html", email=email)

        if username and email and password:
            user = User.create(
                username=username,
                email=email,
                password=password,
                last_login=login,
                rol="user",
            )
            session["user_id"] = user.id
            session["user_rol"] = "user"

            if not session.get("shopping_cart_id"):
                cart = Shopping_cart.create(user_id=user.id, created_at=datetime.now())
                print(datetime.now())
                session["shopping_cart_id"] = cart.id
                print(cart.created_at)

            return redirect("/home")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(email, password)

        try:
            print(email, password)
            user = User.get(User.email == email)

            if user.password == password:
                print(user.username)
                login = datetime.now()

                user.last_login = login
                user.save()

                session["user_id"] = user.id

                if user.rol == "admin":
                    session["user_rol"] = "admin"
                else:
                    session["user_rol"] = "user"

                print("111")

                print(session.get("shopping_cart_id"))

                if not session.get("shopping_cart_id"):
                    cart = Shopping_cart.create(
                        user_id=user.id, created_at=datetime.now()
                    )
                    print(datetime.now())
                    session["shopping_cart_id"] = cart.id
                    print(cart.created_at)
                return redirect("/home")
            else:
                return render_template("no-login.html")

        except:
            return render_template("no-login.html")

    return render_template("login.html")


@app.route("/logout")
def logout():
    return render_template("/logout.html")


@app.route("/logoutme")
def logoutme():
    if not session.get("user_id"):
        return redirect("/")

    try:
        shopping_cart = Shopping_cart.get(
            Shopping_cart.id == session["shopping_cart_id"]
        )
        shopping_cart.deleted = True
        shopping_cart.save()
        session.clear()
        return redirect("/")
    except:
        session.clear()
        return redirect("/")


@app.route("/home")
def home():
    if not session.get("user_id"):
        return redirect("/")

    total = count_products()

    print("total 2:", total)

    if session["user_rol"] == "user":
        return render_template("home.html", total=total)
    else:
        return render_template("/admin/home.html", total=total)


@app.route("/categories")
def categories():
    if not session.get("user_id"):
        return redirect("/")

    categories = (
        Category.select().where(Category.deleted == False).order_by(Category.name)
    )

    return render_template("/categories/index.html", categories=categories)


@app.route("/categories/create", methods=["GET", "POST"])
def category_create():
    if not session.get("user_id"):
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")
        print(name)

        if name:
            Category.create(name=name)
            return redirect("/categories")

    return render_template("categories/create.html")


@app.route("/categories/update/<id>", methods=["GET", "POST"])
def category_update(id):
    if not session.get("user_id"):
        return redirect("/")

    category = Category.get(Category.id == id)

    if request.method == "POST":
        name = request.form.get("name")

        if name:
            category.name = name

            category.save()

            return redirect("/categories")

    return render_template("/categories/update.html", category=category)


@app.route("/categories/delete/<id>", methods=["GET", "POST"])
def category_delete(id):
    if not session.get("user_id"):
        return redirect("/")

    category = Category.get(Category.id == id)

    if request.method == "POST":
        si = request.form.get("si")
        no = request.form.get("no")

        if no:
            return redirect("/categories")

        if si:
            category.deleted = True
            category.save()
            return redirect("/categories")

    return render_template("categories/delete.html", category=category)


@app.route("/products")
def products():
    if not session.get("user_id"):
        return redirect("/")

    products = Product.select().where(Product.deleted == False).order_by(Product.name)

    print(session["user_rol"])

    total = count_products()

    if session["user_rol"] == "admin":
        return render_template("/products/index.html", products=products, total=total)

    return render_template("/products/index_users.html", products=products, total=total)


@app.route("/products/create", methods=["GET", "POST"])
def product_create():
    if not session.get("user_id"):
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")
        price = int(request.form.get("price")) * 100
        categories = request.form.getlist("category_id")

        if name and price:
            product = Product.create(name=name, price=price)

            for category_id in categories:
                Product_category.create(product_id=product.id, category_id=category_id)

            return redirect("/products")

    categories = Category.select().order_by(Category.name)

    return render_template("products/create.html", categories=categories)


@app.route("/products/update/<id>", methods=["GET", "POST"])
def product_update(id):
    if not session.get("user_id"):
        return redirect("/")

    product = Product.get(Product.id == id)

    if request.method == "POST":
        name = request.form.get("name")
        price = int(request.form.get("price")) * 100
        categories_id = request.form.getlist("category_id")
        print("categorías: ", categories_id)

        if name and price:
            product.name = name
            product.price = price
            product.save()

            products_categries = Product_category.select().where(
                Product_category.product_id == product.id
            )

            for i in products_categries:
                if i.category_id not in categories_id:
                    i.delete_instance()
                    print(i.category_id, categories_id)

            for i in categories_id:
                if not Product_category.select().where(
                    Product_category.product_id == product.id,
                    Product_category.category_id == i,
                ):
                    Product_category.create(product_id=product.id, category_id=i)

            return redirect("/products")

    categories_selected = (
        Category.select()
        .join(Product_category, on=(Category.id == Product_category.category_id))
        .where(Product_category.product_id == product.id)
        .order_by(Category.name)
    )

    categories_checked = []
    for category in categories_selected:
        categories_checked.append(category.id)

    categories_no_selected = (
        Category.select()
        .where(Category.id.not_in(categories_checked))
        .order_by(Category.name)
    )

    return render_template(
        "/products/update.html",
        product=product,
        categories_selected=categories_selected,
        categories_no_selected=categories_no_selected,
    )


@app.route("/products/delete/<id>", methods=["GET", "POST"])
def product_delete(id):
    if not session.get("user_id"):
        return redirect("/")

    product = Product.get(Product.id == id)

    if request.method == "POST":
        si = request.form.get("si")
        no = request.form.get("no")

        if no:
            return redirect("/products")

        if si:
            product.deleted = True
            product.save()
            return redirect("/products")

    return render_template("products/delete.html", product=product)


@app.route("/products/details/<id>", methods=["GET", "POST"])
def product_details(id):
    if not session.get("user_id"):
        return redirect("/")

    product = Product.get(Product.id == id)

    if request.method == "POST":
        quantity = request.form.get("quantity")
        print(quantity)

        if quantity:
            Shopping_cart_products.create(
                shopping_cart_id=session["shopping_cart_id"],
                product_id=product.id,
                quantity_products=quantity,
                created_at=datetime.now(),
            )

            return redirect("/products")

    return render_template("/products/details.html", product=product)


@app.route("/shopping_cart")
def shopping_cart():
    if not session.get("user_id"):
        return redirect("/")

    return render_template("/shopping_cart/example.html")


if __name__ == "__main__":
    app.run(debug=True)
