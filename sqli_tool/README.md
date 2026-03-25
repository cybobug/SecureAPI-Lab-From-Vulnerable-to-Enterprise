# ⚙️ SQLi Testing Engine v2026 - Tool Documentation

The **SQLi Testing Engine** is a modular, multithreaded security research tool designed to detect and exploit SQL injection vulnerabilities in REST APIs.

## 🚀 Execution Commands

### 1. 🔍 Detection Mode
Detect if a specific parameter on an endpoint is vulnerable to SQL injection.
```powershell
python -m sqli_tool.main --mode detect --url http://127.0.0.1:8000/login --param username
```

### 🔭 2. Discovery Mode (Schema Enumeration)
Automatically find all table names in the target database using metadata extraction.
```powershell
python -m sqli_tool.main --mode discover --url http://127.0.0.1:8000/login --param username
```

### 🗝️ 3. Dump All Mode (Mass Extraction)
Automatically extract **all** usernames and passwords from the `users` table using a **threaded binary search**.
```powershell
python -m sqli_tool.main --mode dump-all --url http://127.0.0.1:8000/login --param username
```

---

## 🏗️ Architecture Modules
-   `main.py`: Entry point for all commands.
-   `detector.py`: Automated scanning logic.
-   `extractor.py`: Multithreaded extraction engine (Binary Search).
-   `payloads.py`: Categorized attack strings (Boolean, Union, Time).
-   `analyzer.py`: Response analysis engine.
-   `utils.py`: HTTP communication layer.

---

## ⚡ Performance Optimization
This version of the tool uses **Python Threading (`ThreadPoolExecutor`)** to perform 10 simultaneous extraction requests, making password discovery up to **10x faster** than linear brute-force.


Key Commands Included:
Detection: python -m sqli_tool.main --mode detect
Schema Discovery: python -m sqli_tool.main --mode discover
Full Table Dump (Multi-user): python -m sqli_tool.main --mode dump-all