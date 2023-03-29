from flask import Blueprint, request, session
from functions.place_alert import place_alert

create_alert_bp = Blueprint("create_alert", __name__)


@create_alert_bp.route("/create_alert", methods=["POST"])
def create_alert():
    data = request.json
    username = data["username"]
    alert_title = data["alert_name"]
    alert_mssg = data["alert_mssg"]
    symbol = data["symbol"]
    alert_lvl = data["alert_lvl"]
    cancel_lvl = data["cancel_lvl"]
    cancel_title = data["cancel_title"]
    cancel_mssg = data["cancel_mssg"]
    webhook_url = data["webhook_url"]
    session_id = data["session_id"]
    al = place_alert(
        username,
        symbol,
        alert_title,
        alert_mssg,
        alert_lvl,
        webhook_url,
        session_id,
        cancel_title,
        cancel_lvl,
        cancel_mssg,
    )
    print(username, symbol, alert_title, alert_mssg, alert_lvl, webhook_url, session_id)
    return al
