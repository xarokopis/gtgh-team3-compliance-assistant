from fastapi import APIRouter

from gtgh_team3_compliance_assistant.ingestion.metadata_storing import MetadataStore

router = APIRouter(prefix="/documents")

store = MetadataStore()

@router.get("/")
def get_documents():
    return store.load()