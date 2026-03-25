from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import User, Post, get_db, engine
from pydantic import BaseModel
from sqlalchemy import text
import jose.jwt
from datetime import datetime, timedelta
import requests # For SSRF demonstration
from typing import List, Optional

app = FastAPI(title="Ultimate Insecure Enterprise API v2026", description="Phase 1 - MASTER LAB")

# --- VULNERABLE CORS (Wildcard) ---
# Companies often set this to allow 'everything' during development and forget it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # VULNERABLE: Allows any site to read your data via JS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INSECURE CONFIGURATION ---
SECRET_KEY = "weakkey"
ADMIN_TOKEN = "SUPER_SECRET_ADMIN_MAGIC_WORD_2026" 

# --- Pydantic Models ---
class UserLogin(BaseModel) : username: str; password: str
class UserProfile(BaseModel): id: int; username: str; email: str; is_admin: bool; secret_note: Optional[str] = None
class PostModel(BaseModel): id: int; title: str; content: str; author_id: int; is_private: bool
class AIQuery(BaseModel): task: str; url: Optional[str] = None

# --- DATABASE SETUP ---
@app.on_event("startup")
def startup():
    db = next(get_db())
    if not db.query(User).first():
        db.add(User(username="admin", password="password123", email="admin@corp.com", is_admin=True, secret_note="Safe code: 8888"))
        db.add(User(username="alice", password="alice_password", email="alice@corp.com", is_admin=False, secret_note="Pizza Lover"))
        db.add(Post(title="Admin's Private Post", content="Hidden treasure", author_id=1, is_private=True))
        db.add(Post(title="Alice's Public Post", content="Hello!", author_id=2, is_private=False))
        db.commit()

# --- 1. SSRF (Server-Side Request Forgery) ---
# HUGE in 2026: AI features that "fetch" a website to summarize it.
@app.get("/ai/fetch-summary")
def ai_fetch_summary(url: str):
    # VULNERABLE: Fetches ANY URL. Try fetching http://localhost:8000/admin/users-list internal or AWS metadata!
    try:
        response = requests.get(url, timeout=5)
        return {"summary": response.text[:100], "status": "Fetched successfully!"}
    except Exception as e:
        return {"error": str(e)}

# --- 2. INDIRECT PROMPT INJECTION SIMULATION ---
@app.post("/ai/execute-agent-task")
def ai_agent_task(query: AIQuery, db: Session = Depends(get_db)):
    # VULNERABLE: The 'AI' reads a task and executes a command WITH privileges.
    # If the 'task' says "delete user 2", it does it!
    # In 2026, an attacker puts this 'task' in a PDF or Post that the AI reads.
    task_str = query.task.lower()
    
    if "delete" in task_str and "user" in task_str:
        # Simulate deleting user without second auth
        user_id = int(task_str.split("user")[-1].strip())
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return {"status": f"AI deleted user {user_id} based on your request."}
    
    return {"status": "AI didn't understand. (Try 'Delete user 2')"}

# --- 3. INSECURE WEBHOOKS ---
# Common in 2026 for integrations (Stripe, GitHub, Slack).
@app.post("/webhooks/import")
def import_data(data: dict):
    # VULNERABLE: No signature verification (HMAC). Anyone can send fake data to this endpoint.
    return {"message": "Data imported!", "received": data}

# --- 4. ADVANCED BOLA (Leaking Private Data via Relationships) ---
@app.get("/user/posts")
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    # VULNERABLE: BOLA. Changing user_id lets you see any user's private posts.
    posts = db.query(Post).filter(Post.author_id == user_id).all()
    return posts

# --- 5. THE CORE WEB LABS (SQLi, BAC, Mass Assignment) ---
@app.get("/search-users")
def search_users(q: str, db: Session = Depends(get_db)):
    # SQLi in LIKE search - Union-based SQLi target!
    query = text(f"SELECT username, email FROM users WHERE username LIKE '%{q}%'")
    try:
        result = db.execute(query).fetchall()
        return [{"username": r[0], "email": r[1]} for r in result]
    except Exception as e:
        print(f"SQL Error in Search: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    query = text(f"SELECT * FROM users WHERE username = '{user.username}' AND password = '{user.password}'")
    result = db.execute(query).fetchone()
    if not result: raise HTTPException(status_code=401, detail="Fail")
    token = jose.jwt.encode({"id": result[0]}, SECRET_KEY, algorithm="HS256")
    return {"token": token}

@app.get("/admin/users-list")
def list_users(db: Session = Depends(get_db)):
    # BAC: Hidden but no check.
    return db.query(User).all()

@app.put("/user/update")
def update_user(user_id: int, data: dict, db: Session = Depends(get_db)):
    # Mass Assignment
    user = db.query(User).filter(User.id == user_id).first()
    for k, v in data.items(): setattr(user, k, v)
    db.commit()
    return {"status": "Updated"}

@app.get("/auth/check")
def check_jwt(token: str):
    # JWT None Algorithm Attack
    payload = jose.jwt.decode(token, SECRET_KEY, algorithms=["HS256", "none"], options={"verify_signature": False if "none" in token else True})
    return payload

@app.get("/")
def home(): return {"message": "Ultimate Insecure Enterprise API v2026. Ready for Masters."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
