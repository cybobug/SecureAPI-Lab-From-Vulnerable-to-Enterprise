# sqli_tool/detector.py
import time
from .payloads import BOOLEAN_BASED, ERROR_BASED, TIME_BASED
from .utils import send_request
from .analyzer import ResponseInfo, is_vulnerable, analyze_time

def test_sqli(url, param_name, method="POST", base_data=None):
    """
    Finds vulnerabilities by comparing baseline and test responses.
    """
    print(f"\r[*] Testing parameter: '{param_name}'...", end="")
    
    # Baseline
    r_base = ResponseInfo(send_request(url, method, base_data))
    
    # 1. Test Boolean-True
    payload_true = BOOLEAN_BASED["true"][0]
    test_data_true = base_data.copy()
    test_data_true[param_name] = f"{base_data[param_name]}{payload_true}"
    r_true = ResponseInfo(send_request(url, method, test_data_true))
    
    # 2. Test Boolean-False
    payload_false = BOOLEAN_BASED["false"][0]
    test_data_false = base_data.copy()
    test_data_false[param_name] = f"{base_data[param_name]}{payload_false}"
    r_false = ResponseInfo(send_request(url, method, test_data_false))
    
    # Analysis
    if is_vulnerable(r_true, r_false):
        print(f"\n[+] VULNERABILITY FOUND: Parameter '{param_name}' is susceptible to Boolean SQLi!")
        return {"vulnerable": True, "type": "BOOLEAN"}

    # 3. Test Time-Based (SQLite specialized for this lab)
    payload_time = TIME_BASED[0]
    test_data_time = base_data.copy()
    test_data_time[param_name] = f"{base_data[param_name]}{payload_time}"
    
    start = time.time()
    send_request(url, method, test_data_time)
    end = time.time()
    
    if analyze_time(start, end):
        print(f"\n[+] VULNERABILITY FOUND: Parameter '{param_name}' is susceptible to Time-Based SQLi!")
        return {"vulnerable": True, "type": "TIME"}

    return {"vulnerable": False}
