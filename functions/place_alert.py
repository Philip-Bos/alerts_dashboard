import requests
import json

from functions.payloads import generate_payload

def place_cancel_alert(
    username, symbol, webhook_url, session_id, cancel_title, cancel_lvl, cancel_mssg):
    username = username
    webhook_url = webhook_url
    symbol = symbol
    session_id = session_id
    method = "create_alert"

    url = (
        f"https://alerts.tradingview.com/alerts/?"
        f"?log_username={username}"
        f"&log_method={method}"
    )

    payload = generate_payload(
        username, symbol, cancel_title, cancel_mssg, cancel_lvl, webhook_url, session_id
    )

    headers = {
        "accept": "*/*",
        "content-type": "text/plain;charset=UTF-8",
        "cookie": "sessionid=" + session_id,
        "origin": "https://www.tradingview.com",
        "referer": "https://www.tradingview.com/",
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload)).json()
    alert_id = response["p"]
    print("alert placed: " + str(alert_id["id"]))
    return alert_id

def place_alert(
    username,
    symbol,
    alert_title,
    message,
    level,
    webhook_url,
    session_id,
    cancel_title,
    cancel_lvl,
    cancel_mssg,
):
    username = username
    webhook_url = webhook_url
    symbol = symbol
    session_id = session_id
    method = "create_alert"

    url = (
        f"https://alerts.tradingview.com/alerts/?"
        f"?log_username={username}"
        f"&log_method={method}"
    )

    payload = generate_payload(
        username, symbol, alert_title, message, level, webhook_url, session_id
    )
    headers = {
        "accept": "*/*",
        "content-type": "text/plain;charset=UTF-8",
        "cookie": "sessionid=" + session_id,
        "origin": "https://www.tradingview.com",
        "referer": "https://www.tradingview.com/",
    }
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload)
    ).json()
    alert_id = response["p"]
    place_cancel_alert(
        username, symbol, webhook_url, session_id, cancel_title, cancel_lvl, cancel_mssg
    )
    print("alert placed: " + str(alert_id["id"]))
    return alert_id
