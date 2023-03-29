from kiteconnect import KiteConnect
from flask import Blueprint, request, jsonify, session, redirect, url_for
from flask import Blueprint, request, session
import webbrowser

PORT = 5500
HOST = "https://a4f4-2001-8a0-f92b-eb00-9560-f98b-a0f0-f349.eu.ngrok.io/"

kite_api_key = "c0awpsmmvm2fvnsh"
kite_api_secret = "vu3nflghvzr6bu8zs94yw1qenyu3wrg1"
redirect_url = (
    "https://a4f4-2001-8a0-f92b-eb00-9560-f98b-a0f0-f349.eu.ngrok.io/connect_kite"
)


connect_kite_bp = Blueprint("kite", __name__)

kite = KiteConnect(api_key=kite_api_key)


def get_kite_client():
    """Returns a kite client object"""
    if "access_token" in session:
        kite.set_access_token(session["access_token"])
    return kite


@connect_kite_bp.route("/connect_kite", methods=["GET", "POST"])
def connect_kite():
    if request.method == "POST":
        api_key = request.form.get("key")
        api_secret = request.form.get("secret")
        session["api_key"] = api_key
        session["api_secret"] = api_secret
        login_url = "https://kite.zerodha.com/connect/login?api_key=" + api_key
        return redirect(login_url, 302)
    # connect_kite?action=login&type=login&status=success&request_token=KNLFD7uy4Xjibg95wxEYWwhDSwGAXgeE
    request_token = request.args.get("request_token")
    session["kite_req_token"] = request_token
    if not request_token:
        return """
            <span style = "color: red" >
                Error while generating request token.
            </span >
            <a href = '/' > Try again. < a >"""
    data = kite.generate_session(
        session["kite_req_token"], api_secret=session["api_secret"]
    )
    session["kite"] = data
    return redirect(url_for("index"))
