# REST API Practice 🚀
A full-stack REST API project built with **FastAPI** (backend) and **HTML/CSS/JS** (frontend).

## 📁 Project Structure

```REST-API-Practice/
├── backend/
│   ├── app.py         
│   ├── requirements.txt
│   └── Procfile
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL / Supabase
- **Tools:** Postman, Git

## ⚙️ How to Run Locally
### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```
### Frontend
Open `frontend/index.html` in your browser.

## 🌐 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/`      | Health check |
| GET    | `/items` | Get all items |
| POST   | `/items` | Create new item |

