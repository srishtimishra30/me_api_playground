from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

print("DB URL Loaded:", DATABASE_URL)   # debug line

def get_conn():
    return psycopg2.connect('postgresql://postgres.jrdszycfnpfbksmbyugx:admonSupabase12@aws-1-ap-south-1.pooler.supabase.com:6543/postgres', sslmode='require')

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/profile")
def profile():
    print('debug')
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name, email, education FROM profile LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "No profile found"}), 404

    return jsonify({
        "name": row[0],
        "email": row[1],
        "education": row[2]
    })




@app.route("/skills")
def skills():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM skills;")
    data = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/skills/top")
def top_skills():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM skills LIMIT 5;")
    data = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/projects")
def projects():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT title, description, link FROM projects;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

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
    return jsonify(rows)

@app.route("/search")
def search():
    q = request.args.get("q")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT title, description FROM projects WHERE title ILIKE %s;",
        (f"%{q}%",)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/")
def home():
    return {
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
    }
if __name__ == "__main__":
    print(f'in this block {DATABASE_URL}')
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
