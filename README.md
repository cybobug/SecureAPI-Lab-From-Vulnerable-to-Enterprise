# 🛡️ Hardened-API-Architecture-2026

An **Elite-Grade Security Laboratory** designed to showcase the complete transition from a highly vulnerable REST API to an Enterprise-Hardened, "Top 1%" Security Instance. 

This repository is a **Dual-Phase Learning Range**: 
1.  **Phase 1 (Attack)**: A deliberately insecure laboratory environment for practicing advanced exploits (SQLi, BOLA, SSRF).
2.  **Phase 2 (Defense)**: A Master-Level reference implementation of same API, hardened using architectural security standards including **Token Rotation**, **DNS Pinning**, and **Anomaly Detection**.

---

## 🏗️ Architecture Overview

The project is divided into two distinct environments:

### ☣️ [Insecure/](./Insecure/) - The Hacker's Range
A laboratory built to fail. Each endpoint is deliberately engineered with critical modern vulnerabilities:
-   **SQL Injection**: Classic string concatenation vulnerabilities.
-   **BOLA / IDOR**: Insecure direct object references in profile endpoints.
-   **Mass Assignment**: Unvalidated user update logic.
-   **Basic SSRF**: A tool that crawls any URL without restriction.
-   **Insecure AI Agency**: An AI bridge that executes privileged tasks without authorization.

### 🏰 [Secure/](./Secure/) - The Hardened Enterprise (v4.0 Final) - Top 1% Build
A professional, production-ready implementation that uses **State-of-the-Art** architectural defenses:
-   **SQLi Mitigation**: SQLAlchemy ORM-based parameterized queries.
-   **Auth & Tokens**: Direct `bcrypt` hashing + **JWT Refresh Token Rotation**.
-   **Advanced SSRF Mitigation**: Domain Whitelisting + **IP Pinning** (TOCTOU prevention).
-   **RBAC (Role-Based Access Control)**: Granular permissions for Admin, Auditor, and User roles.
-   **Anomaly Detection**: Real-time pattern monitoring for distributed brute-force detection.
-   **DoS Protection**: Early Content-Length guarding and request size limits.

---

## 🛠️ Elite Security Features (The "Top 1%" List)

This repository implements advanced security patterns often missing in standard applications:
-   **🛡️ Token Rotation & Replay Detection**: Every session refresh revokes the old token. Reusing an old token triggers a critical security alert.
-   **🛡️ DNS Rebinding Prevention**: The server resolves the IP once, then locks (pins) the request to that IP to prevent DNS manipulation.
-   **🛡️ Zero-Fallback Secrets**: The server explicitly refuses to start if the `SECRET_KEY` is not cryptographically set in the environment.
-   **🛡️ Multi-Server Throttling**: Scalable rate-limiting logic (ready for Redis integration) to stop automated brute-force attacks.
-   **🛡️ Structured JSON Auditing**: Machine-readable security logs ready for Enterprise SIEM (Splunk/ELK) integration.

---

## 🚀 Getting Started

### 1. Installation
```powershell
pip install fastapi sqlalchemy uvicorn passlib bcrypt python-jose requests
```

### 2. Setting Environment Security
```powershell
# Windows
$env:SECRET_KEY = "your-random-key"

# Linux/macOS
export SECRET_KEY="your-random-key"
```

### 3. Launching the Lab
**To Run the Insecure Laboratory:**
```powershell
cd Insecure
uvicorn main:app --reload
```

**To Run the Hardened Enterprise (Elite Build):**
```powershell
cd Secure
uvicorn main:app --reload
```

---

## 🔬 Automated Hacking Engine: `sqli_tool`
Included in this Repo is a **Custom Multithreaded SQLi Engine** built specifically for Phase 1. 
-   **Threaded Extraction**: Using `ThreadPoolExecutor` for 10x faster data exfiltration.
-   **Automated Schema Discovery**: Finds tables and columns in unknown databases.
-   **Mass Dumping**: Automatically extracts all user credentials from vulnerable endpoints.

**For usage instructions, see [sqli_tool/README.md](./sqli_tool/README.md).**

---

## 📜 Legal Disclaimer
This project is for **Educational and Ethical Security Research** only. Unauthorized testing against systems you do not own is illegal. Use this lab to become a better defender.

**"Becoming a Master Architect starts with understanding the tools of the attacker."** 🚀🏆
