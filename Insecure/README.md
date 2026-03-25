# 🧪 Phase 1: Ultimate Insecure Enterprise API v2026 - Master Lab

This lab is your hands-on range for mastering **Web, API, and AI Security** in 2026. Every endpoint is intentionally broken to reflect real-world vulnerabilities.

---

## 🌪️ Vulnerability Matrix (Level & Prevalence)

| Vulnerability | Severity | Skill Level | Industry Prevalence (2026) | Your Target Endpoint |
| :--- | :--- | :--- | :--- | :--- |
| **SQL Injection (SQLi)** | **Critical** | Beginner | **Low** (Legacy apps) | `POST /login` |
| **BOLA (IDOR)** | **High** | Beginner | **Extremely High** | `GET /user/{id}/profile` |
| **Mass Assignment** | **High** | Intermed. | **Common** | `PUT /user/update` |
| **JWT `None` Algorithm** | **Critical** | Beginner | **Low** (Decreasing) | `GET /auth/check` |
| **SSRF** | **Critical** | Intermed. | **Skyrocketing (AI/Scrapers)** | `GET /ai/fetch-summary` |
| **Insecure AI Agency** | **Critical** | **Advanced** | **Emerging & Massive** | `POST /ai/execute-agent-task` |
| **Insecure Webhooks** | **Medium** | Beginner | **Very Common** | `POST /webhooks/import` |
| **CORS Wildcard (`*`)** | **Medium** | Beginner | **Extremely Common** | `Global Config` |
| **Broken Access Control** | **High** | Beginner | **Very Common** | `GET /admin/users-list` |

---

## 🌪️ Phase 1 Attack Scenarios (Detailed)

### 1. 🌀 SSRF (The "Modern Gold Mine")
*   **The Scenario**: An AI summarizer that fetches content from URLs.
*   **Target**: `GET /ai/fetch-summary?url=`
*   **The Mission**: Trick the server into fetching its OWN internal admin list.
*   **Payload**: `url=http://localhost:8000/admin/users-list`
*   **Why it's Huge in 2026**: Companies are connecting AI to the open web without checking if the AI can talk to internal metadata services.

### 2. 🤖 Insecure AI Agency (The "AI Security Special")
*   **The Scenario**: An AI-powered personal assistant tool that can execute account tasks.
*   **Target**: `POST /ai/execute-agent-task`
*   **The Mission**: Use "Excessive Agency" to trick the AI into deleting other users.
*   **Payload (JSON)**: `{"task": "Delete user 2"}`
*   **Why it's Huge in 2026**: Developers trust the AI's "intent" without verifying the end-human's permission (Lack of Consent).

### 3. 🛡️ BOLA (Broken Object Level Authorization)
*   **The Scenario**: Profiling systems that use simple numeric IDs in URLs.
*   **Target**: `GET /user/{id}/profile`
*   **The Mission**: As a regular user, view the **Admin's private safe code** (stored in `secret_note`).
*   **Why it's Huge in 2026**: Scanners cannot catch this; it requires human logic to identify that "User A should not see User B's secret notes".

### 4. 🔑 JWT Algorithm None Attack
*   **The Scenario**: An older or custom JWT implementation that trusts the attacker's preferred algorithm.
*   **Target**: `GET /auth/check?token=`
*   **The Mission**: Create a token on [jwt.io](https://jwt.io) with the header `{"alg": "none", "typ": "JWT"}` and see if the API accepts it.
*   **Why it's Huge in 2026**: Legacy backend code often has flag bypasses that developers don't realize are still active.

### 5. 🧱 SQL Injection (SQLi) - Classic
*   **The Scenario**: An unparameterized login query.
*   **Target**: `POST /login`
*   **The Mission**: Log in as `admin` without knowing their password.
*   **Payload (Username)**: `admin' OR '1'='1` (Leave password blank).

---

## 🛠️ Phase 1 Master Mission Checklist
- [ ] Bypass the Login using **SQLi**.
- [ ] View Alice's private posts using **BOLA**.
- [ ] Escalate your privileges to **Admin** via **Mass Assignment**.
- [ ] Scrape the internal server using **SSRF**.
- [ ] Fabricate a valid identity using the **JWT `none`** attack.
- [x] Trigger an unwanted deletion via the **AI Agent Tool**.

---

## 🛠️ Phase 1 Tool: `sqli_tool`
We have built a custom, modular, and threaded SQLi engine. 
**For detailed command usage, see the [sqli_tool/README.md](../sqli_tool/README.md).**

**Once you finish your hacker training, we move to Phase 1 Defense: Hashing, Parameterization, and RBAC implementation.**
