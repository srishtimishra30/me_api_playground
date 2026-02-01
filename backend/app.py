from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

print("DB URL Loaded:", DATABASE_URL)

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "API is running",
        "endpoints": [
            "/health",
            "/profile",
            "/skills",
            "/skills/top",
            "/projects",
            "/projects/python",
            "/search?q=ai"
        ]
    })


# -------------------------
# PROFILE
# -------------------------
@app.route("/profile")
def profile():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name, email, education FROM profile LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({
        "name": row[0],
        "email": row[1],
        "education": row[2]
    })


# -------------------------
# SKILLS
# -------------------------
@app.route("/skills")
def skills():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM skills;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([r[0] for r in rows])


# -------------------------
# TOP SKILLS
# -------------------------
@app.route("/skills/top")
def top_skills():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM skills LIMIT 5;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([r[0] for r in rows])


# -------------------------
# PROJECTS
# -------------------------
@app.route("/projects")
def projects():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT title, description, link FROM projects;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {
            "title": r[0],
            "description": r[1],
            "link": r[2]
        }
        for r in rows
    ])


# -------------------------
# PROJECTS BY SKILL
# -------------------------
@app.route("/projects/<skill>")
def projects_by_skill(skill):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT title, description, link FROM projects WHERE description ILIKE %s;",
        (f"%{skill}%",)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {
            "title": r[0],
            "description": r[1],
            "link": r[2]
        }
        for r in rows
    ])


# -------------------------
# SEARCH
# -------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "")

    if not q:
        return jsonify([])

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT title, description FROM projects WHERE title ILIKE %s;",
        (f"%{q}%",)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {
            "title": r[0],
            "description": r[1]
        }
        for r in rows
    ])


# -------------------------
# RUN LOCAL (ignored by Render)
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
