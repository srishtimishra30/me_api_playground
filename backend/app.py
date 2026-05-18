from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import psycopg2, psycopg2.pool, os
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

pool: psycopg2.pool.SimpleConnectionPool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL, sslmode='require')
    yield
    pool.closeall()

app = FastAPI(
    title="Portfolio API",
    description="Personal portfolio API for projects, skills and profile",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_conn():
    return pool.getconn()

def release_conn(conn):
    pool.putconn(conn)


class Profile(BaseModel):
    name: str
    email: str
    education: str

class Project(BaseModel):
    title: str
    description: str
    link: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/profile", response_model=Profile)
def profile():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, email, education FROM profile LIMIT 1;")
        row = cur.fetchone()
        cur.close()
        if row is None:
            raise HTTPException(status_code=404, detail="No profile found")
        return Profile(name=row[0], email=row[1], education=row[2])
    finally:
        release_conn(conn)


@app.get("/skills", response_model=List[str])
def skills():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT name FROM skills ORDER BY name;")
        data = [r[0] for r in cur.fetchall()]
        cur.close()
        return data
    finally:
        release_conn(conn)


@app.get("/skills/top", response_model=List[str])
def top_skills():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT name FROM skills ORDER BY name LIMIT 5;")
        data = [r[0] for r in cur.fetchall()]
        cur.close()
        return data
    finally:
        release_conn(conn)


@app.get("/projects", response_model=List[Project])
def projects():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT title, description, link FROM projects;")
        rows = cur.fetchall()
        cur.close()
        return [Project(title=r[0], description=r[1], link=r[2]) for r in rows]
    finally:
        release_conn(conn)


@app.get("/projects/{skill}", response_model=List[Project])
def projects_by_skill(skill: str):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT DISTINCT title, description, link FROM projects WHERE skill ILIKE %s;",
            (skill,)
        )
        rows = cur.fetchall()
        cur.close()
        return [Project(title=r[0], description=r[1], link=r[2]) for r in rows]
    finally:
        release_conn(conn)


@app.get("/search", response_model=List[Project])
def search(q: Optional[str] = Query(None)):
    if not q:
        return []
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT title, description, link FROM projects WHERE title ILIKE %s OR description ILIKE %s;",
            (f"%{q}%", f"%{q}%")
        )
        rows = cur.fetchall()
        cur.close()
        return [Project(title=r[0], description=r[1], link=r[2]) for r in rows]
    finally:
        release_conn(conn)


@app.get("/")
def home():
    return {
        "message": "Portfolio API v2 is running",
        "docs": "/docs",
        "endpoints": ["/health", "/profile", "/skills", "/skills/top", "/projects", "/projects/{skill}", "/search?q="]
    }
