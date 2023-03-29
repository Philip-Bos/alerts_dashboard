import requests
from flask import Blueprint, request

order_bp = Blueprint("order", __name__)


@order_bp.route("/order", methods=["POST"])
def place_order():
    # Get the data from the webhook message
    data = request.json

    # Send a post request to the broker API to place an order
    response = requests.post("https://broker.com/api/order", json=data)

    return response.text, response.status_code
