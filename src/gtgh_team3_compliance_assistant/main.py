from fastapi import FastAPI

from gtgh_team3_compliance_assistant.api.documents import router as documents_router
from gtgh_team3_compliance_assistant.api.ingestion import router as ingestion_router
from gtgh_team3_compliance_assistant.api.health import router as health_router

app = FastAPI(title="Compliance Assistant")

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(ingestion_router)


@app.get("/")
def root():
    return {"message": "running"}