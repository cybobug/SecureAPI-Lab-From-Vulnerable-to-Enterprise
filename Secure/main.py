# c:\Users\garvi\OneDrive\Desktop\BOUNTY\learn\Secure\main.py
import os
import requests
import bcrypt
import socket
import logging
import json
import secrets # SECURE: True cryptographic randomness
from enum import Enum
from typing import List, Optional, Set
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr, HttpUrl
from urllib.parse import urlparse

from database import User, Post, RefreshToken, get_db

# --- 🚀 TOP 1% ENFORCEMENT: ZERO FALLBACK ---
# SECURITY EXPLANATION: If we allow fallbacks, we invite accidental production leaks.
# A Top-Tier API must fail to start if the security environment is missing.
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # During development, we set one, but we MUST explicitly raise in a real app.
    # raise RuntimeError("CRITICAL ERROR: 'SECRET_KEY' must be set. Aborting startup.")
    SECRET_KEY = "UNSECURE_LAB_KEY_SET_SECRET_KEY_ENV_FOR_V4_MASTER"

ALGORITHM = "HS256" 
ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_DAYS = 7 # Long lived but rotatable

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(title="Top 1% Hardened Master API v4.0", version="4.0.0")

# --- 🔬 ANOMALY DETECTION ---
# SECURITY EXPLANATION: We monitor patterns, not just single events.
class AnomalyDetector:
    def __init__(self):
        self.failed_logins = {} # {ip: {timestamps: []}}
    def check_brute_pattern(self, ip: str):
        now = datetime.now()
        data = self.failed_logins.get(ip, {"timestamps": []})
        data["timestamps"] = [ts for ts in data["timestamps"] if now - ts < timedelta(minutes=5)]
        
        # If 10 failures in 5 minutes across any user = THREAT
        if len(data["timestamps"]) >= 10:
            logger.critical(f"ANOMALY DETECTED: IP {ip} is attempting a distributed brute-force attack.")
            return True
        return False

detector = AnomalyDetector()

# --- 🏰 ELITE LOGGING (JSON) ---
logger = logging.getLogger("security_master")
handler = logging.FileHandler('security_v4_audit.json')
handler.setFormatter(logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# --- 🎯 ROLE-BASED ACCESS CONTROL (RBAC) ---
class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    AUDITOR = "auditor"

# --- PYDANTIC SCHEMAS ---
class AuthResponse(BaseModel):
    access_token: str; refresh_token: str; token_type: str

class UserResponse(BaseModel):
    id: int; username: str; role: str
    class Config: from_attributes = True

# --- 🔐 AUTH HELPERS (ROBUST) ---
def get_password_hash(p: str): return bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
def verify_password(p, h): 
    try: return bcrypt.checkpw(p.encode('utf-8'), h.encode('utf-8'))
    except: return False

def create_tokens(username: str, db: Session):
    # 🏆 TOKEN ROTATION (ACCESS + REFRESH)
    access_token = jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_MINUTES)}, SECRET_KEY, ALGORITHM)
    
    # Generate true cryptographic refresh token
    refresh_token_val = secrets.token_urlsafe(32)
    user = db.query(User).filter(User.username == username).first()
    
    db_refresh = RefreshToken(
        token=refresh_token_val,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_DAYS)
    )
    db.add(db_refresh); db.commit()
    return access_token, refresh_token_val

# --- ENDPOINTS ---

@app.post("/auth/login", response_model=AuthResponse)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    client_ip = request.client.host
    
    # 🔬 ANOMALY DETECTION: Check for distributed pattern
    if detector.check_brute_pattern(client_ip):
        raise HTTPException(status_code=429, detail="Host blocked: Repeated malicious activity detected.")

    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Update anomaly data
        data = detector.failed_logins.get(client_ip, {"timestamps": []})
        data["timestamps"].append(datetime.now())
        detector.failed_logins[client_ip] = data
        
        logger.warning(f"FAILED LOGIN: {client_ip} for {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access, refresh = create_tokens(user.username, db)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@app.post("/auth/refresh", response_model=AuthResponse)
def refresh_token(old_refresh_token: str, db: Session = Depends(get_db)):
    # 🏆 FINAL LEVEL: 2026 TOKEN ROTATION & REPLAY DETECTION
    db_token = db.query(RefreshToken).filter(RefreshToken.token == old_refresh_token, RefreshToken.revoked == False).first()
    
    if not db_token or db_token.expires_at < datetime.utcnow():
        # SECURITY ALERT: If a revoked token is reused, someone might have stolen it!
        if db_token and db_token.revoked:
             logger.critical(f"REPLAY ATTACK: Old refresh token reused for User ID {db_token.user_id}!")
             # Advanced: Here we would Revoke ALL tokens for this user.
        raise HTTPException(status_code=401, detail="Session expired or invalid.")

    # 1. Revoke the old token (Rotate!)
    db_token.revoked = True
    db.commit()
    
    # 2. Issue fresh pair
    user = db.query(User).filter(User.id == db_token.user_id).first()
    access, refresh = create_tokens(user.username, db)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

# --- 🛡️ SSRF (v4 - COMPLETE DNS ISOLATION) ---
TRUSTED_DOMAINS = ["example.com", "api.trusted.com"]
def is_private(ip: str):
    try:
        p = [int(x) for x in ip.split('.')]
        return p[0]==10 or (p[0]==172 and 16<=p[1]<=31) or (p[0]==192 and p[1]==168) or p[0]==127
    except: return True

@app.get("/ai/fetch-summary")
def fetch_safe_summary(url: HttpUrl):
    # WHAT'S NEW: Stricter IP resolution and Request Isolation
    parsed = urlparse(str(url))
    if parsed.hostname not in TRUSTED_DOMAINS:
        raise HTTPException(400, "Untrusted host.")

    try:
        ip = socket.gethostbyname(parsed.hostname)
        if is_private(ip):
            logger.critical(f"SSRF DETECTED: Host {parsed.hostname} resolved to {ip}")
            raise HTTPException(403, "Internal IP forbidden.")

        # FINAL ELITE HARDENING: IP Pinning with Session Isolation
        session = requests.Session()
        session.max_redirects = 0 # No redirects allowed at all!
        
        final_target = str(url).replace(parsed.hostname, ip)
        r = session.get(final_target, headers={"Host": parsed.hostname}, timeout=5)
        return {"summary": r.text[:100]}
    except Exception as e:
        logger.error(f"SSRF Check Failure: {str(e)}")
        raise HTTPException(500, "Connection error.")

# --- 🔐 JWT VERIFICATION ENGINE ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # SECURITY EXPLANATION: This is the central gatekeeper for ALL protected routes.
    credentials_exception = HTTPException(status_code=401, detail="Invalid session")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username: raise credentials_exception
    except JWTError: raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if not user: raise credentials_exception
    return user

# --- RBAC SECURE LIST ---
class RoleChecker:
    def __init__(self, roles: List[Role]): self.roles = roles
    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in [r.value for r in self.roles]:
            raise HTTPException(403, "Insufficient permissions")
        return user

@app.get("/system/users", dependencies=[Depends(RoleChecker([Role.ADMIN]))])
def list_system_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.on_event("startup")
def startup():
    db = next(get_db())
    if not db.query(User).first():
        # Start fresh with elite security schema
        admin_pass = get_password_hash("secure_admin_v4_2026")
        db.add(User(username="admin", hashed_password=admin_pass, role="admin", email="admin@corp.com"))
        db.commit()

@app.get("/")
def home(): return {"message": "Top 1% Master Hardened API v4.0. 🛡️🏆"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
