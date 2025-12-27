from typing import Optional, List, Any
from pydantic import BaseModel, Field


class MedicalCaseBase(BaseModel):
    case_id: str
    age: Optional[str] = None
    gender: Optional[str] = None
    modality: str
    body_part: str
    diagnosis: str
    findings: Optional[str] = None
    clinical_notes: Optional[str] = None
    image_path: str
    image_url: Optional[str] = None
    source: Optional[str] = "custom"
    metadata: Optional[Any] = None


class MedicalCaseCreate(MedicalCaseBase):
    pass


class MedicalCaseResponse(MedicalCaseBase):
    id: int
    similarity_score: Optional[float] = None

    class Config:
        orm_mode = True


class SearchRequest(BaseModel):
    query: Optional[str] = None
    image: Optional[str] = None  # base64 string
    modality: Optional[str] = None
    body_part: Optional[str] = None
    limit: int = 10
    similarity_threshold: float = 0.0


class SearchResponse(BaseModel):
    results: List[MedicalCaseResponse]
    total: int
    query_time_ms: float
