from fastapi import APIRouter

from gtgh_team3_compliance_assistant.service.local_ingestion_service import IngestionService

router = APIRouter(prefix="/ingestion")

service = IngestionService()


@router.post("/eurlex")
async def ingest():
    count = await service.ingest_eurlex()
    return {"ingested_documents": count}