# sqli_tool/utils.py
import requests
import json

def send_request(url, method="POST", data=None, params=None, is_json=True):
    """
    Sends a generic HTTP request and returns a standardized response object.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (SQLi-Testing-Engine-2026)",
            "Content-Type": "application/json" if is_json else "application/x-www-form-urlencoded"
        }

        if method.upper() == "POST":
            if is_json:
                return requests.post(url, json=data, params=params, headers=headers, timeout=10)
            return requests.post(url, data=data, params=params, headers=headers, timeout=10)
        
        return requests.get(url, params=params, headers=headers, timeout=10)
    
    except Exception as e:
        # print(f"[!] Network Error: {e}")
        return None

def encode_payload(payload):
    # Simple URL encoding if needed (requests usually handles this)
    return payload
