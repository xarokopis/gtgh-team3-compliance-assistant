Activate API: `uv run uvicorn gtgh_team3_compliance_assistant.main:app --reload`

Swagger UI: `http://127.0.0.1:8000/docs`

API endpoints:
- Health check: `GET /health`
- Ingestion: `POST /ingestion/eurlex`
- Get documents: `GET /documents`

Files are stored in data/raw/eurlex