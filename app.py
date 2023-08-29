from flask import Flask, jsonify, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

shows_db = SQL("sqlite:///shows.db")
db = SQL("sqlite:///users.db")




# if logged in redirect from login to index


@app.route("/")
def index():
    if session["username"] == None or session["password"] == None:
        return redirect("/login")
    else:
        return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        db.execute(f"""INSERT INTO users (username, password) VALUES ("{session["password"]}", "{session["password"]}")""")
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        if db.execute(f"SELECT id FROM users WHERE username='{session['username']}' and password='{session['password']}'"):
            return redirect("/")
        else:
            session["username"] == None
            session["password"] == None
            return render_template("login.html", message="That account doesn't exist")
    if session["username"] is not None and session["password"] is not None:
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":
        if request.form.get("clear") is not None:
            print(session["cart"])
            session["cart"] = []
            return "clear"

        if request.form.get("book_id") is not None:
            book = request.form.get("book_id")
            if book not in session["cart"]:
                session["cart"].append(book)
            return redirect("/cart")

    else:
        return render_template("cart.html", books=session["cart"])

@app.route("/logout")
def logout():
    session["username"] = None
    session["password"] = None
    return redirect("/")

@app.route("/delete_account")
def delete_account():
    db.execute(f"DELETE FROM users WHERE username = '{session['username']}'")
    return redirect("/logout")

@app.route("/search")
def search():
    showsOrder = request.args.get("shows-order")
    showsQuantity = request.args.get("shows-quantity")
    showsAscDesc = request.args.get("shows-asc-desc")
    q = request.args.get("q")
    if q:
        shows = shows_db.execute("SELECT * FROM shows INNER JOIN ratings on ratings.show_id = shows.id WHERE shows.title LIKE ? ORDER BY " + showsOrder + " " + showsAscDesc + " LIMIT " + showsQuantity + "", "%" + q + "%")
    else:
        shows = []
    return jsonify(shows)
