# Portfolio API

Personal portfolio powered by a REST API — built as a final year project.

## Stack
- Backend: FastAPI + Uvicorn
- Database: PostgreSQL (Supabase)
- Frontend: Vanilla HTML/CSS/JS
- Hosting: Render (API) + Netlify (Frontend)

## Local Setup
```bash
cd backend
pip install -r requirements.txt
# add .env with DATABASE_URL=...
uvicorn app:app --reload
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health check |
| GET | `/profile` | Profile info |
| GET | `/skills` | All skills |
| GET | `/skills/top` | Top 5 skills |
| GET | `/projects` | All projects |
| GET | `/projects/{skill}` | Projects by skill |
| GET | `/search?q=` | Search projects |
| GET | `/docs` | Swagger UI |

## Live Links
- Frontend: https://startling-mousse-24634d.netlify.app/
- API: https://me-api-playground-zrps.onrender.com/
- API Docs: https://me-api-playground-zrps.onrender.com/docs
- Resume: https://drive.google.com/file/d/1BEvvLbrZDGugoHgvB0jGYZDnpY3EpY_Q/view?usp=sharing
