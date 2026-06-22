from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.schemas.evidence_schema import EvidenceCreate, EvidenceResponse
from app.services.evidence_service import EvidenceService
from app.dependencies.auth_dependency import get_current_user_id

router = APIRouter()

@router.post("/", response_model=EvidenceResponse)
async def upload_evidence(
    data: EvidenceCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    service = EvidenceService(db)
    try:
        return await service.submit_evidence(user_id=current_user_id, data=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/task/{task_id}")
async def get_evidences(task_id: int, db: AsyncSession = Depends(get_async_db)):
    service = EvidenceService(db)
    return await service.get_task_evidences(task_id)