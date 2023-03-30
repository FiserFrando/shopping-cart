from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = (
    'asflknjkJKIU/&/()h976789BH/(&%)()ghG(/&%//GR$&%T/gjhkjHiohbhjgGGYom!"#!")'
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
