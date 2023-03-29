import requests
import json
import pandas as pd


def list_alerts(username, session_id):
    method = "list_alerts"
    url = (
        f"https://alerts.tradingview.com/alerts/?"
        f"?log_username={username}"
        f"&log_method={method}"
    )
    payload = {"m": "list_alerts", "p": {"limit": 2000}}
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
    alerts = response["p"]["alerts"]

    # alerts_["extra"] = alerts["extra"]
    return alerts
