import requests
import json

def alert(username, symbol, alert_title, message, level, webhook_url, session_id, cancel_lvl):
    username = username
    webhook_url = webhook_url
    symbol = symbol
    alert_name = alert_title
    alert_mssg = message
    alert_level = level
    session_id = session_id
    method = "create_alert"
    alert_type = "price"
    m = "create_alert"

    url = (
        f"https://alerts.tradingview.com/alerts/?"
        f"?log_username={username}"
        f"&log_method={method}"
    )
    extra_data = {
        "version": 22,
        "condition": {
            "id": "cross",
            "fireInfo": {"frequency": "on_first_fire"},
            "mainSeries": {"id": "0"},
            "alertSeries": {"id": "0"},
            "band": {"id": "special"},
        },
        "statesForAlert": {
            "0": {
                "type": "MainSeries",
                "proSymbol": symbol,
                "actualSymbol": symbol,
                "symbolString": f'={{"symbol":"{symbol}"}}',
            },
            "special": {
                "type": "Value",
                "value": str(alert_level),
            },
        },
    }
    payload = {
        "m": m,
        "p": {
            "name": alert_name,
            "alert_type": alert_type,
            "web_hook": webhook_url,
            "internal_sym": {
                "adjustment": "splits",
                "session": "regular",
                "symbol": symbol,
            },
            "inf_exp": True,
            "sym": symbol,
            "snd_file": "alert/chirpy",
            "snd_duration": 0,
            "snd": True,
            "push": True,
            "sms": False,
            "script_deps": [],
            "script": "/",
            "res": "1",
            "popup": True,
            "extra": json.dumps(extra_data),
            "exp": 1680512623,
            "email": False,
            "desc": alert_mssg,
            "deact": True,
            "cross_int": True,
            "inputs": {
                "in_0": {"f": True, "t": "text", "v": alert_mssg},
                "in_1": {"f": True, "t": "float", "v": alert_level},
            },
            "gen_alert_data": {
                "frequency": "on_first_fire",
                "primitive_alert": {"type": "cross", "price": alert_level},
            },
        },
    }
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
    print("alert placed: " + str(alert_id["id"]))
    return alert_id