from datetime import datetime

from flask import Flask, redirect, render_template, request, session

from database import Category, Product, Shopping_cart, User

app = Flask(__name__)
app.secret_key = (
    'asflknjkJKIU/&/()h976789BH/(&%)()ghG(/&%//GR$&%T/gjhkjHiohbhjgGGYom!"#!")'
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            user = User.get((User.email == email) and (User.password == password))
            login = datetime.now()

            user.last_login = login
            user.save()

            session["user_id"] = user.id
            return redirect("/home")

        except:
            return render_template("no-login.html")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
