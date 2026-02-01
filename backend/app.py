from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not set")
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return jsonify({"message": "API running"})

# ---------- PROFILE ----------
@app.route("/profile")
def profile():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT name, email, education FROM profile LIMIT 1;")
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return jsonify({"error": "No profile data"}), 404

        return jsonify({
            "name": row[0],
            "email": row[1],
            "education": row[2]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- SKILLS ----------
@app.route("/skills")
def skills():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT name FROM skills;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([r[0] for r in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- PROJECTS ----------
@app.route("/projects")
def projects():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT title, description, link FROM projects;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify([
            {"title": r[0], "description": r[1], "link": r[2]}
            for r in rows
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
