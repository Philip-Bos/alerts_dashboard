from flask import Flask, render_template, request, session, redirect, url_for, flash
from functions.place_alert import place_alert
from routes.order import order_bp
from routes.create_alert import create_alert_bp
from routes.create_payloads import create_payloads_bp
from routes.connect_kite import connect_kite_bp, kite
from functions.list_alerts import list_alerts
from functions.delete_alert import delete_alert

app = Flask(__name__)
app.secret_key = "any random string"
app.register_blueprint(order_bp)
app.register_blueprint(create_alert_bp)
app.register_blueprint(create_payloads_bp)
app.register_blueprint(connect_kite_bp)


@app.route("/", methods=("GET", "POST"))
def index():
    if "kf_session" in request.cookies:
        kf_sess = request.cookies.get("kf_session")
        enc = request.cookies.get("enc_token")
        uid = request.cookies.get("user_id")
        print(kf_sess, enc, uid)
    if request.method == "POST":
        username = request.form.get("username")
        session_id = request.form.get("session_id")
        session["username"] = username
        session["session_id"] = session_id
        session["ref"] = request.url
        try:
            alert_list = list_alerts(session["username"], session["session_id"])
            flash("You were successfully logged in", "success")
        except:
            None
        return redirect(url_for("index"))

    if "username" in session:
        try:
            alert_list = list_alerts(session["username"], session["session_id"])
            return render_template(
                "index.html",
                alerts=alert_list,
                username=session["username"],
                session_id=session["session_id"],
            )
        except:
            session.pop("username", None)
            session.pop("session_id", None)
            session.pop("ref", None)
            flash("Error loggin in, try again.", "error")
            return render_template("index.html")
    return render_template("index.html")


@app.route("/test_alert", methods=["POST"])
def test_alert():
    al = place_alert(
        session["username"],
        "BINGX:BTCUSDT",
        "Alert",
        "Alert Message",
        20000,
        "",
        session["session_id"],
        "Cancel Alert",
        19000,
        "Cancel Alert Message",
    )
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    session.pop("username", None)
    session.pop("session_id", None)
    session.pop("ref", None)
    flash("You were successfully logged out.", "success")
    return redirect(url_for("index"))


@app.route("/logout_kite")
def logout_kite():
    # remove the username from the session if it is there
    session.pop("kite", None)
    flash("You were successfully logged out of kite.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<alert_id>", methods=("GET", "POST"))
def delete(alert_id):
    if request.method == "POST":
        if "username" in session:
            delete_alert(alert_id, session["username"], session["session_id"])
            return redirect(url_for("index"))


@app.route("/delete_alerts", methods=("GET", "POST"))
def delete_mult():
    if request.method == "POST":
        print("hello")


@app.route("/guide")
def guide():
    return render_template("guide.html")
