from flask import Flask, render_template, request, redirect, session
import sqlite3
import database

app = Flask(__name__)
app.secret_key = "royalfalconsecure"

def get_db():
    conn = sqlite3.connect("shipments.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET","POST"])
def track():

    shipment = None
    history = []

    if request.method == "POST":

        code = request.form["code"]

        db = get_db()

        shipment = db.execute(
            "SELECT * FROM shipments WHERE code=?",(code,)
        ).fetchone()

        history = db.execute(
            "SELECT * FROM history WHERE code=?",(code,)
        ).fetchall()

    return render_template("track.html", shipment=shipment, history=history)



@app.route("/admin", methods=["GET","POST"])
def admin():

    if "login" not in session:
        return redirect("/login")

    db = get_db()

    if request.method == "POST":

        code = request.form["code"]
        origin = request.form["origin"]
        destination = request.form["destination"]
        location = request.form["location"]
        status = request.form["status"]

        db.execute(
        "INSERT OR REPLACE INTO shipments(code,origin,destination,location,status) VALUES(?,?,?,?,?)",
        (code,origin,destination,location,status)
        )

        db.commit()

    shipments = db.execute("SELECT * FROM shipments").fetchall()

    return render_template("admin.html", shipments=shipments)



@app.route("/update", methods=["POST"])
def update():

    db = get_db()

    code = request.form["code"]
    location = request.form["location"]
    status = request.form["status"]

    db.execute(
    "UPDATE shipments SET location=?,status=? WHERE code=?",
    (location,status,code)
    )

    db.execute(
    "INSERT INTO history(code,location,status) VALUES(?,?,?)",
    (code,location,status)
    )

    db.commit()

    return redirect("/admin")



@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        user = request.form["user"]
        password = request.form["password"]

        if user == "admin" and password == "royalfalcon":

            session["login"] = True

            return redirect("/admin")

    return render_template("login.html")



if __name__ == "__main__":
    app.run()
