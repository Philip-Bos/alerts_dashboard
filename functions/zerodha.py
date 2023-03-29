import json
import logging
from datetime import date, datetime
from decimal import Decimal
from flask import Flask, request, jsonify, session
from kiteconnect import KiteConnect

# Base settings
PORT = 5500
HOST = request.url


def serializer(obj):
    return isinstance(obj, (date, datetime, Decimal)) and str(obj)


kite_api_key = "c0awpsmmvm2fvnsh"
kite_api_secret = "vu3nflghvzr6bu8zs94yw1qenyu3wrg1"
redirect_url = "https://{host}/login".format(host=HOST)
login_url = "https://kite.zerodha.com/connect/login?api_key={api_key}".format(
    api_key=kite_api_key
)
console_url = "https://developers.kite.trade/apps/{api_key}".format(
    api_key=kite_api_key
)

# App
app = Flask(__name__)
# Templates
index_template = """
    <div>Make sure your app with api_key - <b>{api_key}</b> has set redirect to <b>{redirect_url}</b>.</div>
    <div>If not you can set it from your <a href="{console_url}">Kite Connect developer console here</a>.</div>
    <a href="{login_url}"><h1>Login to generate access token.</h1></a>"""

login_template = """
    <h2 style="color: green">Success</h2>
    <div>Access token: <b>{access_token}</b></div>
    <h4>User login data</h4>
    <pre>{user_data}</pre>
    <a target="_blank" href="/holdings.json"><h4>Fetch user holdings</h4></a>
    <a target="_blank" href="/orders.json"><h4>Fetch user orders</h4></a>
    <a target="_blank" href="https://kite.trade/docs/connect/v1/"><h4>Checks Kite Connect docs for other calls.</h4></a>
    """

kite = KiteConnect(api_key=kite_api_key)


def get_kite_client():
    """Returns a kite client object"""

    if "access_token" in session:
        kite.set_access_token(session["access_token"])
    return kite


@app.route("/")
def index():
    return index_template.format(
        api_key=kite_api_key,
        redirect_url=redirect_url,
        console_url=console_url,
        login_url=login_url,
    )


@app.route("/login", methods=["GET"])
def login():
    request_token = request.args.get("request_token")
    if not request_token:
        return """
            <span style = "color: red" >
                Error while generating request token.
            </span >
            <a href = '/' > Try again. < a >"""

    kite = get_kite_client()
    data = kite.generate_session(request_token, api_secret=kite_api_secret)
    print(data)
    session["access_token"] = data["access_token"]

    return login_template.format(
        access_token=data["access_token"],
        user_data=json.dumps(data, indent=4, sort_keys=True, default=serializer),
    )


@app.route("/order", methods=["POST"])
def order():
    if request.method == "POST":
        data = request.json
        try:
            if data["secret"] == "14243547362514464":
                if data["type"] == "limit":
                    order_id = kite.place_order(
                        tradingsymbol=data["symbol"],
                        exchange=data["exchange"],
                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                        quantity=data["qty"],
                        variety=kite.VARIETY_AMO,
                        order_type=kite.ORDER_TYPE_LIMIT,
                        product=kite.PRODUCT_CNC,
                        validity=kite.VALIDITY_TTL,
                        validity_ttl=data["validity"],
                        price=data["price"],
                    )
                    print("Order placed. ID is: {}".format(order_id))
                    return "Order placed. ID is: {}".format(order_id)
                if data["type"] == "market":
                    order_id = kite.place_order(
                        tradingsymbol=data["symbol"],
                        exchange=data["exchange"],
                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                        quantity=data["qty"],
                        variety=kite.VARIETY_AMO,
                        order_type=kite.ORDER_TYPE_MARKET,
                        product=kite.PRODUCT_CNC,
                        validity=kite.VALIDITY_TTL,
                        validity_ttl=data["validity"],
                    )
                    print("Order placed. ID is: {}".format(order_id))
                    return "Order placed. ID is: {}".format(order_id)
        except Exception as e:
            print("Order placement failed: {}".format(e))
            return "Order placement failed: {}".format(e)


@app.route("/holdings.json")
def holdings():
    kite = get_kite_client()
    return jsonify(holdings=kite.profile())


@app.route("/orders.json")
def orders():
    kite = get_kite_client()
    return jsonify(orders=kite.orders())


if __name__ == "__main__":
    app.secret_key = "key"
    logging.info("Starting server: http://{host}:{port}".format(host=HOST, port=PORT))
    app.run(host="0.0.0.0", port=PORT, debug=True)
