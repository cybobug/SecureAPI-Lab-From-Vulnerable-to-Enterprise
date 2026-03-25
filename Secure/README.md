# 🛡️ Professional Secure API v2026 - Security Architecture

This repository contains the **Hardened Reference Implementation** of a modern REST API using **FastAPI** and **SQLAlchemy**. Every vulnerability from our "Insecure" lab has been mitigated using Enterprise-Grade standards.

---

## 🏗️ Security Implementation Details

### 1. 🌀 SQL Injection (SQLi) - FIXED
- **Fix**: Replaced raw `text()` string concatenation with **SQLAlchemy ORM Parameterized queries**.
- **Defense**: SQLAlchemy's `filter()` automatically binds parameters, making SQL injection mathematically impossible.

### 2. 🔐 Authentication & Broken Auth - FIXED
- **Fix**: Replaced plaintext passwords with **Bcrypt (Passlib)** salts & hashes.
- **Defense**: Even if the database is leaked, an attacker cannot reverse the passwords. Passwords are never stored or transmitted in plain text.

### 3. 🎫 JWT Attacks - FIXED
- **Fix**: Hardcoded a fixed **HS256 Algorithm** and forced **Signature & Expiry verification**.
- **Defense**: Explicitly rejects the `none` algorithm and verifies that the `SECRET_KEY` is valid.

### 4. 🔗 BOLA / IDOR (Broken Object Level Authorization) - FIXED
- **Fix**: Implemented a **Per-Request Authorization Check**.
- **Defense**: The API checks if `current_user.id` matches the `requested_user_id` before returning any data.

### 🍱 5. Mass Assignment - FIXED
- **Fix**: Used **Pydantic Schemas** (`UserUpdate`) to explicitly define allowed fields.
- **Defense**: If an attacker sends `{"is_admin": true}`, the Pydantic validator will **silently ignore it**, as it's not in the schema.

### 📡 6. SSRF (Server-Side Request Forgery) - FIXED
- **Fix**: Implemented **Host Whitelisting** (`TRUSTED_DOMAINS`).
- **Defense**: The server will reject any URL targeting internal IPs (localhost, 169.254.x.x) or unapproved external domains.

### 🤖 7. Insecure AI Agency - FIXED
- **Fix**: Implemented **Least Privilege** for the AI Agent bridge.
- **Defense**: The AI tool is explicitly blocked from "admin" or "delete" keywords and requires `current_user` context for every action.

### 🚧 8. Broken Access Control (BAC) - FIXED
- **Fix**: Created a `require_admin` **FastAPI Dependency**.
- **Defense**: Centralized role-checking ensures that sensitive endpoints (like listing all users) are completely inaccessible to non-admins.

---

## 🚀 Deployment Instructions
1. Run the server: `uvicorn Secure.main:app --reload`
2. All passwords must be hashed before entry into the database.
3. Access secure docs at: `http://127.0.0.1:8000/docs`
