from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Portable database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        uname = request.form["uname"].strip()
        passw = request.form["passw"].strip()

        login_user = user.query.filter_by(
            username=uname,
            password=passw
        ).first()

        if login_user:
            return redirect(url_for("index"))

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        uname = request.form['uname'].strip()
        mail = request.form['mail'].strip()
        passw = request.form['passw'].strip()

        # Basic validation
        if not uname or not mail or not passw:
            return "All fields are required"

        new_user = user(
            username=uname,
            email=mail,
            password=passw
        )

        db.session.add(new_user)
        db.session.commit()

        # Show confirmation page with submitted data
        return render_template(
            "success.html",
            username=uname,
            email=mail
        )

    return render_template("register.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)