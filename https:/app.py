from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "royalfalconsecret"

USERNAME = "Bishop7070"
PASSWORD = "Deadpeople"

shipments = {}

@app.route("/", methods=["GET","POST"])
def track():
    result=None
    if request.method=="POST":
        code=request.form.get("tracking")
        result=shipments.get(code)
    return render_template("track.html", result=result)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if "user" not in session:
        return redirect("/login")

    if request.method=="POST":
        code=request.form["code"]
        origin=request.form["origin"]
        destination=request.form["destination"]
        status=request.form["status"]

        shipments[code]={
            "origin":origin,
            "destination":destination,
            "status":status
        }

    return render_template("admin.html", shipments=shipments)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        if u==USERNAME and p==PASSWORD:
            session["user"]=u
            return redirect("/admin")

    return render_template("login.html")

app.run(host="0.0.0.0",port=5000)
