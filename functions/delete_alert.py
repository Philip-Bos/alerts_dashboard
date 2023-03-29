import requests
import json


def delete_alerts(alert_ids, username, session_id):
    print("hello")


def delete_alert(alert_id, username, session_id):
    print("username: " + str(username))
    print("session_id: " + str(session_id))
    print("alert_id: " + str(alert_id))
    method = "delete_alerts"
    url = (
        f"https://alerts.tradingview.com/alerts/"
        f"?log_username={username}"
        f"&log_method={method}"
    )
    payload = {"m": "delete_alerts", "p": {"ids": [int(alert_id)]}}
    print(url)
    print(payload)
    headers = {
        "accept": "*/*",
        "cookie": "sessionid=" + session_id,
        "origin": "https://www.tradingview.com",
        "referer": "https://www.tradingview.com/",
    }
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload)
    ).json()

    print(response)
    return response
